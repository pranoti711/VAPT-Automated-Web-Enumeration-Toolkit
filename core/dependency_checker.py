
from __future__ import annotations

import importlib
import platform
import shutil
from pathlib import Path
from typing import Any, Dict, List

from core.logger import Logger
from core.tool_installer import ToolInstaller
from core.tool_registry import ALL_TOOLS, TOOLS

FEROXBUSTER_DISABLED = True


class DependencyChecker:
    """Dependency checker with robust tool detection."""

    def __init__(self):
        self.logger = Logger()
        self.installer = ToolInstaller()
        self.project_root = Path(__file__).resolve().parents[1]

    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        return TOOLS.get(tool_name, {})

    def _runtime_platform_key(self) -> str:
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        if system == "linux":
            return "linux"
        if system == "darwin":
            return "macos"
        return "unknown"

    def _binary_exists(self, binary: str | None) -> bool:
        if not binary:
            return False
        if binary == "python":
            return True
        return shutil.which(binary) is not None

    def _alternative_binary_exists(self, binaries: List[str]) -> bool:
        return any(shutil.which(b) for b in binaries if b)

    def _python_module_exists(self, modules: List[str]) -> bool:
        for module in modules:
            try:
                importlib.import_module(module)
                return True
            except Exception:
                continue
        return False

    def _script_exists(self, script_path: str | None) -> bool:
        if not script_path:
            return False
        return (self.project_root / script_path).exists()

    def is_available(self, tool: Dict[str, Any]) -> bool:
        supports = tool.get("supports", {}) or {}

        # Platform check
        if supports:
            platform_key = self._runtime_platform_key()
            if platform_key != "unknown" and not supports.get(platform_key, True):
                return False

        if self._script_exists(tool.get("script_path")):
            return True

        if self._binary_exists(tool.get("binary", tool.get("name", ""))):
            return True

        if self._alternative_binary_exists(tool.get("alternative_binaries", [])):
            return True

        python_modules = tool.get("python_modules", [])
        if not python_modules and tool.get("python_module"):
            python_modules = [tool.get("python_module")]

        if self._python_module_exists(python_modules):
            return True

        return False

    def check_tool(self, tool_name: str) -> bool:
        tool = self.get_tool(tool_name)
        if not tool:
            self.logger.error(f"Unknown tool: {tool_name}")
            return False

        if self.is_available(tool):
            self.logger.success(f"OK: {tool_name}")
            return True

        self.logger.warning(f"MISSING: {tool_name}")
        return False

    def check_all(self) -> Dict[str, List[str]]:
        installed: List[str] = []
        missing: List[str] = []

        self.logger.info("Running dependency check...")

        for tool_name in ALL_TOOLS:
            if FEROXBUSTER_DISABLED and tool_name == "feroxbuster":
                continue

            tool = self.get_tool(tool_name)
            if not tool:
                continue

            if self.is_available(tool):
                installed.append(tool_name)
                self.logger.success(f"OK: {tool_name}")
            else:
                missing.append(tool_name)
                self.logger.warning(f"MISSING: {tool_name}")

        self.logger.info(
            "Dependency check complete | Installed: "
            f"{len(installed)} | Missing: {len(missing)}"
        )

        return {"installed": installed, "missing": missing}

    def check_category(self, category: str) -> Dict[str, List[str]]:
        installed: List[str] = []
        missing: List[str] = []

        for tool_name in ALL_TOOLS:
            if FEROXBUSTER_DISABLED and tool_name == "feroxbuster":
                continue

            tool = self.get_tool(tool_name)
            if not tool or tool.get("category") != category:
                continue

            if self.is_available(tool):
                installed.append(tool_name)
            else:
                missing.append(tool_name)

        return {"installed": installed, "missing": missing}

    def auto_fix(self) -> None:
        report = self.check_all()
        missing_tools = report.get("missing", [])

        if not missing_tools:
            self.logger.success("All dependencies satisfied")
            return

        self.logger.info(f"Installing {len(missing_tools)} missing tools...")

        for tool_name in missing_tools:
            self.installer.install_tool(tool_name)

        if self.check_all().get("missing"):
            self.logger.warning(f"Still missing tools: {self.get_missing_tools()}")
        else:
            self.logger.success("All dependencies fixed successfully")

    def generate_report(self) -> Dict[str, Dict[str, Any]]:
        return {
            tool_name: {
                "name": tool.get("name", tool_name),
                "category": tool.get("category", "unknown"),
                "binary": tool.get("binary", tool_name),
                "alternative_binaries": tool.get("alternative_binaries", []),
                "python_modules": tool.get("python_modules", []),
                "installed": self.is_available(tool),
            }
            for tool_name, tool in TOOLS.items()
            if tool and not (FEROXBUSTER_DISABLED and tool_name == "feroxbuster")
        }

    def require_tools(self, tool_names: List[str]) -> bool:
        missing = [t for t in tool_names if not self.check_tool(t)]
        if missing:
            self.logger.error(f"Required tools missing: {missing}")
            return False
        self.logger.success("All required tools available")
        return True

    def get_missing_tools(self) -> List[str]:
        return self.check_all().get("missing", [])

    def get_installed_tools(self) -> List[str]:
        return self.check_all().get("installed", [])


def verify_tools():
    return DependencyChecker().check_all()


def verify_required_tools() -> bool:
    return len(DependencyChecker().check_all().get("missing", [])) == 0


def auto_fix_dependencies():
    DependencyChecker().auto_fix()


def check_tool(tool_name: str) -> bool:
    return DependencyChecker().check_tool(tool_name)


def check_category(category: str):
    return DependencyChecker().check_category(category)


def generate_dependency_report():
    return DependencyChecker().generate_report()


def require_tools(tool_names: List[str]) -> bool:
    return DependencyChecker().require_tools(tool_names)


def get_missing_tools() -> List[str]:
    return DependencyChecker().get_missing_tools()


def get_installed_tools() -> List[str]:
    return DependencyChecker().get_installed_tools()

