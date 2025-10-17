@echo off
echo ============================================
echo JWT Auth System - Actividad 4
echo Backend Flask + Cliente JavaFX
echo ============================================
echo.

REM Iniciar backend Flask en una nueva ventana
echo Iniciando Backend Flask...
start "Backend Flask" cmd /k "call venv\Scripts\activate.bat && python app.py"

REM Esperar un momento para que el backend inicie
echo Esperando 5 segundos para que el backend inicie...
timeout /t 5 /nobreak >nul

REM Iniciar cliente JavaFX
echo.
echo Iniciando Cliente JavaFX...
timeout /t 2 /nobreak >nul

call run_javafx.bat

pause

