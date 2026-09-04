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
RENODE_DIR = ROOT / "emulation"
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


def find_pio_cmd() -> list[str]:
    # 1. Check venv Scripts
    venv_pio = ROOT / ".venv" / "Scripts" / "pio.exe"
    if venv_pio.exists():
        return [str(venv_pio)]
    found = shutil.which("pio")
    if found:
        return [found]
    # 2. Check python module
    return [sys.executable, "-m", "platformio"]


def find_elf_binary(env: str) -> Path | None:
    build_dir = ROOT / ".pio" / "build" / env
    if not build_dir.exists():
        return None
    canonical = build_dir / "firmware.elf"
    if canonical.exists():
        return canonical
    elf_files = sorted(build_dir.glob("*.elf"), key=lambda p: p.stat().st_mtime, reverse=True)
    if elf_files:
        try:
            shutil.copy2(elf_files[0], canonical)
            return canonical
        except Exception:
            return elf_files[0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run EasyIot in Renode hardware emulator")
    parser.add_argument("--env", default="ESP32_DEBUG", help="PlatformIO environment to build and run (default: ESP32_DEBUG)")
    parser.add_argument("--build", action="store_true", help="Force PlatformIO compilation before running Renode")
    parser.add_argument("--headless", action="store_true", help="Run in headless batch mode without GUI")
    parser.add_argument("--test", action="store_true", help="Run automated Robot Framework test suite")
    args = parser.parse_args()

    # Reconfigure stdout for utf-8 if possible
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    elf_path = find_elf_binary(args.env)

    # Compile if requested or if binary is missing
    if args.build or elf_path is None or not elf_path.exists():
        print(f"[BUILD] Compiling {args.env} firmware binary using PlatformIO...")
        pio_cmd = find_pio_cmd() + ["run", "-e", args.env]
        res = subprocess.run(pio_cmd, cwd=ROOT)
        if res.returncode != 0:
            print(f"[ERROR] Build failed for environment {args.env}")
            return res.returncode
        elf_path = find_elf_binary(args.env)

    if elf_path is None or not elf_path.exists():
        print(f"[ERROR] Could not find firmware ELF binary in .pio/build/{args.env}/")
        return 1

    renode_bin = find_renode_executable(headless=args.test or args.headless)
    if not renode_bin:
        print("[WARN] Renode executable was not found on your system PATH or Program Files.")
        print("[INFO] Download & install Renode from: https://github.com/renode/renode/releases")
        print(f"[OK] PlatformIO binary is ready at: {elf_path}")
        return 0

    print(f"[RENODE] Starting Renode ({renode_bin}) with script: {SCRIPT_PATH}...")
    elf_posix = elf_path.as_posix()
    if args.test:
        cmd = [renode_bin, "-e", f"$bin=@{elf_posix}", str(ROBOT_TEST_PATH)]
    else:
        cmd = [renode_bin, "--plain", "-e", f"$bin=@{elf_posix}", str(SCRIPT_PATH)]

    try:
        return subprocess.run(cmd, cwd=ROOT).returncode
    except KeyboardInterrupt:
        print("\n[RENODE] Emulation stopped by user.")
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
