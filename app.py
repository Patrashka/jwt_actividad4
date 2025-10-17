from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, 
    create_refresh_token, get_jwt_identity, get_jwt,
    verify_jwt_in_request
)
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
import uuid
from datetime import datetime, timedelta
import logging
import time

from config import Config
from database import db
from models import User, RevokedToken, TokenAudit
from redis_manager import redis_manager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Configurar CORS
CORS(app)

# Configurar JWT
jwt = JWTManager(app)

# Callback para verificar tokens revocados (SQL)
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Verificar si un token está en la blocklist"""
    jti = jwt_payload['jti']
    return RevokedToken.is_revoked(jti)

# Callback para verificar tokens revocados (Redis)
def check_if_token_revoked_redis(jwt_header, jwt_payload):
    """Verificar si un token está en la blocklist de Redis"""
    jti = jwt_payload['jti']
    return RevokedToken.is_revoked_redis(jti)

# Callback para manejar tokens expirados
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'El token ha expirado',
        'error': 'token_expired'
    }), 401

# Callback para manejar tokens inválidos
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Token inválido',
        'error': 'invalid_token'
    }), 401

# Callback para manejar tokens faltantes
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'message': 'Token de autorización requerido',
        'error': 'authorization_required'
    }), 401

# Callback para manejar tokens revocados
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Token ha sido revocado',
        'error': 'token_revoked'
    }), 401

def get_client_info():
    """Obtener información del cliente (IP y User-Agent)"""
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')
    return ip_address, user_agent

def log_token_action(user_id, action, token_jti=None):
    """Registrar acción de token en la bitácora"""
    ip_address, user_agent = get_client_info()
    audit = TokenAudit(user_id, action, token_jti, ip_address, user_agent)
    audit.save()

@app.route('/api/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({
                'message': 'Username, email y password son requeridos',
                'error': 'missing_fields'
            }), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validaciones básicas
        if len(username) < 3:
            return jsonify({
                'message': 'El username debe tener al menos 3 caracteres',
                'error': 'invalid_username'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'message': 'La contraseña debe tener al menos 6 caracteres',
                'error': 'invalid_password'
            }), 400
        
        # Verificar si el usuario ya existe
        if User.find_by_username(username):
            return jsonify({
                'message': 'El username ya está en uso',
                'error': 'username_exists'
            }), 409
        
        if User.find_by_email(email):
            return jsonify({
                'message': 'El email ya está en uso',
                'error': 'email_exists'
            }), 409
        
        # Crear nuevo usuario
        password_hash = User.hash_password(password).decode('utf-8')
        user = User(username, email, password_hash)
        
        if user.save():
            logger.info(f"Usuario registrado: {username}")
            return jsonify({
                'message': 'Usuario registrado exitosamente',
                'user': user.to_dict()
            }), 201
        else:
            return jsonify({
                'message': 'Error al registrar usuario',
                'error': 'database_error'
            }), 500
            
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Iniciar sesión y obtener tokens (SQL)"""
    start_time = time.time()
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'message': 'Username y password son requeridos',
                'error': 'missing_fields'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Buscar usuario
        user = User.find_by_username(username)
        if not user:
            return jsonify({
                'message': 'Credenciales inválidas',
                'error': 'invalid_credentials'
            }), 401
        
        # Verificar contraseña
        if not user.verify_password(password):
            return jsonify({
                'message': 'Credenciales inválidas',
                'error': 'invalid_credentials'
            }), 401
        
        # Verificar si el usuario está activo
        if not user.is_active:
            return jsonify({
                'message': 'Usuario desactivado',
                'error': 'user_inactive'
            }), 401
        
        # Crear tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Registrar en bitácora
        log_token_action(user.id, 'login')
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # en milisegundos
        
        logger.info(f"Usuario {username} inició sesión (SQL) - Tiempo: {response_time:.2f}ms")
        
        return jsonify({
            'message': 'Login exitoso (SQL)',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
            'response_time_ms': round(response_time, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovar access token usando refresh token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'message': 'Usuario no válido o inactivo',
                'error': 'invalid_user'
            }), 401
        
        # Crear nuevo access token
        new_access_token = create_access_token(identity=current_user_id)
        
        # Registrar en bitácora
        log_token_action(current_user_id, 'refresh')
        
        logger.info(f"Token renovado para usuario {user.username}")
        
        return jsonify({
            'message': 'Token renovado exitosamente',
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        logger.error(f"Error en refresh: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """Cerrar sesión y revocar tokens"""
    try:
        current_user_id = get_jwt_identity()
        jti = get_jwt()['jti']
        token_type = get_jwt()['type']
        exp = get_jwt()['exp']
        
        # Convertir timestamp a datetime
        expires_at = datetime.fromtimestamp(exp)
        
        # Agregar token a la blocklist
        revoked_token = RevokedToken(jti, token_type, current_user_id, expires_at)
        revoked_token.save()
        
        # Registrar en bitácora
        log_token_action(current_user_id, 'logout', jti)
        
        logger.info(f"Usuario {current_user_id} cerró sesión")
        
        return jsonify({
            'message': 'Logout exitoso'
        }), 200
        
    except Exception as e:
        logger.error(f"Error en logout: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api/logout-all', methods=['POST'])
@jwt_required()
def logout_all():
    """Cerrar todas las sesiones del usuario"""
    try:
        current_user_id = get_jwt_identity()
        
        # Revocar todos los tokens del usuario
        RevokedToken.revoke_all_user_tokens(current_user_id)
        
        # Registrar en bitácora
        log_token_action(current_user_id, 'revoke')
        
        logger.info(f"Todas las sesiones del usuario {current_user_id} fueron cerradas")
        
        return jsonify({
            'message': 'Todas las sesiones cerradas exitosamente'
        }), 200
        
    except Exception as e:
        logger.error(f"Error en logout-all: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obtener perfil del usuario autenticado"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'message': 'Usuario no encontrado',
                'error': 'user_not_found'
            }), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo perfil: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api/audit-log', methods=['GET'])
@jwt_required()
def get_audit_log():
    """Obtener bitácora de auditoría del usuario"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        
        audit_log = TokenAudit.get_user_audit_log(current_user_id, limit)
        
        return jsonify({
            'audit_log': audit_log
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo bitácora: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api/admin/audit-log', methods=['GET'])
@jwt_required()
def get_admin_audit_log():
    """Obtener bitácora de auditoría general (admin)"""
    try:
        # En una implementación real, verificarías si el usuario es admin
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 100, type=int)
        
        audit_log = TokenAudit.get_all_audit_log(limit)
        
        return jsonify({
            'audit_log': audit_log
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo bitácora admin: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

# ==================== ENDPOINTS REDIS ====================

@app.route('/api-redis/login', methods=['POST'])
def login_redis():
    """Iniciar sesión usando Redis para almacenar estado"""
    start_time = time.time()
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'message': 'Username y password son requeridos',
                'error': 'missing_fields'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Buscar usuario (sigue usando SQL para usuarios)
        user = User.find_by_username(username)
        if not user:
            return jsonify({
                'message': 'Credenciales inválidas',
                'error': 'invalid_credentials'
            }), 401
        
        # Verificar contraseña
        if not user.verify_password(password):
            return jsonify({
                'message': 'Credenciales inválidas',
                'error': 'invalid_credentials'
            }), 401
        
        # Verificar si el usuario está activo
        if not user.is_active:
            return jsonify({
                'message': 'Usuario desactivado',
                'error': 'user_inactive'
            }), 401
        
        # Crear tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Almacenar sesión en Redis
        session_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'login_time': datetime.utcnow().isoformat()
        }
        redis_manager.store_user_session(user.id, session_data)
        
        # Registrar en bitácora (Redis)
        audit = TokenAudit(user.id, 'login')
        audit.save_redis()
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # en milisegundos
        
        logger.info(f"Usuario {username} inició sesión (Redis) - Tiempo: {response_time:.2f}ms")
        
        return jsonify({
            'message': 'Login exitoso (Redis)',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
            'response_time_ms': round(response_time, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Error en login Redis: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api-redis/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_redis():
    """Renovar access token usando Redis"""
    start_time = time.time()
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'message': 'Usuario no válido o inactivo',
                'error': 'invalid_user'
            }), 401
        
        # Crear nuevo access token
        new_access_token = create_access_token(identity=current_user_id)
        
        # Registrar en bitácora (Redis)
        audit = TokenAudit(current_user_id, 'refresh')
        audit.save_redis()
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        logger.info(f"Token renovado para usuario {user.username} (Redis) - Tiempo: {response_time:.2f}ms")
        
        return jsonify({
            'message': 'Token renovado exitosamente (Redis)',
            'access_token': new_access_token,
            'response_time_ms': round(response_time, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Error en refresh Redis: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api-redis/logout', methods=['POST'])
@jwt_required()
def logout_redis():
    """Cerrar sesión usando Redis"""
    start_time = time.time()
    try:
        current_user_id = get_jwt_identity()
        jti = get_jwt()['jti']
        token_type = get_jwt()['type']
        exp = get_jwt()['exp']
        
        # Convertir timestamp a datetime
        expires_at = datetime.fromtimestamp(exp)
        
        # Agregar token a la blocklist (Redis)
        revoked_token = RevokedToken(jti, token_type, current_user_id, expires_at)
        revoked_token.save_redis()
        
        # Eliminar sesión de Redis
        redis_manager.delete_user_session(current_user_id)
        
        # Registrar en bitácora (Redis)
        audit = TokenAudit(current_user_id, 'logout', jti)
        audit.save_redis()
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        logger.info(f"Usuario {current_user_id} cerró sesión (Redis) - Tiempo: {response_time:.2f}ms")
        
        return jsonify({
            'message': 'Logout exitoso (Redis)',
            'response_time_ms': round(response_time, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Error en logout Redis: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api-redis/logout-all', methods=['POST'])
@jwt_required()
def logout_all_redis():
    """Cerrar todas las sesiones del usuario usando Redis"""
    start_time = time.time()
    try:
        current_user_id = get_jwt_identity()
        
        # Revocar todos los tokens del usuario (Redis)
        RevokedToken.revoke_all_user_tokens_redis(current_user_id)
        
        # Eliminar sesión de Redis
        redis_manager.delete_user_session(current_user_id)
        
        # Registrar en bitácora (Redis)
        audit = TokenAudit(current_user_id, 'revoke')
        audit.save_redis()
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        logger.info(f"Todas las sesiones del usuario {current_user_id} fueron cerradas (Redis) - Tiempo: {response_time:.2f}ms")
        
        return jsonify({
            'message': 'Todas las sesiones cerradas exitosamente (Redis)',
            'response_time_ms': round(response_time, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Error en logout-all Redis: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api-redis/audit-log', methods=['GET'])
@jwt_required()
def get_audit_log_redis():
    """Obtener bitácora de auditoría del usuario desde Redis"""
    start_time = time.time()
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        
        audit_log = TokenAudit.get_user_audit_log_redis(current_user_id, limit)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        return jsonify({
            'audit_log': audit_log,
            'response_time_ms': round(response_time, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo bitácora Redis: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/api-redis/admin/audit-log', methods=['GET'])
@jwt_required()
def get_admin_audit_log_redis():
    """Obtener bitácora de auditoría general desde Redis"""
    start_time = time.time()
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 100, type=int)
        
        audit_log = TokenAudit.get_all_audit_log_redis(limit)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        return jsonify({
            'audit_log': audit_log,
            'response_time_ms': round(response_time, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo bitácora admin Redis: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

# ==================== ENDPOINT DE COMPARACIÓN ====================

@app.route('/api/performance/compare', methods=['POST'])
def compare_performance():
    """Comparar rendimiento entre SQL y Redis"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'message': 'Username y password son requeridos',
                'error': 'missing_fields'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Buscar usuario
        user = User.find_by_username(username)
        if not user or not user.verify_password(password) or not user.is_active:
            return jsonify({
                'message': 'Credenciales inválidas',
                'error': 'invalid_credentials'
            }), 401
        
        results = {
            'user': user.to_dict(),
            'comparison': {
                'sql': {},
                'redis': {}
            }
        }
        
        # Probar SQL
        sql_start = time.time()
        try:
            # Simular operaciones SQL
            access_token_sql = create_access_token(identity=user.id)
            refresh_token_sql = create_refresh_token(identity=user.id)
            
            # Registrar en bitácora SQL
            audit_sql = TokenAudit(user.id, 'login')
            audit_sql.save()
            
            sql_end = time.time()
            results['comparison']['sql'] = {
                'success': True,
                'response_time_ms': round((sql_end - sql_start) * 1000, 2),
                'access_token': access_token_sql,
                'refresh_token': refresh_token_sql
            }
        except Exception as e:
            results['comparison']['sql'] = {
                'success': False,
                'error': str(e),
                'response_time_ms': 0
            }
        
        # Probar Redis
        redis_start = time.time()
        try:
            # Simular operaciones Redis
            access_token_redis = create_access_token(identity=user.id)
            refresh_token_redis = create_refresh_token(identity=user.id)
            
            # Almacenar sesión en Redis
            session_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': datetime.utcnow().isoformat()
            }
            redis_manager.store_user_session(user.id, session_data)
            
            # Registrar en bitácora Redis
            audit_redis = TokenAudit(user.id, 'login')
            audit_redis.save_redis()
            
            redis_end = time.time()
            results['comparison']['redis'] = {
                'success': True,
                'response_time_ms': round((redis_end - redis_start) * 1000, 2),
                'access_token': access_token_redis,
                'refresh_token': refresh_token_redis
            }
        except Exception as e:
            results['comparison']['redis'] = {
                'success': False,
                'error': str(e),
                'response_time_ms': 0
            }
        
        # Calcular diferencia
        if results['comparison']['sql']['success'] and results['comparison']['redis']['success']:
            sql_time = results['comparison']['sql']['response_time_ms']
            redis_time = results['comparison']['redis']['response_time_ms']
            difference = redis_time - sql_time
            percentage = (difference / sql_time * 100) if sql_time > 0 else 0
            
            results['performance_analysis'] = {
                'faster_system': 'redis' if redis_time < sql_time else 'sql',
                'time_difference_ms': round(difference, 2),
                'percentage_difference': round(percentage, 2),
                'redis_advantage': f"Redis es {abs(percentage):.1f}% {'más rápido' if redis_time < sql_time else 'más lento'} que SQL"
            }
        
        return jsonify(results), 200
        
    except Exception as e:
        logger.error(f"Error en comparación de rendimiento: {e}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': 'internal_error'
        }), 500

@app.route('/')
def index():
    """Página principal - API Backend para cliente JavaFX"""
    return jsonify({
        'message': 'JWT Auth System API',
        'version': '1.0',
        'description': 'Backend para cliente de escritorio JavaFX',
        'endpoints': {
            'health': '/api/health',
            'register': '/api/register',
            'login_sql': '/api/login',
            'login_redis': '/api-redis/login',
            'compare': '/api/performance/compare'
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado de la aplicación"""
    try:
        # Verificar conexión a la base de datos
        db_status = 'disconnected'
        if db.connect():
            db.disconnect()
            db_status = 'connected'
        
        # Verificar conexión a Redis
        redis_status = 'disconnected'
        if redis_manager.is_connected():
            redis_status = 'connected'
        
        overall_status = 'healthy' if db_status == 'connected' and redis_status == 'connected' else 'unhealthy'
        
        return jsonify({
            'status': overall_status,
            'database': db_status,
            'redis': redis_status,
            'timestamp': datetime.utcnow().isoformat()
        }), 200 if overall_status == 'healthy' else 503
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

if __name__ == '__main__':
    # Inicializar base de datos
    logger.info("Inicializando aplicación...")
    
    if db.create_database():
        if db.connect():
            db.create_tables()
            db.disconnect()
            logger.info("Base de datos inicializada correctamente")
        else:
            logger.error("No se pudo conectar a la base de datos")
    else:
        logger.error("No se pudo crear la base de datos")
    
    # Ejecutar aplicación
    app.run(debug=Config.FLASK_DEBUG, host='0.0.0.0', port=5000)

