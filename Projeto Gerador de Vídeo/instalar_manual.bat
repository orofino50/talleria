@echo off
cls

echo.
echo ========================================
echo   VIDEO GENERATOR - Instalacao Manual
echo ========================================
echo.
echo Instalando pacotes individualmente...
echo.
echo ========================================
echo.

REM Detecta python
python --version 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    py --version 2>nul
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py
    ) else (
        echo [ERRO] Python nao encontrado!
        pause
        exit /b 1
    )
)

echo [OK] Usando: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo ========================================
echo   Instalando pacotes...
echo ========================================
echo.

REM Atualizar pip
echo [1/8] Atualizando pip...
%PYTHON_CMD% -m pip install --upgrade pip
echo.

REM Selenium
echo [2/8] Instalando selenium...
%PYTHON_CMD% -m pip install selenium
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao instalar selenium
) else (
    echo [OK] selenium instalado
)
echo.

REM webdriver-manager
echo [3/8] Instalando webdriver-manager...
%PYTHON_CMD% -m pip install webdriver-manager
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao instalar webdriver-manager
) else (
    echo [OK] webdriver-manager instalado
)
echo.

REM Pillow (versao compativel)
echo [4/8] Instalando Pillow...
%PYTHON_CMD% -m pip install Pillow
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao instalar Pillow
    echo Tentando versao especifica...
    %PYTHON_CMD% -m pip install "Pillow>=10.3.0"
) else (
    echo [OK] Pillow instalado
)
echo.

REM opencv-python
echo [5/8] Instalando opencv-python...
%PYTHON_CMD% -m pip install opencv-python
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao instalar opencv-python
) else (
    echo [OK] opencv-python instalado
)
echo.

REM requests
echo [6/8] Instalando requests...
%PYTHON_CMD% -m pip install requests
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao instalar requests
) else (
    echo [OK] requests instalado
)
echo.

REM Flask
echo [7/8] Instalando Flask...
%PYTHON_CMD% -m pip install flask
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao instalar Flask
) else (
    echo [OK] Flask instalado
)
echo.

REM flask-cors
echo [8/8] Instalando flask-cors...
%PYTHON_CMD% -m pip install flask-cors
if %errorlevel% neq 0 (
    echo [AVISO] Erro ao instalar flask-cors
) else (
    echo [OK] flask-cors instalado
)
echo.

echo ========================================
echo   Verificando instalacao...
echo ========================================
echo.

REM Testa imports
%PYTHON_CMD% -c "import selenium; print('[OK] selenium funciona')" 2>nul
%PYTHON_CMD% -c "import PIL; print('[OK] Pillow funciona')" 2>nul
%PYTHON_CMD% -c "import cv2; print('[OK] opencv funciona')" 2>nul
%PYTHON_CMD% -c "import requests; print('[OK] requests funciona')" 2>nul
%PYTHON_CMD% -c "import flask; print('[OK] flask funciona')" 2>nul
%PYTHON_CMD% -c "import flask_cors; print('[OK] flask-cors funciona')" 2>nul

echo.
echo ========================================
echo   Instalacao concluida!
echo ========================================
echo.
echo Proximo passo:
echo   Execute: testar_instalacao.bat
echo.
echo Se todos derem [OK], execute:
echo   iniciar_servidor.bat
echo.
echo ========================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
