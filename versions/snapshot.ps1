param(
    [string]$Version = "",
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir
$VersionsDir = Join-Path $ProjectRoot "versions"

if (-not (Test-Path $VersionsDir)) {
    New-Item -ItemType Directory -Path $VersionsDir -Force | Out-Null
}

if ([string]::IsNullOrWhiteSpace($Version)) {
    $existing = Get-ChildItem -Path $VersionsDir -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.Name }
    $numbers = $existing | ForEach-Object { if ($_ -match '^v(\d+)\.(\d+)$') { [int]$Matches[1] * 100 + [int]$Matches[2] } } | Sort-Object
    $next = if ($numbers.Count -gt 0) { $numbers[-1] + 1 } else { 100 }
    $major = [math]::Floor($next / 100)
    $minor = $next % 100
    $Version = "v$major.$minor"
    Write-Host "Auto-detected next version: $Version"
}

$VersionDir = Join-Path $VersionsDir $Version
if (Test-Path $VersionDir) {
    Write-Error "Version $Version already exists at $VersionDir"
    exit 1
}

New-Item -ItemType Directory -Path $VersionDir -Force | Out-Null

$folders = @("talleria", "talleria/css", "talleria/js", "talleria/images")
$files = @("talleria/index.html", "talleria/producto.html", "talleria/sobre.html", "talleria/faq.html", "talleria/contacto.html", "talleria/css/styles.css", "talleria/js/scripts.js")

foreach ($f in $files) {
    $src = Join-Path $ProjectRoot $f
    if (Test-Path $src) {
        $dst = Join-Path $VersionDir $f
        $dstDir = Split-Path -Parent $dst
        if (-not (Test-Path $dstDir)) {
            New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
        }
        Copy-Item -Path $src -Destination $dst -Force
        Write-Host "  + $f"
    }
}

$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$note = @"
Version: $Version
Date: $ts
Message: $Message

Files snapshotted: $($files -join ', ')
"@
$notePath = Join-Path $VersionDir "VERSION.txt"
$note | Out-File -FilePath $notePath -Encoding utf8

Write-Host ""
Write-Host "Snapshot created: $VersionDir" -ForegroundColor Green
Write-Host "Description: $Message"
