function Enter-RepoRoot {
	Param(
		[string]$ScriptDir
	)

	if (-not $ScriptDir) {
		$ScriptDir = Split-Path -Parent $PSScriptRoot
	}
	$repoRoot = Resolve-Path (Join-Path $ScriptDir "..")
	Set-Location $repoRoot
	return $repoRoot
}

function Ensure-Uv {
	if (Get-Command uv -ErrorAction SilentlyContinue) { return }
	Write-Output "uv not found in PATH. Installing via official script..."
	try { irm https://astral.sh/uv/install.ps1 | iex } catch {
		Write-Error "Failed to run official uv install script."
		exit 1
	}
	if (Get-Command uv -ErrorAction SilentlyContinue) { return }
	$uvCandidate1 = Join-Path $env:USERPROFILE ".cargo\bin\uv.exe"
	$uvCandidate2 = Join-Path $env:LOCALAPPDATA "uv\bin\uv.exe"
	if (Test-Path $uvCandidate1) { $env:PATH = "$env:PATH;$([System.IO.Path]::GetDirectoryName($uvCandidate1))"; return }
	if (Test-Path $uvCandidate2) { $env:PATH = "$env:PATH;$([System.IO.Path]::GetDirectoryName($uvCandidate2))"; return }
	Write-Error "uv not found after installation. Please restart the shell or ensure uv is on PATH."
	exit 1
}

function Test-NvidiaGpu {
	$nv = Get-Command nvidia-smi -ErrorAction SilentlyContinue
	if (-not $nv) { return $false }
	try {
		& $nv -L | Out-Null
		return $true
	} catch {
		return $false
	}
}

function Sync-Dependencies {
	Param(
		[string]$ModelName = "kokoro"
	)

	Write-Output "Syncing dependencies with uv..."
	if (Test-NvidiaGpu) {
		Write-Output "NVIDIA GPU detected, syncing CUDA extras..."
		uv sync --extra $ModelName --extra torch-cu121
	} else {
		Write-Output "No NVIDIA GPU detected, syncing CPU extras..."
		uv sync --extra $ModelName --extra torch-cpu
	}
}

function Download-Models {
	Param(
		[string]$ModelName = "kokoro"
	)

	Write-Output "Downloading models..."
	$env:HF_ENDPOINT = "https://hf-mirror.com"
	uv run .\cli.py download --model-names=$ModelName
}

function Start-VoiceService {
	Param(
		[string]$ModelName = "kokoro",
		[int]$Port = 8001
	)

	Write-Output "Starting service (host 0.0.0.0 port $Port)..."
	uv run .\cli.py run --model-names=$ModelName --port $Port
}

function Stop-VoiceService {
	Param(
		[int]$Port = 0
	)

	$portSegment = if ($Port -gt 0) { "--port $Port" } else { "" }
	$targets = Get-CimInstance Win32_Process |
		Where-Object {
			$cmd = $_.CommandLine
			$name = $_.Name
			$isPython = $name -match "python|uv" -or $cmd -match "python|uv"
			$isVoiceRun = $cmd -match "cli\.py\s+run"
			$isPortMatch = [string]::IsNullOrWhiteSpace($portSegment) -or $cmd -match [regex]::Escape($portSegment)
			return $isPython -and $isVoiceRun -and $isPortMatch
		}

	if (-not $targets) {
		if ($Port -gt 0) {
			Write-Output "No running voice service process found on port $Port."
		} else {
			Write-Output "No running voice service process found."
		}
		return
	}

	$targets | ForEach-Object {
		Write-Output "Stopping process PID=$($_.ProcessId)"
		Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
	}
}
