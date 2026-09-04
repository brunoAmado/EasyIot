#!/usr/bin/env python3
"""Runner script for Espressif QEMU ESP32 emulation with OpenETH virtual networking.

This script compiles the firmware, merges the bootloader, partitions, and application
into a bootable flash image, and starts Espressif QEMU with port forwarding so you can
access the Web Server from your browser at http://localhost:<port>.

Usage:
    python tools/run_qemu.py [--env ESP32_DEBUG] [--port 8080] [--build]
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def log(msg: str, color: str = "") -> None:
    prefixes = {
        "cyan": "[QEMU]",
        "green": "[SUCCESS]",
        "yellow": "[WARN]",
        "red": "[ERROR]"
    }
    prefix = prefixes.get(color, "[QEMU]")
    print(f"{prefix} {msg}")


def find_qemu_executable() -> str | None:
    """Find qemu-system-xtensa on PATH or in standard directories."""
    found = shutil.which("qemu-system-xtensa") or shutil.which("qemu-system-xtensa.exe")
    if found:
        return found

    user_home = Path(os.environ.get("USERPROFILE", os.environ.get("HOME", ".")))
    candidates = [
        user_home / ".espressif" / "qemu" / "bin" / "qemu-system-xtensa.exe",
        user_home / ".espressif" / "qemu" / "bin" / "qemu-system-xtensa",
        user_home / ".espressif" / "tools" / "qemu" / "bin" / "qemu-system-xtensa.exe",
        Path("C:/dev_tools/qemu-esp32/bin/qemu-system-xtensa.exe"),
        Path("C:/Program Files/qemu-esp32/bin/qemu-system-xtensa.exe"),
        Path("/opt/qemu-esp32/bin/qemu-system-xtensa"),
        Path("/usr/local/bin/qemu-system-xtensa"),
    ]
    for p in candidates:
        if p.exists():
            return str(p)

    # Search recursively in .espressif if present
    espressif_dir = user_home / ".espressif"
    if espressif_dir.exists():
        for p in espressif_dir.rglob("qemu-system-xtensa*"):
            if p.is_file() and not p.name.endswith(".zip"):
                return str(p)

    return None


def find_pio_cmd() -> list[str]:
    """Locate PlatformIO executable."""
    found = shutil.which("pio") or shutil.which("pio.exe")
    if found:
        return [found]
    candidates = [
        Path("C:/dev_tools/Python311/Scripts/pio.exe"),
        Path("C:/dev_tools/Python312/Scripts/pio.exe"),
        ROOT / ".venv" / "Scripts" / "pio.exe",
    ]
    for p in candidates:
        if p.exists():
            return [str(p)]
    return [sys.executable, "-m", "platformio"]


def find_esptool_cmd() -> list[str]:
    """Find esptool for merging binary images."""
    found = shutil.which("esptool.py") or shutil.which("esptool.exe")
    if found:
        return [found]

    user_home = Path(os.environ.get("USERPROFILE", os.environ.get("HOME", ".")))
    pio_packages = user_home / ".platformio" / "packages"
    if pio_packages.exists():
        for p in pio_packages.rglob("esptool.py"):
            if p.is_file():
                return [sys.executable, str(p)]

    # Fallback to python module
    return [sys.executable, "-m", "esptool"]


def build_firmware(env: str) -> bool:
    """Build PlatformIO environment."""
    log(f"Compiling firmware for environment '{env}'...", "cyan")
    pio_cmd = find_pio_cmd() + ["run", "-e", env]
    res = subprocess.run(pio_cmd, cwd=ROOT)
    return res.returncode == 0


def find_firmware_binary(env: str) -> Path | None:
    """Find the compiled application firmware binary, handling versioned filenames."""
    build_dir = ROOT / ".pio" / "build" / env
    if not build_dir.exists():
        return None
    canonical = build_dir / "firmware.bin"
    if canonical.exists():
        return canonical
    candidates = [
        p for p in build_dir.glob("*.bin")
        if p.name not in ("bootloader.bin", "partitions.bin", "qemu_flash.bin")
    ]
    if candidates:
        latest = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        try:
            shutil.copy2(latest, canonical)
            return canonical
        except Exception:
            return latest
    return None


def create_merged_flash_image(env: str) -> Path | None:
    """Merge bootloader, partitions, and app firmware into a unified QEMU flash image."""
    build_dir = ROOT / ".pio" / "build" / env
    bootloader = build_dir / "bootloader.bin"
    partitions = build_dir / "partitions.bin"
    firmware = find_firmware_binary(env)
    output_flash = build_dir / "qemu_flash.bin"

    if not bootloader.exists() or not partitions.exists() or not firmware or not firmware.exists():
        log(f"Missing build artifacts in {build_dir}. Bootloader, partitions, or firmware binary not found.", "red")
        return None

    flash_size_str = "4MB" if "4m" in env.lower() or "qemu" in env.lower() else "8MB"
    flash_size_bytes = (4 if flash_size_str == "4MB" else 8) * 1024 * 1024

    log(f"Merging flash binaries ({firmware.name}) into {output_flash.name} ({flash_size_str} flash)...", "cyan")
    esptool = find_esptool_cmd()
    cmd = esptool + [
        "--chip", "esp32",
        "merge_bin",
        "-o", str(output_flash),
        "--flash_mode", "dio",
        "--flash_size", flash_size_str,
        "0x1000", str(bootloader),
        "0x8000", str(partitions),
        "0x10000", str(firmware)
    ]

    try:
        res = subprocess.run(cmd, cwd=ROOT)
        if res.returncode == 0 and output_flash.exists():
            log(f"Successfully generated merged flash image: {output_flash} ({output_flash.stat().st_size // 1024} KB)", "green")
            return output_flash
    except Exception as e:
        log(f"esptool merge_bin failed: {e}", "red")

    # Fallback: manual binary concatenation if esptool module is not directly callable
    log("Attempting direct binary padding & merge...", "yellow")
    try:
        flash_data = bytearray([0xFF] * flash_size_bytes)

        def write_at(offset: int, filepath: Path) -> None:
            data = filepath.read_bytes()
            flash_data[offset:offset + len(data)] = data

        write_at(0x1000, bootloader)
        write_at(0x8000, partitions)
        write_at(0x10000, firmware)

        output_flash.write_bytes(flash_data)
        log(f"Generated {flash_size_str} flash image manually: {output_flash}", "green")
        return output_flash
    except Exception as e:
        log(f"Manual flash merge failed: {e}", "red")
        return None


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Run EasyIot ESP32 in Espressif QEMU with virtual networking")
    parser.add_argument("--env", default="ESP32_QEMU", help="PlatformIO environment (default: ESP32_QEMU)")
    parser.add_argument("--port", type=int, default=8080, help="Host HTTP port to forward to ESP32 port 80 (default: 8080)")
    parser.add_argument("--build", action="store_true", help="Force rebuild before launching QEMU")
    parser.add_argument("--install", action="store_true", help="Install Espressif QEMU automatically if missing")
    args = parser.parse_args()

    build_dir = ROOT / ".pio" / "build" / args.env
    flash_img = build_dir / "qemu_flash.bin"
    firmware = find_firmware_binary(args.env)

    if args.build or not flash_img.exists() or not firmware or not firmware.exists():
        if not build_firmware(args.env):
            log(f"Build failed for environment {args.env}", "red")
            return 1
        flash_img = create_merged_flash_image(args.env)
    elif not flash_img.exists():
        flash_img = create_merged_flash_image(args.env)

    if not flash_img or not flash_img.exists():
        log("Could not prepare QEMU flash image.", "red")
        return 1

    qemu_bin = find_qemu_executable()
    if not qemu_bin:
        log("Espressif QEMU (qemu-system-xtensa) not found.", "yellow")
        installer = ROOT / "tools" / "install_qemu.py"
        if args.install or installer.exists():
            log("Running installer (tools/install_qemu.py)...", "cyan")
            subprocess.run([sys.executable, str(installer)], cwd=ROOT)
            qemu_bin = find_qemu_executable()

        if not qemu_bin:
            log("Please install Espressif QEMU from: https://github.com/espressif/qemu/releases", "red")
            log(f"Merged flash binary is ready at: {flash_img}", "green")
            return 0

    log("=========================================================", "cyan")
    log("🚀 Launching Espressif QEMU with Virtual OpenETH Network", "cyan")
    log(f"🌐 Web Server Forwarding: http://localhost:{args.port} -> ESP32:80", "green")
    log("⌨️  Press Ctrl+A then X to exit QEMU.", "yellow")
    log("=========================================================", "cyan")

    cmd = [
        qemu_bin,
        "-nographic",
        "-machine", "esp32",
        "-drive", f"file={flash_img},if=mtd,format=raw",
        "-net", "nic,model=open_eth",
        "-net", f"user,id=net0,hostfwd=tcp::{args.port}-:80",
    ]

    try:
        return subprocess.run(cmd, cwd=ROOT).returncode
    except KeyboardInterrupt:
        log("\nQEMU emulation stopped by user.", "cyan")
        return 0


if __name__ == "__main__":
    sys.exit(main())
