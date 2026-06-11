# =========================================
# FILE: core/tool_installer.py
# FINAL TOOL INSTALLER
# =========================================

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, List

from core.logger import Logger
from core.tool_registry import TOOLS


class ToolInstaller:

    def __init__(self):
        self.logger = Logger()
        self.os_name = self._detect_os()

        self.project_root = Path(__file__).resolve().parents[1]
        self.external_dir = self.project_root / "tools" / "external"
        self.external_dir.mkdir(parents=True, exist_ok=True)

        self.go_bin = Path.home() / "go" / "bin"
        self.cargo_bin = Path.home() / ".cargo" / "bin"
        self.python_scripts = Path(sys.executable).parent / "Scripts"

        self._add_runtime_paths()

    def _detect_os(self) -> str:
        system = platform.system().lower()

        if system == "windows":
            return "windows"
        if system == "linux":
            return "linux"
        if system == "darwin":
            return "macos"

        return "unknown"

    def _add_runtime_paths(self) -> None:
        paths = [
            self.go_bin,
            self.cargo_bin,
            Path(sys.executable).parent,
            self.python_scripts,
        ]

        current_path = os.environ.get("PATH", "")

        for path in paths:
            if path.exists() and str(path) not in current_path:
                os.environ["PATH"] = str(path) + os.pathsep + os.environ.get("PATH", "")

    def _run_command(self, command: str) -> bool:
        self.logger.info(f"Executing: {command}")

        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except Exception as exc:
            self.logger.error(f"Command failed: {exc}")
            return False

    def _binary_exists(self, binary: str | None) -> bool:
        if not binary:
            return False
        if binary == "python":
            return True
        return shutil.which(binary) is not None

    def is_installed(self, tool: Dict) -> bool:
        script_path = tool.get("script_path")

        if script_path:
            return (self.project_root / script_path).exists()

        binary = tool.get("binary", tool.get("name", ""))

        if self._binary_exists(binary):
            return True

        for alt_binary in tool.get("alternative_binaries", []):
            if self._binary_exists(alt_binary):
                return True

        return False

    def _install_subscraper(self) -> bool:
        repo_dir = self.external_dir / "subscraper"
        script_file = repo_dir / "subscraper.py"

        if script_file.exists():
            self.logger.success("Subscraper already installed")

            self._run_command(
                f'"{sys.executable}" -m pip install ipparser taser'
            )

            return True

        if repo_dir.exists():
            shutil.rmtree(repo_dir, ignore_errors=True)

        command = f'git clone https://github.com/m8sec/subscraper.git "{repo_dir}"'

        if not self._run_command(command):
            return False

        requirements = repo_dir / "requirements.txt"

        if requirements.exists():
            self._run_command(
                f'"{sys.executable}" -m pip install -r "{requirements}"'
            )

        self._run_command(
            f'"{sys.executable}" -m pip install ipparser taser'
        )

        if script_file.exists():
            self.logger.success("Subscraper installed successfully")
            return True

        self.logger.error("Subscraper script not found after clone")
        return False

    def _install_paramspider(self) -> bool:
        commands = [
            f'"{sys.executable}" -m pip install git+https://github.com/devanshbatham/ParamSpider.git',
            f'"{sys.executable}" -m pip install paramspider',
        ]

        for command in commands:
            if self._run_command(command):
                self._add_runtime_paths()

                if shutil.which("paramspider") or shutil.which("paramspider.exe"):
                    self.logger.success("ParamSpider installed successfully")
                    return True

        self.logger.warning("ParamSpider install attempted but not verified")
        return False

    def _install_github_subdomains(self) -> bool:
        if not shutil.which("go"):
            self.logger.error("Go is required for github-subdomains")
            return False

        command = "go install github.com/gwen001/github-subdomains@latest"

        if self._run_command(command):
            self._add_runtime_paths()

            if shutil.which("github-subdomains") or shutil.which("github-subdomains.exe"):
                self.logger.success("github-subdomains installed successfully")
                return True

        self.logger.warning("github-subdomains install attempted but not verified")
        return False

    def _install_findomain(self) -> bool:
        if shutil.which("findomain") or shutil.which("findomain.exe"):
            self.logger.success("findomain already installed")
            return True

        base_url = "https://github.com/Edu4rdSHL/findomain/releases/latest/download"
        arch = platform.machine().lower()

        if arch in ["amd64", "x86_64"]:
            arch = "x86_64"
        elif arch in ["aarch64", "arm64"]:
            arch = "aarch64"
        else:
            arch = "x86_64"

        if self.os_name == "windows":
            filename = f"findomain-{arch}-pc-windows-msvc.zip"
            binary_name = "findomain.exe"
        elif self.os_name == "macos":
            filename = f"findomain-{arch}-apple-darwin.zip"
            binary_name = "findomain"
        else:
            filename = f"findomain-{arch}-unknown-linux-musl.zip"
            binary_name = "findomain"

        download_url = f"{base_url}/{filename}"
        temp_zip = self.external_dir / "findomain_temp.zip"

        self.logger.info(f"Downloading findomain from: {download_url}")

        try:
            urllib.request.urlretrieve(download_url, temp_zip)
        except Exception as exc:
            self.logger.error(f"Failed to download findomain: {exc}")
            return False

        try:
            with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                zip_ref.extractall(self.external_dir)

            extracted_bin = self.external_dir / binary_name

            if not extracted_bin.exists():
                for item in self.external_dir.rglob(binary_name):
                    extracted_bin = item
                    break

            if not extracted_bin.exists():
                self.logger.error("findomain binary not found after extraction")
                return False

            if self.os_name != "windows":
                os.chmod(extracted_bin, 0o755)

            target_bin = self.go_bin / binary_name
            target_bin.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(extracted_bin), str(target_bin))

            if temp_zip.exists():
                temp_zip.unlink()

            self._add_runtime_paths()

            if shutil.which("findomain") or shutil.which("findomain.exe"):
                self.logger.success("findomain installed successfully")
                return True

        except Exception as exc:
            self.logger.error(f"Failed to extract/install findomain: {exc}")

        return False

    def _get_install_command(self, tool_name: str) -> str:
        commands = {
            "subfinder": "go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "assetfinder": "go install github.com/tomnomnom/assetfinder@latest",
            "amass": "go install github.com/owasp-amass/amass/v4/...@latest",
            "httpx": "go install github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "gau": "go install github.com/lc/gau/v2/cmd/gau@latest",
            "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
            "katana": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
            "arjun": f'"{sys.executable}" -m pip install arjun',
            "gf": "go install github.com/tomnomnom/gf@latest",
            "ffuf": "go install github.com/ffuf/ffuf/v2@latest",
            "dirsearch": f'"{sys.executable}" -m pip install dirsearch',
        }

        return commands.get(tool_name, "")

    def install_tool(self, tool_name: str) -> bool:
        tool = TOOLS.get(tool_name)

        if not tool:
            self.logger.error(f"Unknown tool: {tool_name}")
            return False

        if tool_name == "subscraper":
            return self._install_subscraper()

        if self.is_installed(tool):
            self.logger.success(f"Already installed: {tool_name}")
            return True

        if tool_name == "paramspider":
            return self._install_paramspider()

        if tool_name == "github-subdomains":
            return self._install_github_subdomains()

        if tool_name == "findomain":
            return self._install_findomain()

        command = self._get_install_command(tool_name)

        if not command:
            self.logger.warning(f"No automatic install command for {tool_name}")
            return False

        self.logger.info(f"Installing {tool_name}...")

        installed = self._run_command(command)
        self._add_runtime_paths()

        if installed and self.is_installed(tool):
            self.logger.success(f"Installed successfully: {tool_name}")
            return True

        self.logger.warning(f"Install attempted but not verified: {tool_name}")
        return False

    def verify_tools(self) -> List[str]:
        missing = []

        self.logger.info("Verifying tool installation...")

        for tool_name, tool in TOOLS.items():
            if self.is_installed(tool):
                self.logger.success(f"Found: {tool_name}")
            else:
                self.logger.warning(f"Missing: {tool_name}")
                missing.append(tool_name)

        return missing

    def install_all(self) -> None:
        self.logger.info("Installing all 15 registered tools...")

        install_order = [
            "subfinder",
            "assetfinder",
            "amass",
            "findomain",
            "github-subdomains",
            "subscraper",
            "httpx",
            "gau",
            "waybackurls",
            "katana",
            "paramspider",
            "arjun",
            "gf",
            "ffuf",
            "dirsearch",
        ]

        for index, tool_name in enumerate(install_order, start=1):
            self.logger.info(f"[{index}/15] Installing/checking {tool_name}")
            self.install_tool(tool_name)

        self.logger.info("Final verification...")

        missing = self.verify_tools()

        if missing:
            self.logger.warning(f"Still missing tools: {missing}")
        else:
            self.logger.success("All 15 tools installed successfully")

    def install_by_category(self, category: str) -> None:
        selected = [
            name
            for name, tool in TOOLS.items()
            if tool.get("category") == category
        ]

        if not selected:
            self.logger.warning(f"No tools found for category: {category}")
            return

        for tool_name in selected:
            self.install_tool(tool_name)

    def generate_report(self) -> Dict[str, bool]:
        return {
            tool_name: self.is_installed(tool)
            for tool_name, tool in TOOLS.items()
        }


def install_all_tools():
    installer = ToolInstaller()
    installer.install_all()


def verify_tools():
    installer = ToolInstaller()
    return installer.verify_tools()


def install_tool(tool_name: str):
    installer = ToolInstaller()
    return installer.install_tool(tool_name)


def install_category(category: str):
    installer = ToolInstaller()
    installer.install_by_category(category)


def generate_install_report():
    installer = ToolInstaller()
    return installer.generate_report()