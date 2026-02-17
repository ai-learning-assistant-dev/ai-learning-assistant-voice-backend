Param(
    [string]$Python = "python",
    [string]$IndexUrl = "https://mirrors.aliyun.com/pypi/simple"
)

$ErrorActionPreference = "Stop"

$py = Get-Command $Python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Error "Python not found: $Python"
    exit 1
}

Write-Host "Upgrading pip (no env vars modified)..." -ForegroundColor Cyan
& $Python -m pip install --upgrade pip --index-url $IndexUrl --trusted-host mirrors.aliyun.com

Write-Host "Installing uv (no env vars modified)..." -ForegroundColor Cyan
& $Python -m pip install uv --index-url $IndexUrl --trusted-host mirrors.aliyun.com

Write-Host "uv installed via $Python" -ForegroundColor Green