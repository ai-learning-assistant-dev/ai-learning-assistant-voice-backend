@echo off
REM start_windows.bat [port]
SETLOCAL

REM Move to repo root (parent of scripts folder)
cd /d "%~dp0\.."

REM Prefer uv from PATH, fallback to official installer
call :resolve_uv
if "%UV_EXE%"=="" (
  echo uv not found in PATH. Installing via official script...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 ^| iex"
  call :resolve_uv
)

if "%UV_EXE%"=="" (
  echo uv not found after installation. Please restart the shell or ensure uv is on PATH.
  pause
  exit /b 1
)

if "%1"=="" (
  set PORT=8001
) else (
  set PORT=%1
)

echo Syncing dependencies with uv (Aliyun mirror)...
where nvidia-smi >nul 2>nul
if errorlevel 1 (
  echo No NVIDIA GPU detected, syncing CPU extras...
  "%UV_EXE%" sync --extra kokoro --extra torch-cpu
) else (
  echo NVIDIA GPU detected, syncing CUDA extras...
  "%UV_EXE%" sync --extra kokoro --extra torch-cu121
)

echo Downloading models...
set "HF_ENDPOINT=https://hf-mirror.com"
"%UV_EXE%" run .\cli.py download --model-names=kokoro

echo Starting service on port %PORT%...
"%UV_EXE%" run .\cli.py run --model-names=kokoro --port %PORT%

@REM echo Starting uvicorn on port %PORT%...
@REM python -m uvicorn api.api_handler:app --host 0.0.0.0 --port %PORT%

ENDLOCAL
exit /b 0

:resolve_uv
set "UV_EXE="
for /f "delims=" %%i in ('where uv 2^>nul') do set "UV_EXE=%%i"
if "%UV_EXE%"=="" if exist "%USERPROFILE%\.cargo\bin\uv.exe" set "UV_EXE=%USERPROFILE%\.cargo\bin\uv.exe"
if "%UV_EXE%"=="" if exist "%LOCALAPPDATA%\uv\bin\uv.exe" set "UV_EXE=%LOCALAPPDATA%\uv\bin\uv.exe"
exit /b 0
