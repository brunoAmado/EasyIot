# ==============================================================================
# 🧠 EasyIot Espressif QEMU Installer for Windows (PowerShell)
# Installs Espressif QEMU for ESP32 full binary & network emulation
# ==============================================================================

$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "🚀 Installing Espressif QEMU for ESP32 (Xtensa + OpenETH)" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Run the python installer
py -3.11 tools/install_qemu.py
if ($LASTEXITCODE -ne 0) {
    python tools/install_qemu.py
}
