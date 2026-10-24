@echo off
rem ============================================================
rem  CyberShield IA v3 - Antivirus con Inteligencia Artificial
rem  Launcher para Windows
rem  Desarrollado en Neuquen, Argentina
rem ============================================================

setlocal enabledelayedexpansion

echo.
echo   ╔═══════════════════════════════════════════════════════════════╗
echo   ║       CyberShield IA v3.0 - Cargando...                      ║
echo   ║       Antivirus Inteligente con Prediccion de Amenazas       ║
echo   ╚═══════════════════════════════════════════════════════════════╝
echo.

rem Verificar que Python esté disponible
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] ERROR: Python no detectado en este equipo.
    echo     Descarga desde: https://www.python.org/downloads/
    echo     IMPORTANTE: Marca "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

rem Verificar versión de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [+] Python detectado: %PYTHON_VERSION%

echo.
echo [*] Verificando dependencias...

python -c "import tkinter" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] tkinter no disponible
    echo     Reinstala Python y marca 'tcl/tk and IDLE' en la instalacion
) else (
    echo [+] tkinter: OK
)

python -c "import sqlite3" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [+] sqlite3: OK
)

echo.
echo [*] Iniciando CyberShield IA v3.0...
echo     Interfaz: Matrix-style | Modo: Predicción con IA
echo.

cd /d "%~dp0"

rem Crear carpeta de datos si no existe
if not exist "cybershield_datos" (
    mkdir cybershield_datos
    echo [+] Carpeta de datos creada
)

rem Ejecutar aplicación principal
python main.pyw

if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] La aplicacion se cerro con errores (codigo: %ERRORLEVEL%)
    echo     Verifica:
    echo     - Python esta correctamente instalado
    echo     - tkinter esta disponible
    echo     - Los archivos .py estan presentes
    echo.
    pause
)

endlocal
