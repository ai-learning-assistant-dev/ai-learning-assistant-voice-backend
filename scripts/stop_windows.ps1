Param(
	[int]$Port = 0
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "windows_common.ps1")

Stop-VoiceService -Port $Port
