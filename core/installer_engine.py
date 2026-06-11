
from __future__ import annotations

import subprocess
from pathlib import Path

from core.live_monitor import (
    info,
    success,
    error,
)

def run_installer(
    os_name: str,
):

    repo_root = Path(__file__).resolve().parents[1]

    try:


        if os_name == "Windows":

            installer = (
                repo_root
                / "installers"
                / "windows"
                / "tools_installer.ps1"
            )

            info("Running Windows Installer")

            subprocess.run(
                [
                    "powershell",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(installer),
                ],
                check=True,
            )


        elif os_name == "Linux":

            installer = (
                repo_root
                / "installers"
                / "linux"
                / "tools_installer.sh"
            )

            info("Running Linux Installer")

            subprocess.run(
                [
                    "bash",
                    str(installer),
                ],
                check=True,
            )


        elif os_name == "macOS":

            installer = (
                repo_root
                / "installers"
                / "mac"
                / "tools_installer.sh"
            )

            info("Running macOS Installer")

            subprocess.run(
                [
                    "bash",
                    str(installer),
                ],
                check=True,
            )

        else:

            error("Unsupported Operating System")

            return False

        success("Installation Completed")

        return True

    except Exception as e:

        error(f"Installation Failed: {e}")

        return False