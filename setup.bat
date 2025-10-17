@echo off
echo ============================================
echo JWT Auth System - Setup
echo ============================================
echo.

echo [1/4] Verificando requisitos...
echo.

REM Verificar Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python no está instalado
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python encontrado
python --version

REM Verificar Java
where java >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Java no está instalado
    echo Descarga Java 21 desde: https://www.oracle.com/java/technologies/downloads/
    pause
    exit /b 1
)
echo ✓ Java encontrado
java -version

REM Verificar Maven
where mvn >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Maven no está instalado
    echo Descarga Maven desde: https://maven.apache.org/download.cgi
    pause
    exit /b 1
)
echo ✓ Maven encontrado
mvn -version

echo.
echo [2/4] Configurando entorno virtual Python...
if not exist "venv" (
    python -m venv venv
    echo ✓ Entorno virtual creado
) else (
    echo ✓ Entorno virtual ya existe
)

echo.
echo [3/4] Instalando dependencias Python...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✓ Dependencias Python instaladas

echo.
echo [4/4] Configurando archivo .env...
if not exist ".env" (
    copy .env.example .env
    echo ✓ Archivo .env creado
    echo.
    echo IMPORTANTE: Edita el archivo .env con tus credenciales de base de datos
    echo.
) else (
    echo ✓ Archivo .env ya existe
)

echo.
echo ============================================
echo Setup completado exitosamente!
echo ============================================
echo.
echo Próximos pasos:
echo 1. Edita .env con tus credenciales de base de datos
echo 2. Asegúrate de que MariaDB/MySQL esté ejecutándose
echo 3. Ejecuta: run_all.bat
echo.

pause

