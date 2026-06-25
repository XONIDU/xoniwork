@echo off
title XONIWORK 2026 - Simulador de Escritura Automatica
color 0A

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo           XONIWORK 2026 - Simulador de Escritura
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo Iniciando XONIWORK...
echo.
echo [INFO] Simulador de escritura automatica para emular trabajo
echo [INFO] Accede a: http://localhost:5000
echo.
echo [INFO] Configuracion disponible:
echo   - Velocidad de escritura (0.01s - 1s por caracter)
echo   - Nivel de errores (0%% a 8%%)
echo   - Espera inicial (0s a 10s)
echo.
echo [INFO] Formatos soportados: .txt, .pdf, .docx
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python start.py

pause
