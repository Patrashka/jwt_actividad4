@echo off
echo ====================================
echo JWT Auth System - Backend Server
echo ====================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias si es necesario
if not exist "venv\Scripts\flask.exe" (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Verificar si existe .env
if not exist ".env" (
    echo.
    echo ADVERTENCIA: No existe archivo .env
    echo Copiando .env.example a .env...
    copy .env.example .env
    echo.
    echo Por favor, edita .env con tus credenciales de base de datos
    pause
)

REM Iniciar servidor Flask
echo.
echo Iniciando servidor Flask...
echo.
python app.py

pause

