import json
import logging
from datetime import datetime, timedelta
from config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intentar importar Redis, si no está disponible usar simulador
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis no está instalado, usando simulador en memoria")

class RedisManager:
    def __init__(self):
        self.redis_client = None
        self.connect()
    
    def connect(self):
        """Establecer conexión con Redis o usar simulador"""
        if not REDIS_AVAILABLE:
            # Usar simulador en memoria
            from redis_alternative import InMemoryRedis
            self.redis_client = InMemoryRedis()
            logger.info("Usando simulador Redis en memoria")
            return True
        
        try:
            # Intentar conectar a Redis real
            self.redis_client = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                password=Config.REDIS_PASSWORD,
                db=Config.REDIS_DB,
                decode_responses=Config.REDIS_DECODE_RESPONSES
            )
            # Probar la conexión
            self.redis_client.ping()
            logger.info("Conexión a Redis establecida exitosamente")
            return True
        except Exception as e:
            logger.warning(f"Redis no disponible ({e}), usando simulador en memoria")
            # Usar simulador como fallback
            from redis_alternative import InMemoryRedis
            self.redis_client = InMemoryRedis()
            return True
    
    def disconnect(self):
        """Cerrar conexión con Redis"""
        if self.redis_client:
            self.redis_client.close()
            logger.info("Conexión a Redis cerrada")
    
    def is_connected(self):
        """Verificar si Redis está conectado"""
        try:
            if self.redis_client:
                self.redis_client.ping()
                return True
        except:
            pass
        return False
    
    def set_token_revoked(self, jti, token_type, user_id, expires_at):
        """Marcar token como revocado en Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            # Calcular TTL basado en la expiración del token
            now = datetime.utcnow()
            if isinstance(expires_at, datetime):
                ttl = int((expires_at - now).total_seconds())
            else:
                ttl = 3600  # 1 hora por defecto
            
            # Solo almacenar si el token no ha expirado
            if ttl > 0:
                token_data = {
                    'jti': jti,
                    'token_type': token_type,
                    'user_id': user_id,
                    'revoked_at': now.isoformat(),
                    'expires_at': expires_at.isoformat() if isinstance(expires_at, datetime) else expires_at
                }
                
                key = f"revoked_token:{jti}"
                self.redis_client.setex(key, ttl, json.dumps(token_data))
                logger.info(f"Token {jti} marcado como revocado en Redis")
                return True
            return False
        except Exception as e:
            logger.error(f"Error marcando token como revocado en Redis: {e}")
            return False
    
    def is_token_revoked(self, jti):
        """Verificar si un token está revocado en Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            key = f"revoked_token:{jti}"
            result = self.redis_client.get(key)
            return result is not None
        except Exception as e:
            logger.error(f"Error verificando token revocado en Redis: {e}")
            return False
    
    def revoke_all_user_tokens(self, user_id):
        """Revocar todos los tokens de un usuario en Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            # Buscar todos los tokens del usuario
            pattern = f"revoked_token:*"
            keys = self.redis_client.keys(pattern)
            
            revoked_count = 0
            for key in keys:
                token_data = self.redis_client.get(key)
                if token_data:
                    data = json.loads(token_data)
                    if data.get('user_id') == user_id:
                        # Marcar como revocado masivamente
                        self.redis_client.setex(key, 3600, token_data)  # 1 hora TTL
                        revoked_count += 1
            
            logger.info(f"Revocados {revoked_count} tokens del usuario {user_id} en Redis")
            return True
        except Exception as e:
            logger.error(f"Error revocando tokens del usuario en Redis: {e}")
            return False
    
    def log_audit_action(self, user_id, action, token_jti=None, ip_address=None, user_agent=None):
        """Registrar acción de auditoría en Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            audit_data = {
                'user_id': user_id,
                'action': action,
                'token_jti': token_jti,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Usar timestamp como parte de la clave para ordenamiento
            timestamp = int(datetime.utcnow().timestamp() * 1000)  # milisegundos
            key = f"audit_log:{user_id}:{timestamp}"
            
            # Almacenar con TTL de 30 días
            self.redis_client.setex(key, 2592000, json.dumps(audit_data))
            
            # También mantener una lista de claves de auditoría por usuario para consultas rápidas
            list_key = f"user_audit_keys:{user_id}"
            self.redis_client.lpush(list_key, key)
            self.redis_client.expire(list_key, 2592000)  # 30 días
            
            logger.info(f"Acción de auditoría registrada en Redis: {action} para usuario {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error registrando auditoría en Redis: {e}")
            return False
    
    def get_user_audit_log(self, user_id, limit=50):
        """Obtener bitácora de auditoría de un usuario desde Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            list_key = f"user_audit_keys:{user_id}"
            audit_keys = self.redis_client.lrange(list_key, 0, limit - 1)
            
            audit_log = []
            for key in audit_keys:
                audit_data = self.redis_client.get(key)
                if audit_data:
                    audit_log.append(json.loads(audit_data))
            
            return audit_log
        except Exception as e:
            logger.error(f"Error obteniendo auditoría del usuario desde Redis: {e}")
            return []
    
    def get_all_audit_log(self, limit=100):
        """Obtener bitácora de auditoría general desde Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            # Buscar todas las claves de auditoría
            pattern = f"audit_log:*"
            keys = self.redis_client.keys(pattern)
            
            # Ordenar por timestamp (las claves incluyen timestamp)
            keys.sort(reverse=True)
            keys = keys[:limit]
            
            audit_log = []
            for key in keys:
                audit_data = self.redis_client.get(key)
                if audit_data:
                    audit_log.append(json.loads(audit_data))
            
            return audit_log
        except Exception as e:
            logger.error(f"Error obteniendo auditoría general desde Redis: {e}")
            return []
    
    def store_user_session(self, user_id, session_data, ttl=3600):
        """Almacenar datos de sesión del usuario en Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            key = f"user_session:{user_id}"
            self.redis_client.setex(key, ttl, json.dumps(session_data))
            return True
        except Exception as e:
            logger.error(f"Error almacenando sesión del usuario en Redis: {e}")
            return False
    
    def get_user_session(self, user_id):
        """Obtener datos de sesión del usuario desde Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            key = f"user_session:{user_id}"
            session_data = self.redis_client.get(key)
            if session_data:
                return json.loads(session_data)
            return None
        except Exception as e:
            logger.error(f"Error obteniendo sesión del usuario desde Redis: {e}")
            return None
    
    def delete_user_session(self, user_id):
        """Eliminar sesión del usuario de Redis"""
        try:
            if not self.is_connected():
                self.connect()
            
            key = f"user_session:{user_id}"
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error eliminando sesión del usuario de Redis: {e}")
            return False

# Instancia global de Redis
redis_manager = RedisManager()

