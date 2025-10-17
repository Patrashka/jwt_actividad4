@echo off
echo ============================================
echo Deteniendo JWT Auth System
echo ============================================
echo.

REM Detectar comando docker-compose
where docker-compose >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set COMPOSE_CMD=docker-compose
) else (
    set COMPOSE_CMD=docker compose
)

echo Deteniendo servicios...
%COMPOSE_CMD% down

echo.
echo ✓ Servicios detenidos
echo.
echo Para eliminar también los datos (CUIDADO):
echo    docker-compose down -v
echo.

pause

