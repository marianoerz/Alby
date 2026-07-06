@echo off
REM ======================================================================
REM  Jarvis - Script de inicio para Windows
REM ======================================================================

title Jarvis - Asistente Virtual

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar si existe el entorno virtual
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ADVERTENCIA] Entorno virtual no encontrado. Usando Python del sistema.
    echo               Ejecuta install.bat para configurar el entorno.
)

REM Iniciar Jarvis
python app.py

REM Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo [ERROR] Jarvis se cerro con un error.
    echo         Revisa logs\jarvis.log para mas detalles.
    pause
)
