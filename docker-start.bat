@echo off
echo ============================================
echo JWT Auth System - Docker Setup
echo ============================================
echo.

REM Verificar si Docker está instalado
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker no está instalado
    echo Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✓ Docker encontrado
docker --version
echo.

REM Verificar si Docker Compose está disponible
where docker-compose >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set COMPOSE_CMD=docker-compose
) else (
    set COMPOSE_CMD=docker compose
)

echo Usando: %COMPOSE_CMD%
echo.

echo [1/3] Construyendo imágenes Docker...
%COMPOSE_CMD% build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Falló la construcción de las imágenes
    pause
    exit /b 1
)

echo.
echo [2/3] Iniciando servicios...
%COMPOSE_CMD% up -d mariadb redis backend

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Falló al iniciar los servicios
    pause
    exit /b 1
)

echo.
echo [3/3] Esperando que los servicios estén listos...
timeout /t 10 /nobreak >nul

echo.
echo ============================================
echo ✓ Servicios iniciados exitosamente!
echo ============================================
echo.
echo 📊 Estado de los servicios:
%COMPOSE_CMD% ps
echo.
echo 🌐 URLs disponibles:
echo    - Backend API: http://localhost:5000
echo    - Health Check: http://localhost:5000/api/health
echo    - MariaDB: localhost:3306 (usuario: root, password: rootpassword)
echo    - Redis: localhost:6379
echo.
echo 📝 Comandos útiles:
echo    - Ver logs: docker-compose logs -f backend
echo    - Detener: docker-compose down
echo    - Reiniciar: docker-compose restart backend
echo.

pause

