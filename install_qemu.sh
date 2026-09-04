#!/usr/bin/env bash
# ==============================================================================
# 🧠 EasyIot Espressif QEMU Installer for Linux / macOS
# Installs Espressif QEMU for ESP32 full binary & network emulation
# ==============================================================================

set -e

echo "========================================================="
echo "🚀 Installing Espressif QEMU for ESP32 (Xtensa + OpenETH)"
echo "========================================================="

python3 tools/install_qemu.py || python tools/install_qemu.py
