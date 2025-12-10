# One-click test runner for Windows PowerShell
# Usage: ./run_tests.ps1

$ErrorActionPreference = 'Stop'

# Prefer the project's .venv python if present, otherwise fallback to system python
$VenvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (Test-Path $VenvPython) {
    $PYEXEC = $VenvPython
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PYEXEC = 'python'
} else {
    Write-Host "Python not found in PATH and no .venv found. Please install or activate a Python environment."
    exit 1
}

& $PYEXEC -m pip install --upgrade pip
& $PYEXEC -m pip install -r requirements.txt

# Run pytest. For CI, skip long perf test by default unless UD_RUN_PERF=1
$env:UD_SKIP_LONG_TESTS = if ($env:UD_RUN_PERF -eq '1') { '0' } else { '1' }

& $PYEXEC -m pytest -q --maxfail=1 --disable-warnings

# Print metrics if available
$PYCODE = "from user_display.metrics import GLOBAL; print('METRICS snapshot:', GLOBAL.snapshot())"
Write-Host "Using python executable:" $PYEXEC
try {
    & "$PYEXEC" "-c" $PYCODE
} catch {
    Write-Warning "Failed to run metrics snippet: $_"
}