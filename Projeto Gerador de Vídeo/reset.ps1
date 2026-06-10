Write-Host "=== LIMPANDO SISTEMA ===" -ForegroundColor Yellow
Write-Host ""

# Mata todos os Python
Write-Host "[1/3] Matando processos Python..." -NoNewline
Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host " OK" -ForegroundColor Green

# Mata todos os Chrome do automation
Write-Host "[2/3] Matando Chrome..." -NoNewline
Get-Process chrome* -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host " OK" -ForegroundColor Green

Start-Sleep -Seconds 3

# Inicia servidor
Write-Host "[3/3] Iniciando servidor na porta 5120..." -NoNewline
$env:SERVER_PORT="5120"
Start-Process powershell -ArgumentList "-NoLogo -NoProfile -Command `$env:SERVER_PORT='5120'; python server.py" -WorkingDirectory "C:\Users\Lucas Pietro\Desktop\Projeto\Projeto Gerador de Vídeo" -WindowStyle Minimized
Start-Sleep -Seconds 8

# Verifica se subiu
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5120/api/health" -UseBasicParsing -ErrorAction Stop
    Write-Host " OK" -ForegroundColor Green
    Write-Host ""
    Write-Host "=== SERVIDOR RODANDO ===" -ForegroundColor Green
    Write-Host "Acesse: http://localhost:5120" -ForegroundColor Cyan
} catch {
    Write-Host " FALHOU" -ForegroundColor Red
    Write-Host "Tente iniciar manualmente: python server.py" -ForegroundColor Yellow
}
