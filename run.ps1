param(
    [Parameter(Position = 0, Mandatory = $false)]
    [string]$Target
)

# 1. Set execution policy for current process
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force

# 2. Locate repository root and virtual environment
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RootDir

$VenvPython = Join-Path $RootDir "venv\Scripts\python.exe"
$VenvActivate = Join-Path $RootDir "venv\Scripts\Activate.ps1"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment Python not found at: $VenvPython"
    exit 1
}

# 3. Activate virtual environment in this session
if (Test-Path $VenvActivate) {
    & $VenvActivate
}

# 4. Handle commands
if (-not $Target) {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " Data Analytics Universal Runner" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "Usage:"
    Write-Host "  .\run.ps1 <path-to-script.py>   Run any python script"
    Write-Host "  .\run.ps1 jupyter               Launch Jupyter Notebook"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run.ps1 Matplotlib-Seaborn\week-6\day-1\netflix_eda.py"
    Write-Host "  .\run.ps1 pandas\titanic_eda.py"
    Write-Host "  .\run.ps1 jupyter"
    Write-Host "==========================================================" -ForegroundColor Cyan
    exit 0
}

if ($Target -eq "jupyter" -or $Target -eq "notebook") {
    Write-Host "Starting Jupyter Notebook from project root..." -ForegroundColor Green
    & "$RootDir\venv\Scripts\jupyter.exe" notebook --notebook-dir="$RootDir"
    exit $LASTEXITCODE
}

# 5. Resolve script path and run
$ScriptPath = if (Test-Path $Target) {
    (Resolve-Path $Target).Path
} elseif (Test-Path (Join-Path $RootDir $Target)) {
    (Resolve-Path (Join-Path $RootDir $Target)).Path
} else {
    Write-Error "Script file not found: $Target"
    exit 1
}

Write-Host "Running: $ScriptPath" -ForegroundColor Green
& $VenvPython $ScriptPath
exit $LASTEXITCODE
