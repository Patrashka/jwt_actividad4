# 🐳 Docker Setup - JWT Auth System

## 📦 Configuración con Docker

Esta guía te permite ejecutar **TODO el proyecto con un solo comando** usando Docker Compose.

---

## 🎯 Servicios Incluidos

El `docker-compose.yml` incluye:

1. **MariaDB** - Base de datos MySQL (puerto 3306)
2. **Redis** - Cache en memoria (puerto 6379)
3. **Backend Flask** - API REST JWT (puerto 5000)
4. **JavaFX Client** - Cliente con Java 21 y Maven (opcional)

---

## 🚀 Inicio Rápido (3 comandos)

```bash
# 1. Construir las imágenes
docker-compose build

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Ver logs (opcional)
docker-compose logs -f backend
```

**¡Eso es todo!** El backend estará disponible en: http://localhost:5000

---

## 📋 Comandos Principales

### Iniciar servicios
```bash
# Iniciar todos los servicios
docker-compose up -d

# Iniciar solo backend (sin JavaFX)
docker-compose up -d mariadb redis backend

# Ver logs en tiempo real
docker-compose logs -f backend
```

### Detener servicios
```bash
# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (BORRA DATOS)
docker-compose down -v
```

### Ver estado
```bash
# Ver servicios en ejecución
docker-compose ps

# Ver logs de un servicio específico
docker-compose logs backend
docker-compose logs mariadb
docker-compose logs redis
```

### Reconstruir después de cambios
```bash
# Reconstruir imagen del backend
docker-compose build backend

# Reconstruir y reiniciar
docker-compose up -d --build backend
```

---

## 🔍 Verificar que todo funciona

### 1. Health Check del Backend
```bash
# Opción 1: Con curl
curl http://localhost:5000/api/health

# Opción 2: En el navegador
# Abrir: http://localhost:5000/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Verificar MariaDB
```bash
# Conectar a MariaDB
docker exec -it jwt-mariadb mysql -u root -prootpassword jwt_auth_db

# Ver tablas
SHOW TABLES;

# Salir
exit
```

### 3. Verificar Redis
```bash
# Conectar a Redis
docker exec -it jwt-redis redis-cli

# Probar conexión
PING
# Debe responder: PONG

# Ver claves
KEYS *

# Salir
exit
```

---

## 🧪 Probar la API

### Registrar Usuario
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Login (SQL)
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

**Guardar el access_token de la respuesta para los siguientes comandos:**

### Ver Perfil (requiere token)
```bash
# Reemplaza TOKEN con tu access_token
curl http://localhost:5000/api/profile \
  -H "Authorization: Bearer TOKEN"
```

### Comparar SQL vs Redis
```bash
curl -X POST http://localhost:5000/api/performance/compare \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

---

## 🛠️ Cliente JavaFX con Docker

### Opción 1: Compilar dentro del contenedor
```bash
# Iniciar el contenedor de desarrollo
docker-compose --profile dev up javafx-client

# Compilar el proyecto
docker-compose exec javafx-client mvn clean package
```

### Opción 2: Usar Docker solo para construir
```bash
# Construir la imagen
docker-compose build javafx-client

# Copiar el JAR compilado al host
docker create --name temp-javafx jwt-javafx-client
docker cp temp-javafx:/app/target/jwt-client-javafx-1.0.0.jar ./
docker rm temp-javafx

# Ejecutar localmente (requiere Java 21)
java -jar jwt-client-javafx-1.0.0.jar
```

### Opción 3: Ejecutar GUI desde Docker (Linux/Mac con X11)
```bash
# En Linux/Mac con X11
xhost +local:docker
docker-compose --profile dev up javafx-client
```

**Nota:** En Windows, ejecutar GUI desde Docker es complicado. Es mejor:
1. Usar Docker solo para el backend
2. Ejecutar el cliente JavaFX localmente (cuando tengas Maven/Java 21)

---

## 📊 Estructura de Volúmenes

Los datos se guardan en volúmenes Docker:

```bash
# Ver volúmenes
docker volume ls | grep jwt

# Inspeccionar volumen
docker volume inspect jwt_act4_mariadb_data

# Backup de MariaDB
docker exec jwt-mariadb mysqldump -u root -prootpassword jwt_auth_db > backup.sql

# Restaurar desde backup
docker exec -i jwt-mariadb mysql -u root -prootpassword jwt_auth_db < backup.sql
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear archivo `.env.docker` para personalizar:

```env
# Base de Datos
DB_PASSWORD=tu_password_seguro
DB_USER_PASSWORD=password_del_usuario

# Redis
REDIS_PASSWORD=redis_password_seguro

# JWT
JWT_SECRET_KEY=tu-clave-secreta-super-segura-aqui
```

Usar con:
```bash
docker-compose --env-file .env.docker up -d
```

### Modo Producción

```bash
# Usar configuración de producción
docker-compose -f docker-compose.prod.yml up -d

# Con variables de entorno
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
```

---

## 🐛 Troubleshooting

### Backend no inicia
```bash
# Ver logs detallados
docker-compose logs backend

# Verificar que MariaDB esté listo
docker-compose ps mariadb

# Reiniciar backend
docker-compose restart backend
```

### Error de conexión a la base de datos
```bash
# Verificar que MariaDB esté saludable
docker-compose ps

# Entrar al contenedor del backend
docker-compose exec backend bash

# Probar conexión desde dentro
apt-get update && apt-get install -y mysql-client
mysql -h mariadb -u root -prootpassword -e "SHOW DATABASES;"
```

### Puerto ocupado
```bash
# Verificar qué está usando el puerto 5000
netstat -ano | findstr :5000

# Cambiar puerto en docker-compose.yml
# En la sección backend > ports, cambiar:
# - "5001:5000"  # Usar puerto 5001 en el host
```

### Redis no conecta
```bash
# Verificar estado de Redis
docker-compose logs redis

# Reiniciar Redis
docker-compose restart redis

# Probar conexión
docker exec -it jwt-redis redis-cli ping
```

### Limpiar todo y empezar de nuevo
```bash
# ADVERTENCIA: Esto borra todos los datos
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## 📦 Exportar/Importar Datos

### Exportar
```bash
# Exportar base de datos
docker exec jwt-mariadb mysqldump -u root -prootpassword jwt_auth_db > jwt_backup.sql

# Exportar datos de Redis
docker exec jwt-redis redis-cli --rdb /data/dump.rdb
docker cp jwt-redis:/data/dump.rdb ./redis_backup.rdb
```

### Importar
```bash
# Importar base de datos
docker exec -i jwt-mariadb mysql -u root -prootpassword jwt_auth_db < jwt_backup.sql

# Importar datos de Redis
docker cp ./redis_backup.rdb jwt-redis:/data/dump.rdb
docker-compose restart redis
```

---

## 🌐 Acceso desde Otras Máquinas

Si quieres que otros accedan a tu API:

1. **Encuentra tu IP local:**
```bash
ipconfig  # Windows
ip addr   # Linux
```

2. **Accede desde otra máquina:**
```
http://TU_IP_LOCAL:5000/api/health
```

3. **Configurar firewall (si es necesario):**
```bash
# Windows: Permitir puerto 5000
netsh advfirewall firewall add rule name="Flask JWT" dir=in action=allow protocol=TCP localport=5000
```

---

## 📝 Comandos Útiles

```bash
# Ver recursos usados
docker stats

# Limpiar imágenes no usadas
docker image prune -a

# Ver redes
docker network ls

# Inspeccionar red
docker network inspect jwt_act4_jwt-network

# Ejecutar comando en contenedor
docker-compose exec backend python -c "print('Hello from container')"

# Abrir shell en contenedor
docker-compose exec backend bash
docker-compose exec mariadb bash
docker-compose exec redis sh
```

---

## ✅ Checklist de Verificación

- [ ] Docker instalado (`docker --version`)
- [ ] Docker Compose instalado (`docker-compose --version`)
- [ ] Puertos libres (5000, 3306, 6379)
- [ ] Suficiente espacio en disco (mínimo 2GB)
- [ ] Todos los servicios en estado "healthy" (`docker-compose ps`)
- [ ] Health check responde OK (`curl http://localhost:5000/api/health`)

---

## 🎓 Ventajas de usar Docker

✅ **No necesitas instalar:**
- Python, pip, venv
- MariaDB/MySQL
- Redis
- Java 21 (para compilar)
- Maven

✅ **Entorno consistente** en cualquier máquina

✅ **Fácil de limpiar** - elimina todo con `docker-compose down -v`

✅ **Aislamiento** - no interfiere con otras aplicaciones

✅ **Reproducible** - mismo resultado en dev, test, prod

---

## 🚀 Próximos Pasos

1. **Desarrollo:** Modifica código, reconstruye con `docker-compose up -d --build`
2. **Testing:** Usa Postman o curl para probar endpoints
3. **Producción:** Usa `docker-compose.prod.yml` con variables seguras
4. **Monitoreo:** Agrega Grafana/Prometheus para métricas

---

**¡Todo listo para usar Docker!** 🐳

Para más información, consulta:
- `README.md` - Documentación completa
- `docker-compose.yml` - Configuración de servicios
- Logs: `docker-compose logs -f`

