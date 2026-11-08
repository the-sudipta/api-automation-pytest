# Prepares everything inside the repo on Windows without admin rights.
# Uses uv from PATH if present; otherwise downloads the standalone uv (checksum verified) into tools/.
# uv then installs Python 3.12 and the packages from uv.lock.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$repo = Split-Path -Parent $PSScriptRoot
$tools = Join-Path $repo 'tools'

function Install-Uv {
    $base = 'https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip'
    New-Item -ItemType Directory -Force $tools | Out-Null
    $zip = Join-Path $tools 'uv.zip'
    Invoke-WebRequest $base -OutFile $zip
    $expected = (Invoke-RestMethod "$base.sha256").ToString().Split(' ')[0].Trim().ToLower()
    if ((Get-FileHash $zip -Algorithm SHA256).Hash.ToLower() -ne $expected) { throw 'uv checksum mismatch' }
    Expand-Archive $zip -DestinationPath (Join-Path $tools 'uv') -Force
    Remove-Item $zip
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    if (-not (Test-Path (Join-Path $tools 'uv\uv.exe'))) { Install-Uv }
    $env:Path = (Join-Path $tools 'uv') + ';' + $env:Path
}

Push-Location $repo
try {
    uv sync
    Write-Host 'Setup complete. Run: uv run pytest'
} finally {
    Pop-Location
}
