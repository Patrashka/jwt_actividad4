# JWT Authentication System - Actividad 4
## Cliente JavaFX Desktop

Sistema de autenticación JWT con interfaz gráfica de escritorio desarrollada en **JavaFX**. Esta aplicación consume el backend de las actividades anteriores (Flask + SQL/Redis) y permite probar funcionalidades de health check, login, refresh, logout y comparación visual de rendimiento entre SQL y Redis.

![Java](https://img.shields.io/badge/Java-21-orange)
![JavaFX](https://img.shields.io/badge/JavaFX-21-blue)
![Maven](https://img.shields.io/badge/Maven-3.8+-red)
![License](https://img.shields.io/badge/License-Educational-green)

## 🎯 Objetivos

- ✅ Crear cliente de escritorio con **JavaFX** (Java 21)
- ✅ Consumir API JWT con endpoints SQL y Redis
- ✅ Implementar funcionalidades: Health Check, Login, Token Info, Refresh, Logout
- ✅ Comparación visual de rendimiento SQL vs Redis
- ✅ Interfaz moderna y profesional
- ✅ Manejo asíncrono de peticiones HTTP

## 🛠️ Tecnologías Utilizadas

### Backend (Flask)
- **Flask** - Framework web Python
- **Flask-JWT-Extended** - Manejo de JWT
- **MariaDB/MySQL** - Base de datos SQL
- **Redis** - Cache en memoria (con simulador alternativo)
- **Flask-CORS** - Soporte CORS

### Frontend (JavaFX)
- **Java 21** - Lenguaje de programación
- **JavaFX 21** - Framework UI
- **Maven** - Gestión de dependencias
- **Jackson** - Procesamiento JSON
- **Java HTTP Client** - Comunicación HTTP (java.net.http)

## 📋 Requisitos Previos

### Para el Backend
1. **Python 3.8+**
2. **MariaDB/MySQL Server**
3. **Redis Server** (opcional, hay simulador)

### Para el Cliente JavaFX
1. **Java 21** (JDK)
   - Descargar desde: https://www.oracle.com/java/technologies/downloads/
2. **Maven 3.8+**
   - Descargar desde: https://maven.apache.org/download.cgi
3. **Variables de entorno configuradas** (JAVA_HOME, MAVEN_HOME, PATH)

### Verificar instalación:
```bash
# Verificar Java
java -version
# Debe mostrar: java version "21.x.x"

# Verificar Maven
mvn -version
# Debe mostrar: Apache Maven 3.8.x o superior
```

## 🚀 Instalación y Configuración

### 1. Backend Flask

#### a) Crear entorno virtual
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### b) Instalar dependencias
```bash
pip install -r requirements.txt
```

#### c) Configurar base de datos
Crear archivo `.env` basado en `.env.example`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=jwt_auth_db

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=2592000

FLASK_ENV=development
FLASK_DEBUG=True
```

#### d) Iniciar servidor Flask
```bash
# Opción 1: Script automatizado (Windows)
start_windows.bat

# Opción 2: Manual
python app.py
```

El servidor Flask iniciará en: **http://localhost:5000**

### 2. Cliente JavaFX

#### a) Compilar el proyecto
```bash
mvn clean compile
```

#### b) Ejecutar la aplicación
```bash
# Opción 1: Con Maven
mvn javafx:run

# Opción 2: Script automatizado (Windows)
run_javafx.bat

# Opción 3: Con Java directamente (después de compilar)
mvn clean package
java -jar target/jwt-client-javafx-1.0.0.jar
```

## 🖥️ Interfaz de Usuario

La aplicación JavaFX cuenta con las siguientes secciones:

### 1. 🏥 Health Check
- **Verificar Estado del Servidor**
  - Comprueba si el backend Flask está activo
  - Muestra estado de conexión a MariaDB
  - Muestra estado de conexión a Redis
  - Indicadores visuales de salud (verde/rojo)

### 2. 🔑 Autenticación
- **Selector de Modo**: SQL o Redis
- **Campos de entrada**:
  - Username
  - Password
  - Email (para registro)
- **Botones**:
  - 🔓 **Login**: Iniciar sesión con SQL o Redis
  - 📝 **Registrar**: Crear nuevo usuario

### 3. 👤 Sesión Actual
- **Indicador de estado**: Autenticado / No autenticado
- **Área de información de tokens**:
  - Access Token (truncado)
  - Refresh Token (truncado)
- **Botones de sesión**:
  - 🔄 **Refresh Token**: Renovar access token
  - 👤 **Ver Perfil**: Mostrar información del usuario
  - 🔒 **Logout**: Cerrar sesión

### 4. ⚡ Comparación de Rendimiento
- **Botón de comparación**: 🔬 Comparar SQL vs Redis
- Ejecuta login simultáneamente en ambos sistemas
- Muestra resultados en ventana modal con:
  - Tiempos de respuesta de SQL y Redis
  - Sistema más rápido
  - Diferencia en ms y porcentaje
  - Análisis visual comparativo

### 5. 📋 Registro de Actividad
- **Log en tiempo real** de todas las operaciones
- Timestamps para cada evento
- Mensajes con emojis para fácil identificación:
  - ✅ Operaciones exitosas
  - ❌ Errores
  - ⏱️ Tiempos de respuesta
  - 🔬 Comparaciones
- Botón 🗑️ **Limpiar Log**

## 📊 Funcionalidades Principales

### Health Check
```java
GET /api/health
```
Verifica el estado del servidor, base de datos y Redis.

**Respuesta exitosa**:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Registro de Usuario
```java
POST /api/register
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "usuario@ejemplo.com",
  "password": "password123"
}
```

### Login (SQL)
```java
POST /api/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**Respuesta**:
```json
{
  "message": "Login exitoso (SQL)",
  "access_token": "eyJ0eXAiOiJKV1...",
  "refresh_token": "eyJ0eXAiOiJKV1...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com",
    "is_active": true
  },
  "response_time_ms": 45.23
}
```

### Login (Redis)
```java
POST /api-redis/login
```
Similar al login SQL, pero usa Redis para almacenar la sesión.

### Refresh Token
```java
POST /api/refresh
Authorization: Bearer {refresh_token}
```

### Logout
```java
POST /api/logout
Authorization: Bearer {access_token}
```

### Ver Perfil
```java
GET /api/profile
Authorization: Bearer {access_token}
```

### Comparación de Rendimiento
```java
POST /api/performance/compare
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**Respuesta**:
```json
{
  "user": {...},
  "comparison": {
    "sql": {
      "success": true,
      "response_time_ms": 45.23
    },
    "redis": {
      "success": true,
      "response_time_ms": 12.45
    }
  },
  "performance_analysis": {
    "faster_system": "redis",
    "time_difference_ms": 32.78,
    "percentage_difference": 72.47,
    "redis_advantage": "Redis es 72.5% más rápido que SQL"
  }
}
```

## 🔧 Estructura del Proyecto

```
jwt_act4/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── jwtauth/
│                   ├── JWTAuthClientApp.java      # Aplicación principal JavaFX
│                   ├── model/                     # Modelos de datos
│                   │   ├── User.java
│                   │   ├── LoginRequest.java
│                   │   ├── LoginResponse.java
│                   │   ├── RegisterRequest.java
│                   │   ├── RefreshResponse.java
│                   │   ├── HealthResponse.java
│                   │   ├── ComparisonResponse.java
│                   │   └── ErrorResponse.java
│                   └── service/                   # Servicios
│                       └── ApiClient.java         # Cliente HTTP para API
├── pom.xml                                        # Configuración Maven
├── app.py                                         # Backend Flask
├── config.py                                      # Configuración backend
├── database.py                                    # Gestión de MariaDB
├── models.py                                      # Modelos backend
├── redis_manager.py                               # Gestión de Redis
├── redis_alternative.py                           # Simulador Redis
├── requirements.txt                               # Dependencias Python
├── .env.example                                   # Plantilla de variables
├── start_windows.bat                              # Script para iniciar backend
├── run_javafx.bat                                 # Script para ejecutar JavaFX
└── README.md                                      # Este archivo
```

## 🧪 Pruebas

### Flujo de prueba recomendado:

1. **Verificar Backend**
   ```bash
   # Iniciar Flask
   python app.py
   
   # En otra terminal, probar health check
   curl http://localhost:5000/api/health
   ```

2. **Iniciar Cliente JavaFX**
   ```bash
   mvn javafx:run
   ```

3. **Probar Health Check**
   - Click en "Verificar Estado del Servidor"
   - Verificar que muestra "Estado: healthy"

4. **Registrar Usuario** (si es primera vez)
   - Ingresar username, email y password
   - Click en "Registrar"

5. **Login con SQL**
   - Seleccionar modo "SQL"
   - Ingresar credenciales (testuser / password123)
   - Click en "Login"
   - Observar tiempo de respuesta en el log

6. **Probar Operaciones de Sesión**
   - **Refresh Token**: Renovar access token
   - **Ver Perfil**: Mostrar información del usuario
   - **Logout**: Cerrar sesión

7. **Login con Redis**
   - Seleccionar modo "Redis"
   - Login nuevamente
   - Comparar tiempo de respuesta con SQL

8. **Comparación Visual**
   - Click en "Comparar SQL vs Redis"
   - Observar ventana modal con resultados
   - Verificar análisis de rendimiento

### Usuario de Prueba
- **Username**: `testuser`
- **Password**: `password123`
- **Email**: `testuser@example.com`

## 📈 Comparación SQL vs Redis

### ¿Por qué comparar?

- **SQL (MariaDB)**:
  - Almacenamiento persistente en disco
  - Operaciones de lectura/escritura más lentas
  - Ideal para datos permanentes

- **Redis**:
  - Almacenamiento en memoria RAM
  - Operaciones extremadamente rápidas
  - Ideal para cache y sesiones temporales

### Resultados Esperados

En condiciones normales, Redis es **50-80% más rápido** que SQL para operaciones de sesión:

- **SQL**: 30-60 ms
- **Redis**: 5-15 ms

La aplicación muestra esta diferencia visualmente y con métricas detalladas.

## 🐛 Solución de Problemas

### Backend no responde
```
Error: No se pudo conectar al servidor
```
**Solución**:
- Verificar que Flask esté ejecutándose en http://localhost:5000
- Comprobar que el puerto 5000 no esté ocupado
- Revisar configuración de firewall

### Error de conexión a la base de datos
```
Error conectando a MariaDB: Access denied
```
**Solución**:
- Verificar credenciales en archivo `.env`
- Asegurar que MariaDB esté ejecutándose
- Crear la base de datos si no existe: `CREATE DATABASE jwt_auth_db;`

### Redis no disponible
```
Redis no disponible, usando simulador en memoria
```
**Solución**:
- Esto es normal si Redis no está instalado
- La aplicación usará un simulador en memoria automáticamente
- Para usar Redis real: `sudo service redis-server start` (Linux)

### Error al compilar JavaFX
```
Error: JAVA_HOME not set
```
**Solución**:
```bash
# Windows
set JAVA_HOME=C:\Program Files\Java\jdk-21

# Linux/Mac
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
```

### Maven no encuentra dependencias
```bash
# Limpiar caché de Maven
mvn clean
mvn dependency:purge-local-repository
mvn clean install
```

## 📝 Características Técnicas

### Asincronía
- Todas las peticiones HTTP son **asíncronas** usando `CompletableFuture`
- La UI permanece responsiva durante las operaciones
- Callbacks en el hilo de JavaFX con `Platform.runLater()`

### Manejo de Errores
- Excepciones capturadas y mostradas al usuario
- Logs detallados de errores
- Alertas visuales con información clara

### Seguridad
- Tokens JWT almacenados en memoria (no en disco)
- Contraseñas nunca se muestran en logs
- Tokens truncados en la UI para mayor seguridad

### UI Moderna
- Diseño con colores distintivos por sección
- Emojis para mejorar UX
- Botones deshabilitados según estado de sesión
- Scroll automático en logs

## 🎓 Aprendizajes

Este proyecto demuestra:

1. **Arquitectura Cliente-Servidor**
   - Separación clara entre frontend y backend
   - Comunicación vía API REST

2. **JavaFX Moderno**
   - Uso de componentes avanzados
   - Layouts responsivos
   - Programación asíncrona

3. **Consumo de APIs REST**
   - HTTP Client de Java 11+
   - Serialización/Deserialización JSON con Jackson
   - Manejo de autenticación con Bearer tokens

4. **JWT en Aplicaciones Desktop**
   - Gestión de access y refresh tokens
   - Renovación automática de tokens
   - Logout y revocación

5. **Comparación de Tecnologías**
   - SQL vs NoSQL (Redis)
   - Métricas de rendimiento
   - Análisis visual de resultados

## 🔗 Endpoints API Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/register` | Registrar usuario |
| POST | `/api/login` | Login con SQL |
| POST | `/api-redis/login` | Login con Redis |
| POST | `/api/refresh` | Refresh token (SQL) |
| POST | `/api-redis/refresh` | Refresh token (Redis) |
| POST | `/api/logout` | Logout (SQL) |
| POST | `/api-redis/logout` | Logout (Redis) |
| GET | `/api/profile` | Ver perfil |
| POST | `/api/performance/compare` | Comparar SQL vs Redis |

## 📚 Recursos Adicionales

- [JavaFX Documentation](https://openjfx.io/)
- [Jackson Documentation](https://github.com/FasterXML/jackson)
- [Java HTTP Client Guide](https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/package-summary.html)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Redis Documentation](https://redis.io/documentation)

## 👤 Autor

Proyecto desarrollado para el curso de **Integración de Aplicaciones** - Actividad 4

## 📄 Licencia

Este proyecto es con fines educativos.

---

## 🎯 Diferencias con Actividades Anteriores

- **Actividad 1**: Backend básico SQL + Postman
- **Actividad 2**: Backend SQL + Redis + Comparación (Postman)
- **Actividad 3**: Cliente de escritorio con **Tkinter** (Python)
- **Actividad 4**: Cliente de escritorio con **JavaFX** (Java 21) ⭐

### Ventajas de JavaFX sobre Tkinter:
✅ Tipado estático y compilado  
✅ Mejor rendimiento  
✅ UI más moderna y profesional  
✅ Mejor manejo de concurrencia  
✅ Empaquetado como JAR ejecutable  
✅ Multiplataforma con JVM  

---

**¡Disfruta explorando JWT con JavaFX!** 🚀

