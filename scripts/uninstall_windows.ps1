Param(
	[switch]$KeepModels
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "windows_common.ps1")

$repoRoot = Enter-RepoRoot -ScriptDir $scriptDir

function Remove-PathIfExists {
	Param(
		[string]$PathToRemove,
		[string]$Label
	)

	if (-not (Test-Path $PathToRemove)) {
		Write-Output "Skip $Label (not found): $PathToRemove"
		return
	}

	Write-Output "Removing ${Label}: $PathToRemove"
	Remove-Item -Path $PathToRemove -Recurse -Force -ErrorAction SilentlyContinue
}

Remove-PathIfExists -PathToRemove (Join-Path $repoRoot ".venv") -Label "virtualenv"

if (-not $KeepModels) {
	$modelsRoot = Join-Path $repoRoot "models"
	if (-not (Test-Path $modelsRoot)) {
		Write-Output "Skip models cleanup (not found): $modelsRoot"
		return
	}

	Get-ChildItem -Path $modelsRoot -Directory | ForEach-Object {
		$downloadPath = Join-Path $_.FullName "model_download"
		Remove-PathIfExists -PathToRemove $downloadPath -Label "model download"

		$voicesPath = Join-Path $_.FullName "voices"
		if (Test-Path $voicesPath) {
			Get-ChildItem -Path $voicesPath -File -Include *.pt, *.pth, *.safetensors, *.bin | ForEach-Object {
				Remove-PathIfExists -PathToRemove $_.FullName -Label "voice weights"
			}
		}
	}
} else {
	Write-Output "Keep models folder as requested."
}
