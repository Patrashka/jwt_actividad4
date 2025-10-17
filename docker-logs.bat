@echo off
echo ============================================
echo Logs de JWT Auth System
echo ============================================
echo.

REM Detectar comando docker-compose
where docker-compose >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set COMPOSE_CMD=docker-compose
) else (
    set COMPOSE_CMD=docker compose
)

echo Mostrando logs en tiempo real...
echo Presiona Ctrl+C para salir
echo.

%COMPOSE_CMD% logs -f backend

