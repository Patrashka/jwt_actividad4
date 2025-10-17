@echo off
echo ==========================================
echo JWT Auth Client - JavaFX
echo ==========================================
echo.

REM Verificar si Maven está instalado
where mvn >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Maven no está instalado o no está en el PATH
    echo.
    echo Por favor, instala Maven desde: https://maven.apache.org/download.cgi
    echo Y configura la variable de entorno PATH
    pause
    exit /b 1
)

REM Verificar si Java está instalado
where java >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Java no está instalado o no está en el PATH
    echo.
    echo Por favor, instala Java 21 desde: https://www.oracle.com/java/technologies/downloads/
    echo Y configura la variable de entorno JAVA_HOME y PATH
    pause
    exit /b 1
)

echo Verificando versiones...
java -version
echo.
mvn -version
echo.

echo ==========================================
echo Compilando proyecto...
echo ==========================================
mvn clean compile
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: La compilación falló
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Ejecutando aplicación JavaFX...
echo ==========================================
echo.

REM Verificar que el backend esté ejecutándose
echo NOTA: Asegúrate de que el backend Flask esté ejecutándose en http://localhost:5000
echo Si no lo has iniciado, abre otra terminal y ejecuta: start_windows.bat
echo.
timeout /t 3 >nul

mvn javafx:run

pause

