#!/usr/bin/env python3
"""Cross-platform installer for Antmicro Renode hardware emulator.

Supports Windows, Linux (Ubuntu/Debian, Fedora, Arch, Generic), and macOS.

Usage:
    python tools/install_renode.py
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
import urllib.request
import json

ROOT = Path(__file__).resolve().parents[1]


def log(msg: str, color: str = "") -> None:
    prefixes = {
        "cyan": "[INFO]",
        "green": "[SUCCESS]",
        "yellow": "[WARN]",
        "red": "[ERROR]"
    }
    prefix = prefixes.get(color, "[INSTALL]")
    print(f"{prefix} {msg}")


def is_renode_installed() -> bool:
    """Check if Renode is already available on PATH or standard locations."""
    if shutil.which("renode") or shutil.which("renode.exe"):
        return True
    
    system = platform.system()
    if system == "Windows":
        win_paths = [
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Renode" / "bin" / "renode.exe",
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Renode" / "renode.exe",
            Path(os.environ.get("LOCALAPPDATA", r"C:\Users\Default\AppData\Local")) / "Programs" / "Renode" / "renode.exe",
        ]
        return any(p.exists() for p in win_paths)
    elif system == "Darwin":
        return Path("/Applications/Renode.app").exists()
    elif system == "Linux":
        return Path("/opt/renode/renode").exists()
    return False


def install_windows() -> bool:
    """Install Renode on Windows via winget, choco, or direct GitHub MSI."""
    log("Detecting Windows installation methods...", "cyan")

    # 1. Try winget
    if shutil.which("winget"):
        log("Installing Renode via Windows Package Manager (winget)...", "cyan")
        cmd = ["winget", "install", "Renode.Renode", "--accept-package-agreements", "--accept-source-agreements"]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            log("Renode installed successfully via winget!", "green")
            return True
        log("winget installation encountered an issue, trying Chocolatey...", "yellow")

    # 2. Try choco
    if shutil.which("choco"):
        log("Installing Renode via Chocolatey...", "cyan")
        cmd = ["choco", "install", "renode", "-y"]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            log("Renode installed successfully via Chocolatey!", "green")
            return True

    # 3. Direct GitHub Releases download and install
    log("Installing Renode via direct GitHub Releases MSI installer...", "cyan")
    try:
        api_url = "https://api.github.com/repos/renode/renode/releases/latest"
        req = urllib.request.Request(api_url, headers={"User-Agent": "EasyIot-Renode-Installer"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        msi_asset = None
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name.endswith(".msi") or (name.endswith(".exe") and "windows" in name.lower()):
                msi_asset = asset
                break
        
        if not msi_asset:
            log("Could not find Windows installer asset in latest release.", "red")
            return False

        download_url = msi_asset["browser_download_url"]
        temp_installer = ROOT / "tools" / msi_asset["name"]
        log(f"Downloading {download_url}...", "cyan")
        urllib.request.urlretrieve(download_url, temp_installer)

        log("Running MSI installer...", "cyan")
        cmd = ["msiexec.exe", "/i", str(temp_installer), "/qn", "/norestart"]
        res = subprocess.run(cmd)
        
        if temp_installer.exists():
            temp_installer.unlink()

        if res.returncode == 0:
            log("Renode installed successfully via MSI!", "green")
            return True
        else:
            log(f"MSI installer exited with code {res.returncode}", "red")
            return False
    except Exception as e:
        log(f"Failed to install Renode: {e}", "red")
        return False


def install_macos() -> bool:
    """Install Renode on macOS via Homebrew or DMG."""
    log("Detecting macOS installation methods...", "cyan")

    if shutil.which("brew"):
        log("Installing Renode via Homebrew Cask...", "cyan")
        cmd = ["brew", "install", "--cask", "renode"]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            log("Renode installed successfully via Homebrew!", "green")
            return True

    log("Homebrew not found. Please install Homebrew or download Renode from:", "yellow")
    log("https://github.com/renode/renode/releases", "cyan")
    return False


def install_linux() -> bool:
    """Install Renode on Linux via package managers or GitHub binary package."""
    log("Detecting Linux distribution...", "cyan")

    # 1. Debian / Ubuntu
    if shutil.which("apt-get"):
        log("Installing Renode on Debian/Ubuntu...", "cyan")
        try:
            api_url = "https://api.github.com/repos/renode/renode/releases/latest"
            req = urllib.request.Request(api_url, headers={"User-Agent": "EasyIot-Renode-Installer"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())

            deb_asset = next((a for a in data.get("assets", []) if a["name"].endswith(".deb")), None)
            if deb_asset:
                download_url = deb_asset["browser_download_url"]
                deb_file = ROOT / "tools" / deb_asset["name"]
                log(f"Downloading {download_url}...", "cyan")
                urllib.request.urlretrieve(download_url, deb_file)
                subprocess.run(["sudo", "apt-get", "update"])
                res = subprocess.run(["sudo", "apt-get", "install", "-y", str(deb_file)])
                if deb_file.exists():
                    deb_file.unlink()
                if res.returncode == 0:
                    log("Renode installed successfully on Debian/Ubuntu!", "green")
                    return True
        except Exception as e:
            log(f"Automatic Debian package install failed: {e}", "yellow")

    # 2. Arch Linux
    if shutil.which("yay"):
        log("Installing Renode via AUR (yay)...", "cyan")
        res = subprocess.run(["yay", "-S", "--noconfirm", "renode-bin"])
        if res.returncode == 0:
            log("Renode installed successfully via yay!", "green")
            return True

    # 3. Fedora / RHEL
    if shutil.which("dnf"):
        log("Installing Renode on Fedora/RHEL...", "cyan")
        res = subprocess.run(["sudo", "dnf", "install", "-y", "renode"])
        if res.returncode == 0:
            log("Renode installed successfully via DNF!", "green")
            return True

    log("Could not find automated package manager. Please download Renode Linux package from:", "yellow")
    log("https://github.com/renode/renode/releases", "cyan")
    return False


def main() -> int:
    # Reconfigure stdout for utf-8 if possible
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    log("==================================================", "cyan")
    log("🚀 Antmicro Renode Emulator Installer for EasyIot", "cyan")
    log("==================================================", "cyan")

    if is_renode_installed():
        log("Renode is already installed on this machine!", "green")
        log("You can start emulating with: python tools/run_renode.py", "cyan")
        return 0

    system = platform.system()
    success = False
    if system == "Windows":
        success = install_windows()
    elif system == "Darwin":
        success = install_macos()
    elif system == "Linux":
        success = install_linux()
    else:
        log(f"Unsupported operating system: {system}", "red")
        return 1

    if success:
        log("🎉 Renode installation complete! Ready to emulate ESP32 hardware.", "green")
        return 0
    else:
        log("❌ Installation could not be completed automatically.", "red")
        log("Please visit https://github.com/renode/renode/releases for manual setup.", "yellow")
        return 1


if __name__ == "__main__":
    sys.exit(main())
