

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from core.logger import Logger


class ReportGenerator:
    """
    Generates JSON, TXT, Markdown, and CSV reports.
    """

    def __init__(self, scan_root: str | Path):
        self.scan_root = Path(scan_root)
        self.reports_dir = self.scan_root / "reports"
        self.exports_dir = self.scan_root / "exports"
        self.metadata_dir = self.scan_root / "metadata"

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        self.logger = Logger(self.scan_root / "logs")

    def _count(self, data: Dict[str, Any], key: str) -> int:
        value = data.get(key, [])
        return len(value) if isinstance(value, (list, dict)) else 0

    def generate_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "target": data.get("target", ""),
            "generated_at": datetime.now().isoformat(),
            "subdomains": self._count(data, "subdomains"),
            "alive_hosts": self._count(data, "alive_hosts"),
            "urls": self._count(data, "urls"),
            "parameters": self._count(data, "parameters"),
            "directories": self._count(data, "directories"),
            "technologies": self._count(data, "technologies"),
            "sensitive_files": self._count(data, "sensitive_files"),
            "api_endpoints": self._count(data, "api_endpoints"),
        }

    def save_json(self, filename: str, data: Dict[str, Any]) -> Path:
        path = self.reports_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        self.logger.success(f"JSON report saved: {path}")
        return path

    def save_txt(self, filename: str, content: str) -> Path:
        path = self.reports_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", errors="ignore")

        self.logger.success(f"TXT report saved: {path}")
        return path

    def save_markdown(self, filename: str, content: str) -> Path:
        path = self.exports_dir / "markdown" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", errors="ignore")

        self.logger.success(f"Markdown report saved: {path}")
        return path

    def save_csv(self, filename: str, rows: List[Dict[str, Any]]) -> Path:
        path = self.exports_dir / "csv" / filename
        path.parent.mkdir(parents=True, exist_ok=True)

        if not rows:
            path.write_text("", encoding="utf-8")
            return path

        fieldnames = sorted(rows[0].keys())

        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        self.logger.success(f"CSV export saved: {path}")
        return path

    def generate_summary_text(self, data: Dict[str, Any]) -> str:
        stats = self.generate_statistics(data)

        return f"""
========================================
VAPT RECON SUMMARY
========================================

Target:
{stats["target"]}

Generated At:
{stats["generated_at"]}

----------------------------------------

Subdomains:
{stats["subdomains"]}

Alive Hosts:
{stats["alive_hosts"]}

URLs:
{stats["urls"]}

Parameters:
{stats["parameters"]}

Directories:
{stats["directories"]}

Technologies:
{stats["technologies"]}

Sensitive Files:
{stats["sensitive_files"]}

API Endpoints:
{stats["api_endpoints"]}

========================================
"""

    def generate_markdown_report(self, data: Dict[str, Any]) -> str:
        stats = self.generate_statistics(data)

        md = [
            "# VAPT Recon Report",
            "",
            f"**Target:** `{stats['target']}`",
            f"**Generated At:** `{stats['generated_at']}`",
            "",
            "## Summary",
            "",
            f"- Subdomains: **{stats['subdomains']}**",
            f"- Alive Hosts: **{stats['alive_hosts']}**",
            f"- URLs: **{stats['urls']}**",
            f"- Parameters: **{stats['parameters']}**",
            f"- Directories: **{stats['directories']}**",
            f"- Technologies: **{stats['technologies']}**",
            f"- Sensitive Files: **{stats['sensitive_files']}**",
            f"- API Endpoints: **{stats['api_endpoints']}**",
            "",
        ]

        sections = [
            ("Subdomains", "subdomains"),
            ("Alive Hosts", "alive_hosts"),
            ("URLs", "urls"),
            ("Parameters", "parameters"),
            ("Directories", "directories"),
            ("Technologies", "technologies"),
            ("Sensitive Files", "sensitive_files"),
            ("API Endpoints", "api_endpoints"),
        ]

        for title, key in sections:
            items = data.get(key, [])

            md.append(f"## {title}")
            md.append("")

            if not items:
                md.append("_No results found._")
                md.append("")
                continue

            for item in items[:500]:
                md.append(f"- `{item}`")

            if len(items) > 500:
                md.append("")
                md.append(f"_Showing first 500 of {len(items)} results._")

            md.append("")

        return "\n".join(md)

    def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        stats = self.generate_statistics(data)

        return f"""
Executive Summary

The recon scan for {stats["target"]} identified {stats["subdomains"]} subdomains, 
{stats["alive_hosts"]} live hosts, {stats["urls"]} URLs, {stats["parameters"]} parameters, 
and {stats["directories"]} directory or content discovery results.

Potentially sensitive files found: {stats["sensitive_files"]}.
API endpoints found: {stats["api_endpoints"]}.

This report should be reviewed manually before any active vulnerability testing.
"""

    def export_lists(self, data: Dict[str, Any]) -> None:
        export_map = {
            "subdomains.txt": data.get("subdomains", []),
            "alive_hosts.txt": data.get("alive_hosts", []),
            "urls.txt": data.get("urls", []),
            "parameters.txt": data.get("parameters", []),
            "directories.txt": data.get("directories", []),
            "sensitive_files.txt": data.get("sensitive_files", []),
            "api_endpoints.txt": data.get("api_endpoints", []),
        }

        txt_dir = self.exports_dir / "txt"
        txt_dir.mkdir(parents=True, exist_ok=True)

        for filename, items in export_map.items():
            path = txt_dir / filename
            path.write_text(
                "\n".join(str(x) for x in items),
                encoding="utf-8",
                errors="ignore",
            )

    def generate_all(self, data: Dict[str, Any]) -> Dict[str, str]:
        self.logger.phase("GENERATING REPORTS")

        stats = self.generate_statistics(data)

        json_path = self.save_json("report.json", data)
        stats_path = self.save_json("statistics.json", stats)

        summary_text = self.generate_summary_text(data)
        summary_path = self.save_txt("summary.txt", summary_text)

        executive_text = self.generate_executive_summary(data)
        executive_path = self.save_txt("executive_summary.txt", executive_text)

        markdown = self.generate_markdown_report(data)
        markdown_path = self.save_markdown("report.md", markdown)

        self.export_lists(data)

        self.logger.success("All reports generated")

        return {
            "json_report": str(json_path),
            "statistics": str(stats_path),
            "summary": str(summary_path),
            "executive_summary": str(executive_path),
            "markdown": str(markdown_path),
        }