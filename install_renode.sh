#!/usr/bin/env bash
# install_renode.sh
# Automated installer for Antmicro Renode on Linux and macOS

set -e

echo "=================================================="
echo "🚀 Installing Renode Hardware Emulator (Linux/macOS)"
echo "=================================================="

PYTHON_BIN="python3"
if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
fi

$PYTHON_BIN tools/install_renode.py
