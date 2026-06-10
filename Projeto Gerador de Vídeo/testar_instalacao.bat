@echo off
cls

echo.
echo ========================================
echo   VIDEO GENERATOR - Diagnostico
echo ========================================
echo.
echo Este script verifica se tudo esta OK
echo.
echo ========================================
echo.

REM Teste 1: Python
echo [1/6] Testando Python...
python --version 2>nul
if %errorlevel% equ 0 (
    echo [OK] python funciona
    python --version
    set PYTHON_CMD=python
    goto :test2
)

py --version 2>nul
if %errorlevel% equ 0 (
    echo [OK] py funciona
    py --version
    set PYTHON_CMD=py
    echo [AVISO] Use 'py' ao inves de 'python'
    goto :test2
)

echo [ERRO] Python NAO encontrado
echo        Instale de: https://www.python.org/downloads/
set PYTHON_CMD=NONE
goto :error

:test2
echo.

REM Teste 2: pip
echo [2/6] Testando pip...
%PYTHON_CMD% -m pip --version 2>nul
if %errorlevel% equ 0 (
    echo [OK] pip funciona
    %PYTHON_CMD% -m pip --version
) else (
    echo [ERRO] pip NAO funciona
    echo        Execute: %PYTHON_CMD% -m ensurepip
)
echo.

REM Teste 3: Arquivos do projeto
echo [3/6] Verificando arquivos...
if exist requirements.txt (
    echo [OK] requirements.txt encontrado
) else (
    echo [ERRO] requirements.txt NAO encontrado
)

if exist server.py (
    echo [OK] server.py encontrado
) else (
    echo [ERRO] server.py NAO encontrado
)

if exist video_generator.py (
    echo [OK] video_generator.py encontrado
) else (
    echo [ERRO] video_generator.py NAO encontrado
)

if exist interface.html (
    echo [OK] interface.html encontrado
) else (
    echo [ERRO] interface.html NAO encontrado
)
echo.

REM Teste 4: Dependencias principais
echo [4/6] Verificando dependencias...
%PYTHON_CMD% -c "import selenium" 2>nul
if %errorlevel% equ 0 (
    echo [OK] selenium instalado
) else (
    echo [FALTA] selenium NAO instalado
)

%PYTHON_CMD% -c "import PIL" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Pillow instalado
) else (
    echo [FALTA] Pillow NAO instalado
)

%PYTHON_CMD% -c "import cv2" 2>nul
if %errorlevel% equ 0 (
    echo [OK] opencv-python instalado
) else (
    echo [FALTA] opencv-python NAO instalado
)

%PYTHON_CMD% -c "import requests" 2>nul
if %errorlevel% equ 0 (
    echo [OK] requests instalado
) else (
    echo [FALTA] requests NAO instalado
)
echo.

REM Teste 5: Flask
echo [5/6] Verificando Flask...
%PYTHON_CMD% -c "import flask" 2>nul
if %errorlevel% equ 0 (
    echo [OK] flask instalado
) else (
    echo [FALTA] flask NAO instalado
)

%PYTHON_CMD% -c "import flask_cors" 2>nul
if %errorlevel% equ 0 (
    echo [OK] flask-cors instalado
) else (
    echo [FALTA] flask-cors NAO instalado
)
echo.

REM Teste 6: Porta 5000
echo [6/6] Verificando porta 5000...
netstat -an 2>nul | findstr ":5000" >nul
if %errorlevel% equ 0 (
    echo [AVISO] Porta 5000 JA esta em uso
    echo         Feche outros servidores antes de iniciar
) else (
    echo [OK] Porta 5000 disponivel
)
echo.

echo ========================================
echo   RESUMO DO DIAGNOSTICO
echo ========================================
echo.

REM Resumo
%PYTHON_CMD% -c "import sys; import selenium, PIL, cv2, requests, flask, flask_cors; print('[OK] Tudo pronto!')" 2>nul
if %errorlevel% equ 0 (
    echo STATUS: [OK] TUDO INSTALADO!
    echo.
    echo Voce pode usar o Video Generator!
    echo.
    echo Proximo passo:
    echo   1. Execute: iniciar_servidor.bat
    echo   2. Abra navegador em: http://localhost:5000
) else (
    echo STATUS: [ERRO] FALTAM DEPENDENCIAS
    echo.
    echo Execute: instalar_windows.bat
)

echo.
echo ========================================
goto :end

:error
echo.
echo ========================================
echo   [ERRO CRITICO]
echo ========================================
echo.
echo Python nao esta instalado ou nao esta no PATH.
echo.
echo SOLUCAO:
echo   1. Instale Python: https://www.python.org/downloads/
echo   2. Marque "Add Python to PATH"
echo   3. Reinicie o terminal
echo.
echo ========================================

:end
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
