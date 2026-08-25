#!/usr/bin/env python3
"""Runner script for Renode emulation of EasyIot firmware binaries.

Usage:
    python tools/run_renode.py [--env ESP32_DEBUG] [--headless] [--test]
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RENODE_DIR = ROOT / "renode"
SCRIPT_PATH = RENODE_DIR / "easyiot_esp32.resc"
ROBOT_TEST_PATH = RENODE_DIR / "tests" / "easyiot_boot.robot"


def find_renode_executable(headless: bool = False) -> str | None:
    # 1. Check PATH
    cmd_name = "renode-test" if headless else "renode"
    found = shutil.which(cmd_name)
    if found:
        return found
    found = shutil.which("renode")
    if found:
        return found

    # 2. Check standard Windows installation paths
    win_paths = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Renode" / "bin" / (cmd_name + ".exe"),
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Renode" / "renode.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Renode" / "bin" / (cmd_name + ".exe"),
        Path(os.environ.get("LOCALAPPDATA", r"C:\Users\Default\AppData\Local")) / "Programs" / "Renode" / "renode.exe",
        Path(os.environ.get("USERPROFILE", r"C:\Users\Default")) / "renode" / "renode.exe",
    ]
    for p in win_paths:
        if p.exists():
            return str(p)

    # 3. Check standard Linux/Unix paths
    unix_paths = [
        Path("/usr/bin/renode"),
        Path("/usr/local/bin/renode"),
        Path("/opt/renode/renode"),
    ]
    for p in unix_paths:
        if p.exists():
            return str(p)

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run EasyIot in Renode hardware emulator")
    parser.add_argument("--env", default="ESP32_DEBUG", help="PlatformIO environment to build and run (default: ESP32_DEBUG)")
    parser.add_argument("--build", action="store_true", help="Force PlatformIO compilation before running Renode")
    parser.add_argument("--headless", action="store_true", help="Run in headless batch mode without GUI")
    parser.add_argument("--test", action="store_true", help="Run automated Robot Framework test suite")
    args = parser.parse_args()

    elf_path = ROOT / ".pio" / "build" / args.env / "firmware.elf"

    # Compile if requested or if binary is missing
    if args.build or not elf_path.exists():
        print(f"🔨 Compiling {args.env} firmware binary using PlatformIO...")
        res = subprocess.run(["pio", "run", "-e", args.env], cwd=ROOT)
        if res.returncode != 0:
            print(f"❌ Build failed for environment {args.env}")
            return res.returncode

    renode_bin = find_renode_executable(headless=args.test or args.headless)
    if not renode_bin:
        print("⚠️ Renode executable was not found on your system.")
        print("📥 Download & install Renode from: https://github.com/renode/renode/releases")
        print(f"ℹ️ PlatformIO binary is ready at: {elf_path}")
        return 1

    print(f"🚀 Starting Renode ({renode_bin}) with script: {SCRIPT_PATH}...")
    if args.test:
        cmd = [renode_bin, str(ROBOT_TEST_PATH)]
    else:
        cmd = [renode_bin, "--plain", str(SCRIPT_PATH)]

    return subprocess.run(cmd, cwd=ROOT).returncode


if __name__ == "__main__":
    sys.exit(main())
