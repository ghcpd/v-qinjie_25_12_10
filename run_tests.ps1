# run_tests.ps1
# PowerShell test runner for user_display module
# Usage: .\run_tests.ps1

param(
    [switch]$Verbose = $false,
    [switch]$Coverage = $false,
    [string]$TestFile = "tests/test_all.py"
)

Write-Host "=" * 80
Write-Host "User Display Module - Test Runner (PowerShell)"
Write-Host "=" * 80
Write-Host ""

# Check Python availability
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Get Python version
$pythonVersion = python --version 2>&1
Write-Host "Using: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check if test file exists
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$testFilePath = Join-Path $scriptRoot $TestFile

if (-not (Test-Path $testFilePath)) {
    Write-Host "ERROR: Test file not found: $testFilePath" -ForegroundColor Red
    exit 1
}

Write-Host "Running tests from: $testFilePath" -ForegroundColor Cyan
Write-Host ""

# Run tests
$args = @($testFilePath)
if ($Verbose) {
    $args += "--verbose"
}
if ($Coverage) {
    $args += "--cov=user_display"
}

try {
    & python @args
    $exitCode = $LASTEXITCODE
} catch {
    Write-Host "ERROR: Failed to run tests" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

Write-Host ""
Write-Host "=" * 80
Write-Host "Test run completed" -ForegroundColor Green
Write-Host "=" * 80

exit $exitCode
