#!/usr/bin/env pwsh
set-StrictMode -Version Latest

if (-not (Test-Path .\venv)) {
    python -m venv .\venv
}
. .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
