#!/usr/bin/env python3
"""Cross-platform installer for Espressif QEMU (ESP32 Xtensa emulator with virtual networking).

Supports Windows, Linux, and macOS.

Usage:
    python tools/install_qemu.py
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INSTALL_DIR = Path(os.environ.get("USERPROFILE", os.environ.get("HOME", "."))) / ".espressif" / "qemu"


def log(msg: str, color: str = "") -> None:
    prefixes = {
        "cyan": "[INFO]",
        "green": "[SUCCESS]",
        "yellow": "[WARN]",
        "red": "[ERROR]"
    }
    prefix = prefixes.get(color, "[INSTALL]")
    print(f"{prefix} {msg}")


def find_qemu_executable() -> str | None:
    """Check if qemu-system-xtensa is available on PATH or standard install locations."""
    found = shutil.which("qemu-system-xtensa") or shutil.which("qemu-system-xtensa.exe")
    if found:
        return found

    # Check Espressif standard install directory
    candidates = [
        DEFAULT_INSTALL_DIR / "bin" / "qemu-system-xtensa.exe",
        DEFAULT_INSTALL_DIR / "bin" / "qemu-system-xtensa",
        Path("C:/dev_tools/qemu-esp32/bin/qemu-system-xtensa.exe"),
        Path("C:/Program Files/qemu-esp32/bin/qemu-system-xtensa.exe"),
        Path("/opt/qemu-esp32/bin/qemu-system-xtensa"),
        Path("/usr/local/bin/qemu-system-xtensa"),
    ]
    for p in candidates:
        if p.exists():
            return str(p)

    return None


def get_latest_qemu_release() -> dict | None:
    """Query GitHub API for latest Espressif QEMU release."""
    api_url = "https://api.github.com/repos/espressif/qemu/releases/latest"
    req = urllib.request.Request(api_url, headers={"User-Agent": "EasyIot-QEMU-Installer"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        log(f"GitHub API query failed: {e}", "yellow")
        # Fallback to releases list if latest is a draft/tag
        try:
            list_url = "https://api.github.com/repos/espressif/qemu/releases"
            req2 = urllib.request.Request(list_url, headers={"User-Agent": "EasyIot-QEMU-Installer"})
            with urllib.request.urlopen(req2, timeout=15) as resp:
                releases = json.loads(resp.read().decode())
                if releases:
                    return releases[0]
        except Exception:
            pass
    return None


def install_qemu() -> bool:
    """Download and extract Espressif QEMU for the current OS/architecture."""
    log("Checking latest Espressif QEMU release from GitHub...", "cyan")
    release_data = get_latest_qemu_release()
    if not release_data:
        log("Could not fetch release metadata from https://github.com/espressif/qemu", "red")
        return False

    system = platform.system().lower()
    machine = platform.machine().lower()

    target_pattern = ""
    if system == "windows":
        target_pattern = "mingw32"
    elif system == "darwin":
        if "arm" in machine or "aarch64" in machine:
            target_pattern = "aarch64-apple-darwin"
        else:
            target_pattern = "apple-darwin"
    elif system == "linux":
        if "aarch64" in machine or "arm64" in machine:
            target_pattern = "aarch64-linux-gnu"
        else:
            target_pattern = "x86_64-linux-gnu"

    chosen_asset = None
    for asset in release_data.get("assets", []):
        name = asset.get("name", "").lower()
        if "xtensa" in name and target_pattern in name:
            chosen_asset = asset
            break

    if not chosen_asset:
        # Fallback to any matching OS asset
        for asset in release_data.get("assets", []):
            name = asset.get("name", "").lower()
            if target_pattern in name:
                chosen_asset = asset
                break

    if not chosen_asset:
        log(f"No binary asset found for OS: {system}, architecture: {machine}", "red")
        log("Please visit https://github.com/espressif/qemu/releases to download manually.", "yellow")
        return False

    download_url = chosen_asset["browser_download_url"]
    filename = chosen_asset["name"]
    download_dest = ROOT / "tools" / filename

    log(f"Downloading {chosen_asset['name']} ({chosen_asset.get('size', 0) // (1024*1024)} MB)...", "cyan")
    try:
        urllib.request.urlretrieve(download_url, download_dest)
    except Exception as e:
        log(f"Download failed: {e}", "red")
        return False

    log(f"Extracting to {DEFAULT_INSTALL_DIR}...", "cyan")
    DEFAULT_INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        if filename.endswith(".zip"):
            with zipfile.ZipFile(download_dest, "r") as zf:
                zf.extractall(DEFAULT_INSTALL_DIR)
        elif filename.endswith(".tar.xz") or filename.endswith(".tar.gz") or filename.endswith(".tgz"):
            with tarfile.open(download_dest, "r:*") as tf:
                tf.extractall(DEFAULT_INSTALL_DIR)
    except Exception as e:
        log(f"Extraction failed: {e}", "red")
        return False
    finally:
        if download_dest.exists():
            download_dest.unlink()

    # If extracted into a subfolder (e.g. qemu/), adjust or symlink
    bin_path = find_qemu_executable()
    if bin_path:
        log(f"Espressif QEMU installed successfully at: {bin_path}", "green")
        if system == "windows":
            qemu_bin_dir = str(Path(bin_path).parent)
            log(f"Add this directory to your PATH: {qemu_bin_dir}", "cyan")
        return True

    # Search extracted directory for qemu-system-xtensa
    for p in DEFAULT_INSTALL_DIR.rglob("qemu-system-xtensa*"):
        if p.is_file() and not p.name.endswith(".zip"):
            log(f"Found QEMU executable at: {p}", "green")
            return True

    log("Extracted files but could not locate qemu-system-xtensa executable.", "yellow")
    return False


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    log("==================================================", "cyan")
    log("🚀 Espressif QEMU Installer for EasyIot", "cyan")
    log("==================================================", "cyan")

    existing = find_qemu_executable()
    if existing:
        log(f"Espressif QEMU is already installed at: {existing}", "green")
        log("You can start emulating with: python tools/run_qemu.py", "cyan")
        return 0

    if install_qemu():
        log("🎉 Espressif QEMU installation complete! Ready to emulate ESP32 with virtual networking.", "green")
        return 0
    else:
        log("❌ Installation could not be completed automatically.", "red")
        log("Visit https://github.com/espressif/qemu/releases for manual setup.", "yellow")
        return 1


if __name__ == "__main__":
    sys.exit(main())
