Param(
	[int]$Port = 8001,
	[string]$ModelName = "kokoro"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "windows_common.ps1")

Enter-RepoRoot -ScriptDir $scriptDir | Out-Null
Ensure-Uv
Start-VoiceService -ModelName $ModelName -Port $Port
