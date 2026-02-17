Param(
    [string]$DownloadUrl = "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip",
    [string]$DestDir = "..\util\uv-bin"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$destPath = Join-Path $repoRoot $DestDir
$zipPath = Join-Path $repoRoot "uv.zip"

Write-Host "Downloading uv binary..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $DownloadUrl -OutFile $zipPath

Write-Host "Extracting..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $destPath -Force | Out-Null
Expand-Archive -LiteralPath $zipPath -DestinationPath $destPath -Force

Write-Host "Cleaning up..." -ForegroundColor Cyan
Remove-Item $zipPath -Force

Write-Host "uv downloaded to $destPath (no environment variables modified)." -ForegroundColor Green
Write-Host "Use it via: `"$(Join-Path $destPath 'uv.exe')`" or add that folder to PATH manually." -ForegroundColor Yellow