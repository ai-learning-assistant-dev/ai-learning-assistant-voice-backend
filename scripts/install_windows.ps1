Param(
	[string]$ModelName = "kokoro"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "windows_common.ps1")

Enter-RepoRoot -ScriptDir $scriptDir | Out-Null
Ensure-Uv
Sync-Dependencies -ModelName $ModelName
Download-Models -ModelName $ModelName
