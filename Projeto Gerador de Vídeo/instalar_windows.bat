@echo off
cls

echo.
echo ========================================
echo   VIDEO GENERATOR - Instalador Windows
echo ========================================
echo.
echo Instalando dependencias...
echo.
echo ========================================
echo.

REM Testa python
python --version 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python encontrado!
    python --version
    echo.
    set PYTHON_CMD=python
    goto :install
)

REM Tenta py
py --version 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python encontrado via 'py'!
    py --version
    echo.
    echo [AVISO] Use 'py' ao inves de 'python' nos comandos
    echo.
    set PYTHON_CMD=py
    goto :install
)

REM Se nenhum funciona
echo [ERRO] Python NAO encontrado!
echo.
echo SOLUCOES:
echo.
echo 1. Instale Python de: https://www.python.org/downloads/
echo    - Marque "Add Python to PATH" na instalacao!
echo.
echo 2. Ou baixe da Microsoft Store:
echo    - Procure "Python 3.12"
echo.
echo 3. Apos instalar, REINICIE o PowerShell
echo.
echo ========================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
exit /b 1

:install
echo [1/4] Atualizando pip...
%PYTHON_CMD% -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [ERRO] Erro ao atualizar pip
    echo.
    echo Pressione qualquer tecla para fechar...
    pause >nul
    exit /b 1
)
echo [OK] pip atualizado
echo.

echo [2/4] Instalando dependencias principais...
echo (Isso pode levar alguns minutos...)
echo.
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Erro ao instalar dependencias!
    echo.
    echo Tente instalar manualmente:
    echo   %PYTHON_CMD% -m pip install selenium
    echo   %PYTHON_CMD% -m pip install Pillow
    echo   %PYTHON_CMD% -m pip install opencv-python
    echo   %PYTHON_CMD% -m pip install requests
    echo.
    echo Pressione qualquer tecla para fechar...
    pause >nul
    exit /b 1
)
echo [OK] Dependencias principais instaladas
echo.

echo [3/4] Instalando servidor Flask...
%PYTHON_CMD% -m pip install flask flask-cors
if %errorlevel% neq 0 (
    echo [ERRO] Erro ao instalar Flask
    echo.
    echo Pressione qualquer tecla para fechar...
    pause >nul
    exit /b 1
)
echo [OK] Flask instalado
echo.

echo [4/4] Verificando instalacao...
%PYTHON_CMD% -m pip list | findstr "flask"
echo.

echo ========================================
echo   [OK] INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo PROXIMOS PASSOS:
echo.
echo 1. Execute: iniciar_servidor.bat
echo.
echo 2. Aguarde aparecer "Servidor rodando"
echo.
echo 3. Abra navegador em: http://localhost:5000
echo.
echo ========================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
