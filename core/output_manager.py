
from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Any


def sanitize_target(target: str) -> str:
    target = (target or "").strip().lower()
    target = re.sub(r"^https?://", "", target, flags=re.IGNORECASE)
    target = target.rstrip("/")
    target = re.sub(r"[^A-Za-z0-9._-]+", "_", target)
    return target or "target"


class OutputManager:
    """
    Centralized scan output manager.
    """

    def __init__(self, target: str):
        self.target = sanitize_target(target)
        self.repo_root = Path(__file__).resolve().parents[1]
        self.scan_root = self.repo_root / "outputs" / "scans" / self.target
        self.create_structure()

    def create_structure(self) -> None:
        folders = [
            self.scan_root,

            self.scan_root / "metadata",
            self.scan_root / "logs",

            self.scan_root / "subdomains" / "raw",
            self.scan_root / "subdomains" / "cleaned",
            self.scan_root / "subdomains" / "final",

            self.scan_root / "httpx" / "raw",
            self.scan_root / "httpx" / "final",

            self.scan_root / "urls" / "raw",
            self.scan_root / "urls" / "cleaned",
            self.scan_root / "urls" / "final",

            self.scan_root / "parameters" / "raw",
            self.scan_root / "parameters" / "cleaned",
            self.scan_root / "parameters" / "final",

            self.scan_root / "directories" / "raw",
            self.scan_root / "directories" / "cleaned",
            self.scan_root / "directories" / "final",

            self.scan_root / "gf_patterns",

            self.scan_root / "javascript" / "raw",
            self.scan_root / "javascript" / "final",

            self.scan_root / "screenshots" / "alive_hosts",
            self.scan_root / "screenshots" / "admin_panels",

            self.scan_root / "technologies",

            self.scan_root / "reports",

            self.scan_root / "exports" / "csv",
            self.scan_root / "exports" / "json",
            self.scan_root / "exports" / "txt",
            self.scan_root / "exports" / "markdown",

            self.scan_root / "temp" / "session",
            self.scan_root / "temp" / "cache",
            self.scan_root / "temp" / "tool_runtime",
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

        self._create_default_metadata()

    def _create_default_metadata(self) -> None:
        self.save_json(
            "metadata/scan_info.json",
            {
                "target": self.target,
                "created_at": str(datetime.now()),
                "framework": "VAPT Automation Framework",
                "version": "2.0",
            },
        )

    def timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def get_path(self, relative_path: str | Path) -> str:
        return str(self.scan_root / relative_path)

    def get_scan_root(self) -> str:
        return str(self.scan_root)

    def exists(self, relative_path: str | Path) -> bool:
        return (self.scan_root / relative_path).exists()

    def save_text(self, relative_path: str | Path, data: Any) -> Path:
        file_path = self.scan_root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, list):
            content = "\n".join(str(x) for x in data)
        else:
            content = str(data)

        file_path.write_text(
            content,
            encoding="utf-8",
            errors="ignore",
        )

        return file_path

    def save_list(self, relative_path: str | Path, data: list[str]) -> Path:
        cleaned = [
            str(x).strip()
            for x in data
            if str(x).strip()
        ]

        return self.save_text(
            relative_path,
            cleaned,
        )

    def append_text(self, relative_path: str | Path, data: str) -> Path:
        file_path = self.scan_root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(
            file_path,
            "a",
            encoding="utf-8",
            errors="ignore",
        ) as f:
            f.write(str(data) + "\n")

        return file_path

    def save_json(self, relative_path: str | Path, data: dict) -> Path:
        file_path = self.scan_root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return file_path

    def load_json(self, relative_path: str | Path) -> dict:
        file_path = self.scan_root / relative_path

        if not file_path.exists():
            return {}

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def save_scan_result(
        self,
        category: str,
        filename: str,
        data: Any,
        final: bool = True,
    ) -> Path:
        folder = "final" if final else "raw"
        relative_path = Path(category) / folder / filename

        if isinstance(data, dict):
            return self.save_json(relative_path, data)

        if isinstance(data, list):
            return self.save_list(relative_path, data)

        return self.save_text(relative_path, data)

    def save_raw_tool_output(
        self,
        category: str,
        tool_name: str,
        output: Any,
    ) -> Path:
        return self.save_text(
            Path(category) / "raw" / f"{tool_name}.txt",
            output,
        )

    def save_export(
        self,
        export_type: str,
        filename: str,
        data: Any,
    ) -> Path:
        return self.save_text(
            Path("exports") / export_type / filename,
            data,
        )

    def save_metadata(self, filename: str, data: dict) -> Path:
        return self.save_json(
            Path("metadata") / filename,
            data,
        )

    def save_report(self, filename: str, data: Any) -> Path:
        if isinstance(data, dict):
            return self.save_json(
                Path("reports") / filename,
                data,
            )

        return self.save_text(
            Path("reports") / filename,
            data,
        )

    def save_subdomains(self, data: list[str]) -> Path:
        return self.save_list(
            "subdomains/final/subdomains_final.txt",
            data,
        )

    def save_alive_hosts(self, data: list[str]) -> Path:
        return self.save_list(
            "httpx/final/alive_hosts.txt",
            data,
        )

    def save_urls(self, data: list[str]) -> Path:
        return self.save_list(
            "urls/final/urls_final.txt",
            data,
        )

    def save_parameters(self, data: list[str]) -> Path:
        return self.save_list(
            "parameters/final/parameters_final.txt",
            data,
        )

    def save_directories(self, data: list[str]) -> Path:
        return self.save_list(
            "directories/final/directories_final.txt",
            data,
        )

    def save_phase_report(
        self,
        phase: str,
        stats: dict,
    ) -> Path:
        return self.save_json(
            f"reports/{phase}_report.json",
            stats,
        )

    def save_subdomain_report(
        self,
        stats: dict,
    ) -> Path:
        return self.save_phase_report(
            "subdomain",
            stats,
        )

    def save_httpx_report(
        self,
        stats: dict,
    ) -> Path:
        return self.save_phase_report(
            "httpx",
            stats,
        )

    def save_url_report(
        self,
        stats: dict,
    ) -> Path:
        return self.save_phase_report(
            "url",
            stats,
        )

    def save_parameter_report(
        self,
        stats: dict,
    ) -> Path:
        return self.save_phase_report(
            "parameter",
            stats,
        )

    def save_directory_report(
        self,
        stats: dict,
    ) -> Path:
        return self.save_phase_report(
            "directory",
            stats,
        )

    def save_gf_report(
        self,
        stats: dict,
    ) -> Path:
        return self.save_phase_report(
            "gf",
            stats,
        )

    def save_final_report(
        self,
        report: dict,
    ) -> Path:
        return self.save_json(
            "reports/final_report.json",
            report,
        )

    def get_subdomains_file(self) -> str:
        return self.get_path(
            "subdomains/final/subdomains_final.txt"
        )

    def get_alive_hosts_file(self) -> str:
        return self.get_path(
            "httpx/final/alive_hosts.txt"
        )

    def get_urls_file(self) -> str:
        return self.get_path(
            "urls/final/urls_final.txt"
        )

    def get_parameters_file(self) -> str:
        return self.get_path(
            "parameters/final/parameters_final.txt"
        )

    def get_directories_file(self) -> str:
        return self.get_path(
            "directories/final/directories_final.txt"
        )


def create_scan_structure(target: str) -> str:
    manager = OutputManager(target)
    return manager.get_scan_root()