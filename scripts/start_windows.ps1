Param(
	[int]$Port = 8001,
	[switch]$Reload,
	[string]$ModelName = "kokoro"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "windows_common.ps1")

Enter-RepoRoot -ScriptDir $scriptDir | Out-Null
Ensure-Uv
Sync-Dependencies -ModelName $ModelName
Download-Models -ModelName $ModelName
Start-VoiceService -ModelName $ModelName -Port $Port

# Write-Output "Starting uvicorn (host 0.0.0.0 port $Port)..."
# if ($Reload) {
#     & python -m uvicorn api.api_handler:app --host 0.0.0.0 --port $Port --reload
# } else {
#     & python -m uvicorn api.api_handler:app --host 0.0.0.0 --port $Port
# }
