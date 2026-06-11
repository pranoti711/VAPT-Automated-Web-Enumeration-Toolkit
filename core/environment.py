
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, Any

from core.os_detector import (
    get_os,
    is_windows,
    is_linux,
    is_macos,
    get_shell,
    get_path_separator,
)
from core.live_monitor import info, success, warning

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
TOOLS_DIR = PROJECT_ROOT / "tools"
WORDLISTS_DIR = PROJECT_ROOT / "wordlists"
INSTALLERS_DIR = PROJECT_ROOT / "installers"

class EnvironmentManager:
    """
    Cross-platform environment manager.

    Responsibilities:
    -----------------
    - Detect OS and shell
    - Manage PATH
    - Manage GOPATH
    - Manage PYTHONPATH
    - Provide project directories
    - Validate environment readiness
    """

    def __init__(self):
        self.os_name = get_os()
        self.shell = get_shell()
        self.path_separator = get_path_separator()


    def get_environment(self) -> Dict[str, Any]:
        return {
            "os": self.os_name,
            "shell": self.shell,
            "project_root": str(PROJECT_ROOT),
            "outputs_dir": str(OUTPUTS_DIR),
            "tools_dir": str(TOOLS_DIR),
            "wordlists_dir": str(WORDLISTS_DIR),
            "installers_dir": str(INSTALLERS_DIR),
            "python_executable": sys.executable,
            "path_separator": self.path_separator,
        }


    def create_directories(self) -> None:
        dirs = [
            OUTPUTS_DIR,
            OUTPUTS_DIR / "logs",
            OUTPUTS_DIR / "cache",
            OUTPUTS_DIR / "sessions",
            OUTPUTS_DIR / "scans",
            TOOLS_DIR,
            WORDLISTS_DIR,
            INSTALLERS_DIR,
        ]

        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)

        success("Environment directories ready")

    def add_to_path(self, path: str | Path) -> None:
        path = str(Path(path).resolve())

        current_path = os.environ.get("PATH", "")

        paths = current_path.split(self.path_separator)

        if path not in paths:
            os.environ["PATH"] = (
                path + self.path_separator + current_path
            )

    def setup_go_path(self) -> None:
        home = Path.home()

        go_path = home / "go"
        go_bin = go_path / "bin"

        os.environ.setdefault("GOPATH", str(go_path))

        self.add_to_path(go_bin)

    def setup_python_path(self) -> None:
        current_pythonpath = os.environ.get("PYTHONPATH", "")

        root = str(PROJECT_ROOT)

        if root not in current_pythonpath.split(self.path_separator):
            os.environ["PYTHONPATH"] = (
                root
                + self.path_separator
                + current_pythonpath
            )

    def setup_environment(self) -> None:
        info("Setting up framework environment...")

        self.create_directories()
        self.setup_go_path()
        self.setup_python_path()

        success("Environment setup completed")


    def get_installer_path(self) -> Path:
        if is_windows():
            return INSTALLERS_DIR / "windows"

        if is_linux():
            return INSTALLERS_DIR / "linux"

        if is_macos():
            return INSTALLERS_DIR / "macos"

        return INSTALLERS_DIR

    def get_tools_installer_script(self) -> Path:
        installer_dir = self.get_installer_path()

        if is_windows():
            return installer_dir / "tools_installer.ps1"

        return installer_dir / "tools_installer.sh"

    def get_go_setup_script(self) -> Path:
        installer_dir = self.get_installer_path()

        if is_windows():
            return installer_dir / "go_setup.ps1"

        return installer_dir / "go_setup.sh"

    def get_python_setup_script(self) -> Path:
        installer_dir = self.get_installer_path()

        if is_windows():
            return installer_dir / "python_setup.ps1"

        return installer_dir / "python_setup.sh"

    def validate(self) -> bool:
        info("Validating environment...")

        if self.os_name == "unknown":
            warning("Unsupported OS detected")
            return False

        if not PROJECT_ROOT.exists():
            warning("Project root not found")
            return False

        if not WORDLISTS_DIR.exists():
            warning("Wordlists directory missing")

        success("Environment validation completed")
        return True

    def show(self) -> None:
        env = self.get_environment()

        info("Environment Information")

        for key, value in env.items():
            print(f"{key:<20}: {value}")

environment_manager = EnvironmentManager()

def setup_environment() -> None:
    environment_manager.setup_environment()


def set_environment(os_name: str | None = None) -> None:
    """
    Compatibility helper for old main.py.
    If os_name is passed, it is accepted but runtime OS detection is still used.
    """

    if os_name:
        info(f"Selected environment: {os_name}")

    environment_manager.setup_environment()


def get_environment() -> Dict[str, Any]:
    return environment_manager.get_environment()


def get_current_os() -> str:
    return environment_manager.os_name


def get_os_name() -> str:
    return environment_manager.os_name


def get_os() -> str:
    return environment_manager.os_name


def show_environment() -> None:
    environment_manager.show()


def validate_environment() -> bool:
    return environment_manager.validate()


def get_project_root() -> Path:
    return PROJECT_ROOT


def get_outputs_dir() -> Path:
    return OUTPUTS_DIR


def get_tools_dir() -> Path:
    return TOOLS_DIR


def get_wordlists_dir() -> Path:
    return WORDLISTS_DIR