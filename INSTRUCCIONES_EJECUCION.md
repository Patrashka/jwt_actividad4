# 📖 Instrucciones de Ejecución - JWT Auth System (Actividad 4)

## ⚡ Ejecución Rápida (Recomendado)

### Método 1: Script Automático (Todo en Uno)

```bash
# 1. Configuración inicial (solo primera vez)
setup.bat

# 2. Ejecutar backend y cliente
run_all.bat
```

**¡Eso es todo!** El script iniciará automáticamente el backend Flask y el cliente JavaFX.

---

## 🔧 Ejecución Manual (Paso a Paso)

### Prerequisitos

✅ **Python 3.8+** instalado  
✅ **Java 21** instalado  
✅ **Maven 3.8+** instalado  
✅ **MariaDB/MySQL** ejecutándose  
✅ **Redis** (opcional)  

---

### Backend Flask

#### Terminal 1: Iniciar Backend

```bash
# 1. Activar entorno virtual
venv\Scripts\activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Configurar .env (primera vez)
# Editar .env con credenciales de base de datos

# 4. Iniciar servidor
python app.py
```

**Verificar que el backend esté corriendo:**
```bash
curl http://localhost:5000/api/health
```

Debe responder:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "..."
}
```

---

### Cliente JavaFX

#### Terminal 2: Ejecutar Cliente

```bash
# Opción A: Con Maven (Recomendado)
mvn javafx:run

# Opción B: Compilar y ejecutar JAR
mvn clean package
java -jar target/jwt-client-javafx-1.0.0.jar

# Opción C: Script automatizado
run_javafx.bat
```

---

## 🗂️ Estructura de Archivos

```
jwt_act4/
│
├── 📁 Backend (Flask)
│   ├── app.py                    # Servidor Flask
│   ├── config.py                 # Configuración
│   ├── database.py               # Gestión DB
│   ├── models.py                 # Modelos
│   ├── redis_manager.py          # Redis
│   ├── redis_alternative.py      # Simulador Redis
│   ├── requirements.txt          # Dependencias Python
│   └── .env                      # Variables de entorno
│
├── 📁 Frontend (JavaFX)
│   ├── src/main/java/com/jwtauth/
│   │   ├── JWTAuthClientApp.java # App principal
│   │   ├── model/                # Modelos
│   │   └── service/              # Servicios
│   └── pom.xml                   # Maven config
│
└── 📁 Scripts
    ├── setup.bat                 # Setup inicial
    ├── run_all.bat               # Ejecutar todo
    ├── run_javafx.bat            # Solo JavaFX
    └── start_windows.bat         # Solo backend
```

---

## 🎯 Flujo de Uso

### 1. Verificar Salud del Sistema
```
Aplicación JavaFX > Health Check
→ Click "Verificar Estado del Servidor"
✓ Debe mostrar: Status: healthy
```

### 2. Registrar Usuario (Primera vez)
```
Sección: Autenticación
→ Username: testuser
→ Email: testuser@example.com
→ Password: password123
→ Click "Registrar"
✓ Mensaje: "Usuario registrado exitosamente"
```

### 3. Iniciar Sesión (SQL)
```
→ Modo: SQL
→ Username: testuser
→ Password: password123
→ Click "Login"
✓ Sesión iniciada, tokens guardados
```

### 4. Operaciones de Sesión
```
→ Click "Refresh Token" - Renueva access token
→ Click "Ver Perfil" - Muestra información del usuario
→ Click "Logout" - Cierra sesión
```

### 5. Iniciar Sesión (Redis)
```
→ Modo: Redis
→ Username: testuser
→ Password: password123
→ Click "Login"
✓ Observar tiempo de respuesta (más rápido que SQL)
```

### 6. Comparar Rendimiento
```
→ Click "Comparar SQL vs Redis"
✓ Ventana modal con resultados:
  - Tiempo SQL: ~45 ms
  - Tiempo Redis: ~12 ms
  - Análisis: "Redis es 72% más rápido"
```

---

## 📊 Endpoints Utilizados

| Funcionalidad | Endpoint | Método | Requiere Auth |
|---------------|----------|--------|---------------|
| Health Check | `/api/health` | GET | No |
| Registrar | `/api/register` | POST | No |
| Login SQL | `/api/login` | POST | No |
| Login Redis | `/api-redis/login` | POST | No |
| Refresh SQL | `/api/refresh` | POST | Sí (refresh token) |
| Refresh Redis | `/api-redis/refresh` | POST | Sí (refresh token) |
| Logout SQL | `/api/logout` | POST | Sí (access token) |
| Logout Redis | `/api-redis/logout` | POST | Sí (access token) |
| Ver Perfil | `/api/profile` | GET | Sí (access token) |
| Comparar | `/api/performance/compare` | POST | No |

---

## 🐛 Troubleshooting

### ❌ Backend no responde

**Síntoma:**
```
Error: No se pudo conectar al servidor
```

**Solución:**
```bash
# Verificar que Flask esté corriendo
curl http://localhost:5000/api/health

# Si no responde, verificar puerto
netstat -an | findstr :5000

# Reiniciar backend
python app.py
```

---

### ❌ Error de Base de Datos

**Síntoma:**
```
Error conectando a MariaDB: Access denied
```

**Solución:**
```bash
# 1. Verificar credenciales en .env
DB_USER=root
DB_PASSWORD=tu_password_correcta

# 2. Crear base de datos si no existe
mysql -u root -p
CREATE DATABASE jwt_auth_db;
exit;

# 3. Reiniciar backend
python app.py
```

---

### ❌ Maven no compila

**Síntoma:**
```
Error: JAVA_HOME not set
```

**Solución:**
```bash
# Windows - PowerShell (como administrador)
[System.Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Java\jdk-21", "Machine")

# Verificar
echo %JAVA_HOME%

# Reiniciar terminal y probar
mvn -version
```

---

### ❌ JavaFX no inicia

**Síntoma:**
```
Error: JavaFX runtime components are missing
```

**Solución:**
```bash
# Limpiar y recompilar
mvn clean
mvn clean install
mvn javafx:run
```

---

### ⚠️ Redis no disponible

**Síntoma:**
```
Redis no disponible, usando simulador en memoria
```

**Solución:**
```
✓ Esto es NORMAL si no tienes Redis instalado
✓ El sistema usa un simulador automáticamente
✓ La aplicación funcionará perfectamente

Opcional - Instalar Redis:
# Windows: https://github.com/microsoftarchive/redis/releases
# Linux: sudo apt install redis-server
# Mac: brew install redis
```

---

## 📝 Notas Importantes

### Tokens JWT

- **Access Token**: Válido por 15 minutos
- **Refresh Token**: Válido por 30 días
- Los tokens se almacenan solo en memoria (no en disco)
- Se eliminan automáticamente al cerrar la aplicación

### Modos de Operación

**SQL (MariaDB):**
- ✅ Almacenamiento persistente
- ✅ Ideal para producción
- ⏱️ Más lento (~30-60 ms)

**Redis:**
- ✅ Almacenamiento en memoria
- ✅ Ideal para cache/sesiones
- ⚡ Muy rápido (~5-15 ms)

### Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Tokens firmados con JWT
- ✅ CORS configurado para seguridad
- ✅ Tokens revocables (blocklist)

---

## 🎓 Recursos

- **Documentación Completa**: `README.md`
- **Guía Rápida**: `GUIA_RAPIDA.md`
- **Backend Flask**: `app.py`
- **Cliente JavaFX**: `src/main/java/com/jwtauth/JWTAuthClientApp.java`

---

## ✅ Checklist de Verificación

Antes de ejecutar, verifica:

- [ ] Python 3.8+ instalado
- [ ] Java 21 instalado
- [ ] Maven 3.8+ instalado
- [ ] MariaDB/MySQL corriendo
- [ ] Archivo `.env` configurado
- [ ] Puerto 5000 disponible
- [ ] Variables de entorno configuradas (JAVA_HOME, PATH)

---

## 💡 Tips

1. **Usa el log** - Toda la actividad se registra en tiempo real
2. **Prueba ambos modos** - Compara SQL vs Redis
3. **Observa los tiempos** - Redis es mucho más rápido
4. **Usa Health Check** - Verifica conexiones antes de operar

---

**¡Todo listo para ejecutar!** 🚀

Si tienes problemas, consulta la sección de Troubleshooting o el README.md completo.

