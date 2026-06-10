@echo off
cls

echo.
echo ========================================
echo   VIDEO GENERATOR - Servidor
echo ========================================
echo.

REM Testa python
python --version 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :start
)

REM Tenta py
py --version 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :start
)

REM Nenhum funciona
echo [ERRO] Python NAO encontrado!
echo.
echo Execute primeiro: instalar_windows.bat
echo.
echo ========================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
exit /b 1

:start
echo [OK] Python encontrado: 
%PYTHON_CMD% --version
echo.

REM Verifica se server.py existe
if not exist server.py (
    echo [ERRO] Arquivo server.py nao encontrado!
    echo.
    echo Certifique-se de estar na pasta correta do projeto.
    echo.
    echo ========================================
    echo.
    echo Pressione qualquer tecla para fechar...
    pause >nul
    exit /b 1
)

echo ========================================
echo   INICIANDO SERVIDOR...
echo ========================================
echo.
echo URL: http://localhost:5000
echo.
echo Abra seu navegador neste endereco
echo.
echo IMPORTANTE: 
echo    - NAO FECHE esta janela enquanto usar!
echo    - Para parar: Pressione Ctrl+C
echo.
echo ========================================
echo.

%PYTHON_CMD% server.py

REM Se o servidor parar
echo.
echo.
echo ========================================
echo   Servidor parou
echo ========================================
echo.
echo Se houve erro, verifique:
echo   1. Todas dependencias instaladas?
echo   2. Porta 5000 esta livre?
echo   3. Arquivos estao na pasta correta?
echo.
echo ========================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
