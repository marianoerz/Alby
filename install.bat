@echo off
REM ======================================================================
REM  Jarvis - Script de instalacion automatica para Windows
REM  Ejecutar como administrador si hay problemas de permisos.
REM ======================================================================

title Instalacion de Jarvis

echo.
echo  ===================================================
echo            JARVIS - Instalacion Automatica
echo  ===================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo         Descarga Python 3.12+ desde https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado.

REM Crear entorno virtual
echo.
echo [1/4] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado.

REM Activar entorno virtual
echo.
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo.
echo [3/4] Actualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar dependencias
echo.
echo [4/4] Instalando dependencias (puede tardar varios minutos)...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ADVERTENCIA] Algunas dependencias opcionales pueden no haberse instalado.
    echo               Jarvis puede funcionar con funcionalidades reducidas.
    echo               Revisa el mensaje de error anterior para mas detalles.
) else (
    echo [OK] Todas las dependencias instaladas correctamente.
)

echo.
echo  ===================================================
echo             Instalacion completada
echo.
echo   Proximos pasos:
echo   1. Edita config.json y agrega tu API key
echo   2. Ejecuta: jarvis.bat
echo  ===================================================
echo.

pause
