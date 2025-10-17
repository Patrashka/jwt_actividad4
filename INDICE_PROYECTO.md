# 📚 Índice del Proyecto - JWT Auth System (Actividad 4)

## 🎯 Descripción General

Cliente de escritorio **JavaFX** (Java 21) que consume una API REST JWT desarrollada con Flask. Permite gestionar autenticación con tokens JWT, comparar rendimiento entre SQL (MariaDB) y Redis, y visualizar toda la información en una interfaz gráfica moderna.

---

## 📁 Estructura del Proyecto

```
jwt_act4/
│
├── 📄 README.md                          # Documentación completa del proyecto
├── 📄 GUIA_RAPIDA.md                     # Guía rápida de inicio (3 pasos)
├── 📄 INSTRUCCIONES_EJECUCION.md         # Instrucciones detalladas de ejecución
├── 📄 INDICE_PROYECTO.md                 # Este archivo (navegación)
│
├── 🔧 Setup y Ejecución
│   ├── setup.bat                         # Configuración inicial automática
│   ├── run_all.bat                       # Ejecutar backend + cliente
│   ├── run_javafx.bat                    # Ejecutar solo cliente JavaFX
│   ├── start_windows.bat                 # Ejecutar solo backend Flask
│   ├── .env.example                      # Plantilla de variables de entorno
│   └── .gitignore                        # Archivos ignorados por Git
│
├── 🐍 Backend Flask
│   ├── app.py                            # Servidor Flask principal
│   ├── config.py                         # Configuración (DB, Redis, JWT)
│   ├── database.py                       # Gestión de MariaDB
│   ├── models.py                         # Modelos: User, Token, Audit
│   ├── redis_manager.py                  # Gestión de Redis
│   ├── redis_alternative.py              # Simulador Redis (fallback)
│   └── requirements.txt                  # Dependencias Python
│
└── ☕ Cliente JavaFX
    ├── pom.xml                           # Configuración Maven
    └── src/main/java/com/jwtauth/
        ├── JWTAuthClientApp.java         # Aplicación principal JavaFX
        ├── model/                        # Modelos de datos
        │   ├── User.java                 # Usuario
        │   ├── LoginRequest.java         # Request de login
        │   ├── LoginResponse.java        # Response de login
        │   ├── RegisterRequest.java      # Request de registro
        │   ├── RefreshResponse.java      # Response de refresh
        │   ├── HealthResponse.java       # Response de health
        │   ├── ComparisonResponse.java   # Response de comparación
        │   └── ErrorResponse.java        # Response de error
        └── service/
            └── ApiClient.java            # Cliente HTTP para API REST
```

---

## 📖 Documentación Principal

### 1. README.md
**📄 Documentación completa del proyecto**

Contenido:
- ✅ Objetivos del proyecto
- ✅ Tecnologías utilizadas
- ✅ Requisitos previos
- ✅ Instalación detallada paso a paso
- ✅ Descripción de la interfaz de usuario
- ✅ Funcionalidades principales
- ✅ Endpoints de la API
- ✅ Estructura del proyecto
- ✅ Comparación SQL vs Redis
- ✅ Solución de problemas
- ✅ Características técnicas
- ✅ Recursos adicionales

**Lee primero:** `README.md`

---

### 2. GUIA_RAPIDA.md
**⚡ Inicio rápido en 3 pasos**

Contenido:
- 🚀 Configuración inicial
- 🚀 Ejecución rápida
- 🚀 Credenciales de prueba
- 🚀 Flujo de uso básico
- 🚀 Solución rápida de problemas

**Para empezar rápido:** `GUIA_RAPIDA.md`

---

### 3. INSTRUCCIONES_EJECUCION.md
**🔧 Instrucciones detalladas de ejecución**

Contenido:
- 📋 Métodos de ejecución (automático y manual)
- 📋 Estructura de archivos
- 📋 Flujo de uso completo
- 📋 Lista de endpoints
- 📋 Troubleshooting detallado
- 📋 Checklist de verificación

**Para ejecutar correctamente:** `INSTRUCCIONES_EJECUCION.md`

---

## 🚀 Scripts de Ejecución

### setup.bat
**Configuración inicial del proyecto**

Acciones:
- ✅ Verifica Python, Java, Maven
- ✅ Crea entorno virtual Python
- ✅ Instala dependencias Python
- ✅ Crea archivo .env

**Ejecutar una vez:** `setup.bat`

---

### run_all.bat
**Ejecuta backend y cliente automáticamente**

Acciones:
- 🚀 Inicia backend Flask en ventana nueva
- 🚀 Espera 5 segundos
- 🚀 Inicia cliente JavaFX

**Recomendado para uso normal:** `run_all.bat`

---

### run_javafx.bat
**Ejecuta solo el cliente JavaFX**

Acciones:
- ☕ Verifica Maven y Java
- ☕ Compila el proyecto
- ☕ Ejecuta la aplicación JavaFX

**Solo si backend ya está corriendo:** `run_javafx.bat`

---

### start_windows.bat
**Ejecuta solo el backend Flask**

Acciones:
- 🐍 Activa entorno virtual
- 🐍 Instala dependencias si es necesario
- 🐍 Verifica archivo .env
- 🐍 Inicia servidor Flask

**Solo si quieres backend separado:** `start_windows.bat`

---

## 🎓 Archivos de Código

### Backend (Flask)

#### app.py
**Servidor Flask principal con todos los endpoints**

Endpoints implementados:
- `GET /api/health` - Health check
- `POST /api/register` - Registrar usuario
- `POST /api/login` - Login con SQL
- `POST /api-redis/login` - Login con Redis
- `POST /api/refresh` - Refresh token (SQL)
- `POST /api-redis/refresh` - Refresh token (Redis)
- `POST /api/logout` - Logout (SQL)
- `POST /api-redis/logout` - Logout (Redis)
- `GET /api/profile` - Ver perfil
- `POST /api/performance/compare` - Comparar SQL vs Redis

---

#### config.py
**Configuración centralizada**

Variables:
- DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
- REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
- JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES

---

#### database.py
**Gestión de conexión a MariaDB**

Funciones:
- `connect()` - Conectar a la base de datos
- `disconnect()` - Desconectar
- `execute_query()` - Ejecutar consultas SELECT
- `execute_insert()` - Ejecutar INSERT
- `execute_update()` - Ejecutar UPDATE
- `create_database()` - Crear base de datos
- `create_tables()` - Crear tablas

---

#### models.py
**Modelos de datos del backend**

Clases:
- `User` - Modelo de usuario con hash de password
- `RevokedToken` - Tokens revocados (blocklist)
- `TokenAudit` - Auditoría de acciones con tokens

---

#### redis_manager.py
**Gestión de Redis con fallback**

Funcionalidad:
- Conectar a Redis (o simulador)
- Gestión de tokens revocados
- Almacenamiento de sesiones
- Logs de auditoría

---

#### redis_alternative.py
**Simulador Redis en memoria**

Usado cuando Redis no está disponible. Implementa:
- `setex()` - Set con TTL
- `get()` - Get valor
- `delete()` - Delete clave
- `keys()` - Buscar claves
- `lpush()`, `lrange()` - Listas

---

### Frontend (JavaFX)

#### JWTAuthClientApp.java
**Aplicación principal JavaFX**

Secciones de UI:
- 🏥 Health Check
- 🔑 Autenticación (Login/Register)
- 👤 Sesión Actual (Tokens, Perfil, Logout)
- ⚡ Comparación de Rendimiento
- 📋 Registro de Actividad (Logs)

Funcionalidades:
- Interfaz gráfica moderna con JavaFX
- Manejo asíncrono con CompletableFuture
- Actualización de UI en tiempo real
- Ventanas modales para comparaciones
- Logs detallados con timestamps

---

#### ApiClient.java
**Cliente HTTP para consumir la API**

Métodos:
- `checkHealth()` - Health check
- `register()` - Registrar usuario
- `login()` / `loginRedis()` - Login
- `refreshToken()` / `refreshTokenRedis()` - Refresh
- `logout()` / `logoutRedis()` - Logout
- `getProfile()` - Ver perfil
- `comparePerformance()` - Comparar SQL vs Redis

Tecnología:
- Java HTTP Client (java.net.http)
- Jackson para JSON
- CompletableFuture para asincronía

---

#### Modelos (model/)

**Clases Java para serialización JSON:**
- `User` - Usuario
- `LoginRequest` - Petición de login
- `LoginResponse` - Respuesta de login
- `RegisterRequest` - Petición de registro
- `RefreshResponse` - Respuesta de refresh
- `HealthResponse` - Respuesta de health
- `ComparisonResponse` - Respuesta de comparación
- `ErrorResponse` - Respuesta de error

---

## 📊 Flujo de Datos

```
┌─────────────────┐
│  Cliente JavaFX │
│   (Frontend)    │
└────────┬────────┘
         │ HTTP Request (JSON)
         │ Authorization: Bearer {token}
         ↓
┌─────────────────┐
│   Flask Server  │
│    (Backend)    │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐  ┌────────┐
│ MariaDB│  │ Redis  │
│  (SQL) │  │(Cache) │
└────────┘  └────────┘
```

---

## 🎯 Casos de Uso

### Caso 1: Login con SQL
```
Usuario ingresa credenciales
  → Cliente JavaFX envía POST /api/login
    → Flask valida usuario en MariaDB
      → Genera JWT tokens
        → Guarda auditoría en SQL
          → Retorna tokens al cliente
            → Cliente guarda tokens en memoria
```

### Caso 2: Login con Redis
```
Usuario ingresa credenciales
  → Cliente JavaFX envía POST /api-redis/login
    → Flask valida usuario en MariaDB
      → Genera JWT tokens
        → Guarda sesión en Redis
          → Guarda auditoría en Redis
            → Retorna tokens al cliente
              → Cliente guarda tokens en memoria
```

### Caso 3: Comparación de Rendimiento
```
Usuario hace click en "Comparar"
  → Cliente envía POST /api/performance/compare
    → Backend ejecuta operaciones en paralelo:
        ├─ Login SQL + Auditoría SQL
        └─ Login Redis + Auditoría Redis
      → Mide tiempos de cada uno
        → Calcula diferencias y porcentajes
          → Retorna análisis completo
            → Cliente muestra ventana modal con resultados
```

---

## 💡 Próximos Pasos

### Para Desarrollo
1. ✅ Implementar más endpoints (CRUD completo)
2. ✅ Agregar roles y permisos
3. ✅ Implementar paginación
4. ✅ Agregar filtros y búsqueda

### Para Producción
1. ✅ Configurar HTTPS
2. ✅ Usar base de datos en servidor
3. ✅ Configurar Redis en servidor
4. ✅ Empaquetar JavaFX como ejecutable
5. ✅ Agregar logging avanzado

---

## 📞 Soporte

Para dudas o problemas:
1. Consulta `README.md` - Documentación completa
2. Consulta `INSTRUCCIONES_EJECUCION.md` - Troubleshooting
3. Revisa los logs en la aplicación JavaFX

---

## ✅ Checklist de Archivos

### Documentación
- [x] README.md
- [x] GUIA_RAPIDA.md
- [x] INSTRUCCIONES_EJECUCION.md
- [x] INDICE_PROYECTO.md

### Scripts
- [x] setup.bat
- [x] run_all.bat
- [x] run_javafx.bat
- [x] start_windows.bat

### Backend
- [x] app.py
- [x] config.py
- [x] database.py
- [x] models.py
- [x] redis_manager.py
- [x] redis_alternative.py
- [x] requirements.txt

### Frontend
- [x] pom.xml
- [x] JWTAuthClientApp.java
- [x] ApiClient.java
- [x] Todos los modelos (8 clases)

### Configuración
- [x] .env.example
- [x] .gitignore

---

**Proyecto completo y funcional** ✅

Desarrollado con ❤️ para Actividad 4 - Integración de Aplicaciones

