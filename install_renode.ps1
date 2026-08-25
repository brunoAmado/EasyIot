# install_renode.ps1
# Automated installer for Antmicro Renode on Windows

$ErrorActionPreference = "Continue"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🚀 Installing Renode Hardware Emulator for Windows" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Check if python is available in project venv
$PythonExe = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }

# Execute the cross-platform Python installer
& $PythonExe tools/install_renode.py
