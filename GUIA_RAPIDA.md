# 🚀 Guía Rápida - JWT Auth Client JavaFX

## Inicio Rápido (3 pasos)

### 1️⃣ Configuración Inicial (Solo primera vez)

```bash
# Ejecutar script de setup
setup.bat
```

Esto instalará todas las dependencias necesarias automáticamente.

### 2️⃣ Configurar Base de Datos

Editar el archivo `.env` con tus credenciales:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=TU_PASSWORD_AQUI
DB_NAME=jwt_auth_db
```

### 3️⃣ Ejecutar la Aplicación

```bash
# Opción A: Ejecutar todo automáticamente
run_all.bat

# Opción B: Ejecutar manualmente
# Terminal 1 - Backend:
start_windows.bat

# Terminal 2 - Cliente JavaFX:
run_javafx.bat
```

---

## 📝 Credenciales de Prueba

**Usuario de prueba predefinido:**
- Username: `testuser`
- Password: `password123`

**Primero debes registrarlo:**
1. Abre la aplicación JavaFX
2. Completa los campos:
   - Username: `testuser`
   - Password: `password123`
   - Email: `testuser@example.com`
3. Click en **"Registrar"**
4. Ahora puedes hacer login

---

## 🎮 Flujo de Uso

### 1. Health Check
```
Click en "Verificar Estado del Servidor"
→ Debe mostrar: Estado: healthy, DB: connected, Redis: connected
```

### 2. Login
```
Modo: SQL o Redis
Username: testuser
Password: password123
→ Click en "Login"
```

### 3. Operaciones de Sesión
```
✓ Refresh Token - Renueva el access token
✓ Ver Perfil - Muestra información del usuario
✓ Logout - Cierra la sesión
```

### 4. Comparación de Rendimiento
```
Click en "Comparar SQL vs Redis"
→ Ventana modal mostrará tiempos y análisis
```

---

## ⚠️ Solución Rápida de Problemas

### Backend no responde
```bash
# Verificar que Flask esté corriendo
curl http://localhost:5000/api/health

# Si no responde, iniciar backend
start_windows.bat
```

### Error de base de datos
```sql
-- Crear la base de datos manualmente
mysql -u root -p
CREATE DATABASE jwt_auth_db;
exit;
```

### Maven no funciona
```bash
# Verificar instalación
mvn -version

# Si no está instalado, descargar de:
# https://maven.apache.org/download.cgi
```

### Java no funciona
```bash
# Verificar instalación
java -version

# Debe mostrar Java 21
# Si no, descargar de:
# https://www.oracle.com/java/technologies/downloads/
```

---

## 📊 Endpoints Principales

| Acción | Endpoint | Método |
|--------|----------|--------|
| Health Check | `/api/health` | GET |
| Login SQL | `/api/login` | POST |
| Login Redis | `/api-redis/login` | POST |
| Refresh | `/api/refresh` | POST |
| Logout | `/api/logout` | POST |
| Perfil | `/api/profile` | GET |
| Comparar | `/api/performance/compare` | POST |

---

## 🎯 Características Principales

✅ **Health Check** - Verifica estado del servidor  
✅ **Autenticación JWT** - Login con SQL o Redis  
✅ **Gestión de Tokens** - Access y Refresh tokens  
✅ **Perfil de Usuario** - Información del usuario autenticado  
✅ **Comparación Visual** - SQL vs Redis con métricas  
✅ **Logs en Tiempo Real** - Actividad detallada  

---

## 💡 Tips

1. **Mantén el backend corriendo** mientras usas el cliente JavaFX
2. **Prueba ambos modos** (SQL y Redis) para ver diferencias de rendimiento
3. **Usa el log** para ver detalles de cada operación
4. **Compara tiempos** entre SQL y Redis con el botón de comparación

---

## 📚 Más Información

Ver `README.md` para documentación completa.

---

**¡Listo para usar!** 🎉

