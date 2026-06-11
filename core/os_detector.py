
from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Dict

from core.live_monitor import info, success, warning


def get_os() -> str:
    system = platform.system().lower()

    if system == "windows":
        return "windows"

    if system == "linux":
        return "linux"

    if system == "darwin":
        return "macos"

    return "unknown"


def is_windows() -> bool:
    return get_os() == "windows"


def is_linux() -> bool:
    return get_os() == "linux"


def is_macos() -> bool:
    return get_os() == "macos"


def get_shell() -> str:
    if is_windows():
        if os.environ.get("PSModulePath"):
            return "powershell"
        return "cmd"

    shell = os.environ.get("SHELL", "")

    if "zsh" in shell:
        return "zsh"

    if "bash" in shell:
        return "bash"

    return shell or "unknown"


def get_architecture() -> str:
    return platform.machine()


def get_python_version() -> str:
    return sys.version.split()[0]


def get_home_dir() -> Path:
    return Path.home()


def get_current_dir() -> Path:
    return Path.cwd()


def get_system_info() -> Dict[str, str]:
    return {
        "os": get_os(),
        "platform": platform.platform(),
        "architecture": get_architecture(),
        "python_version": get_python_version(),
        "shell": get_shell(),
        "home": str(get_home_dir()),
        "current_dir": str(get_current_dir()),
    }


def show_system_info() -> None:
    info("System Information")

    system_info = get_system_info()

    for key, value in system_info.items():
        print(f"{key:<18}: {value}")

    if system_info["os"] == "unknown":
        warning("Unsupported operating system detected")
    else:
        success(f"Detected OS: {system_info['os']}")


def get_path_separator() -> str:
    return ";" if is_windows() else ":"


def get_executable_extension() -> str:
    return ".exe" if is_windows() else ""


def normalize_path(path: str | Path) -> str:
    return str(Path(path).resolve())


def supports_bash() -> bool:
    return is_linux() or is_macos()


def supports_powershell() -> bool:
    return is_windows()


def get_terminal_clear_command() -> str:
    return "cls" if is_windows() else "clear"