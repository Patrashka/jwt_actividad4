import bcrypt
import uuid
from datetime import datetime, timedelta
from database import db
from redis_manager import redis_manager
import logging

logger = logging.getLogger(__name__)

class User:
    def __init__(self, username, email, password_hash=None, is_active=True, user_id=None):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
    
    @staticmethod
    def hash_password(password):
        """Hashear contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password):
        """Verificar contraseña"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def save(self):
        """Guardar usuario en la base de datos"""
        query = """
        INSERT INTO users (username, email, password_hash, is_active)
        VALUES (%s, %s, %s, %s)
        """
        params = (self.username, self.email, self.password_hash, self.is_active)
        user_id = db.execute_insert(query, params)
        if user_id:
            self.id = user_id
            return True
        return False
    
    @staticmethod
    def find_by_username(username):
        """Buscar usuario por nombre de usuario"""
        query = "SELECT * FROM users WHERE username = %s"
        result = db.execute_query(query, (username,))
        if result:
            user_data = result[0]
            return User(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                is_active=user_data['is_active']
            )
        return None
    
    @staticmethod
    def find_by_email(email):
        """Buscar usuario por email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = db.execute_query(query, (email,))
        if result:
            user_data = result[0]
            return User(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                is_active=user_data['is_active']
            )
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """Buscar usuario por ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = db.execute_query(query, (user_id,))
        if result:
            user_data = result[0]
            return User(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                is_active=user_data['is_active']
            )
        return None
    
    def to_dict(self):
        """Convertir usuario a diccionario (sin password_hash)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active
        }

class RevokedToken:
    def __init__(self, jti, token_type, user_id, expires_at, revoked_at=None):
        self.jti = jti
        self.token_type = token_type
        self.user_id = user_id
        self.expires_at = expires_at
        self.revoked_at = revoked_at
    
    def save(self):
        """Guardar token revocado en la blocklist (SQL)"""
        query = """
        INSERT INTO revoked_tokens (jti, token_type, user_id, expires_at)
        VALUES (%s, %s, %s, %s)
        """
        params = (self.jti, self.token_type, self.user_id, self.expires_at)
        return db.execute_insert(query, params) is not None
    
    def save_redis(self):
        """Guardar token revocado en Redis"""
        return redis_manager.set_token_revoked(
            self.jti, self.token_type, self.user_id, self.expires_at
        )
    
    @staticmethod
    def is_revoked(jti):
        """Verificar si un token está revocado (SQL)"""
        query = "SELECT id FROM revoked_tokens WHERE jti = %s"
        result = db.execute_query(query, (jti,))
        return len(result) > 0
    
    @staticmethod
    def is_revoked_redis(jti):
        """Verificar si un token está revocado (Redis)"""
        return redis_manager.is_token_revoked(jti)
    
    @staticmethod
    def revoke_all_user_tokens(user_id):
        """Revocar todos los tokens de un usuario (SQL)"""
        # Esta función se implementaría para revocar todos los tokens activos de un usuario
        # Por simplicidad, aquí solo registramos la acción
        logger.info(f"Revocando todos los tokens del usuario {user_id}")
        return True
    
    @staticmethod
    def revoke_all_user_tokens_redis(user_id):
        """Revocar todos los tokens de un usuario (Redis)"""
        return redis_manager.revoke_all_user_tokens(user_id)

class TokenAudit:
    def __init__(self, user_id, action, token_jti=None, ip_address=None, user_agent=None):
        self.user_id = user_id
        self.action = action
        self.token_jti = token_jti
        self.ip_address = ip_address
        self.user_agent = user_agent
    
    def save(self):
        """Guardar entrada de auditoría (SQL)"""
        query = """
        INSERT INTO token_audit (user_id, action, token_jti, ip_address, user_agent)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (self.user_id, self.action, self.token_jti, self.ip_address, self.user_agent)
        return db.execute_insert(query, params) is not None
    
    def save_redis(self):
        """Guardar entrada de auditoría (Redis)"""
        return redis_manager.log_audit_action(
            self.user_id, self.action, self.token_jti, self.ip_address, self.user_agent
        )
    
    @staticmethod
    def get_user_audit_log(user_id, limit=50):
        """Obtener bitácora de auditoría de un usuario (SQL)"""
        query = """
        SELECT * FROM token_audit 
        WHERE user_id = %s 
        ORDER BY created_at DESC 
        LIMIT %s
        """
        return db.execute_query(query, (user_id, limit))
    
    @staticmethod
    def get_user_audit_log_redis(user_id, limit=50):
        """Obtener bitácora de auditoría de un usuario (Redis)"""
        return redis_manager.get_user_audit_log(user_id, limit)
    
    @staticmethod
    def get_all_audit_log(limit=100):
        """Obtener bitácora de auditoría general (SQL)"""
        query = """
        SELECT ta.*, u.username 
        FROM token_audit ta
        JOIN users u ON ta.user_id = u.id
        ORDER BY ta.created_at DESC 
        LIMIT %s
        """
        return db.execute_query(query, (limit,))
    
    @staticmethod
    def get_all_audit_log_redis(limit=100):
        """Obtener bitácora de auditoría general (Redis)"""
        return redis_manager.get_all_audit_log(limit)

