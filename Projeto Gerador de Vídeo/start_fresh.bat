@echo off
echo ========================================
echo   LIMPANDO CACHE E INICIANDO SERVIDOR
echo ========================================
echo.

REM Limpa cache Python
echo Limpando cache Python...
if exist __pycache__ (
    rmdir /S /Q __pycache__
    echo   - Cache __pycache__ removido
)

if exist *.pyc (
    del /F /Q *.pyc
    echo   - Arquivos .pyc removidos
)

echo.
echo ========================================
echo   INICIANDO SERVIDOR LIMPO
echo ========================================
echo.

REM Define variável para forçar reload
set PYTHONDONTWRITEBYTECODE=1

REM Inicia servidor
python server.py

pause
