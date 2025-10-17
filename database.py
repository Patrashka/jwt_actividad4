import mysql.connector
from mysql.connector import Error
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establecer conexión con MariaDB"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                autocommit=True
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("Conexión a MariaDB establecida exitosamente")
            return True
        except Error as e:
            logger.error(f"Error conectando a MariaDB: {e}")
            return False
    
    def disconnect(self):
        """Cerrar conexión con la base de datos"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión a MariaDB cerrada")
    
    def execute_query(self, query, params=None):
        """Ejecutar consulta SQL"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return None
    
    def execute_insert(self, query, params=None):
        """Ejecutar inserción SQL"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params)
            return self.cursor.lastrowid
        except Error as e:
            logger.error(f"Error ejecutando inserción: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Ejecutar actualización SQL"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params)
            return self.cursor.rowcount
        except Error as e:
            logger.error(f"Error ejecutando actualización: {e}")
            return None
    
    def create_database(self):
        """Crear la base de datos si no existe"""
        try:
            # Conectar sin especificar base de datos
            connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            cursor = connection.cursor()
            
            # Crear base de datos
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
            logger.info(f"Base de datos {Config.DB_NAME} creada o ya existe")
            
            cursor.close()
            connection.close()
            return True
        except Error as e:
            logger.error(f"Error creando base de datos: {e}")
            return False
    
    def create_tables(self):
        """Crear las tablas necesarias"""
        try:
            # Tabla de usuarios
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            # Tabla de tokens revocados (blocklist)
            revoked_tokens_table = """
            CREATE TABLE IF NOT EXISTS revoked_tokens (
                id INT AUTO_INCREMENT PRIMARY KEY,
                jti VARCHAR(36) UNIQUE NOT NULL,
                token_type ENUM('access', 'refresh') NOT NULL,
                user_id INT NOT NULL,
                revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            # Tabla de auditoría de tokens
            token_audit_table = """
            CREATE TABLE IF NOT EXISTS token_audit (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                action ENUM('login', 'logout', 'refresh', 'revoke') NOT NULL,
                token_jti VARCHAR(36),
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            # Ejecutar creación de tablas
            self.execute_query(users_table)
            self.execute_query(revoked_tokens_table)
            self.execute_query(token_audit_table)
            
            logger.info("Tablas creadas exitosamente")
            return True
        except Error as e:
            logger.error(f"Error creando tablas: {e}")
            return False

# Instancia global de la base de datos
db = Database()

