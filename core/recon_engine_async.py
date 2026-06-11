
from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from core.logger import Logger
from core.output_manager import OutputManager
from core.workflow_engine import WorkflowEngine
from core.dependency_checker import DependencyChecker


class ReconEngineAsync:
    """
    Master async recon engine.
    """

    OPTIONAL_TOOLS = {
        "github-subdomains",
        "subscraper",
        "feroxbuster",
    }

    CRITICAL_TOOLS = {
        "subfinder",
        "assetfinder",
        "amass",
        "findomain",
        "httpx",
        "gau",
        "waybackurls",
        "katana",
        "paramspider",
        "arjun",
        "gf",
        "ffuf",
        "dirsearch",
    }

    def __init__(
        self,
        target: str,
        mode: str = "normal",
        verify_tools: bool = True,
    ):
        self.target = target.strip().lower()
        self.mode = mode
        self.verify_tools = verify_tools

        self.start_time = datetime.now()
        self.end_time: datetime | None = None

        self.logger = Logger()
        self.output = OutputManager(self.target)
        self.dependency_checker = DependencyChecker()

        self.scan_root = Path(self.output.get_scan_root())

        self.workflow = WorkflowEngine(
            target=self.target,
            output=self.output,
        )

        self.result: Dict[str, Any] = {}

    async def initialize(self) -> None:
        self.logger.phase("INITIALIZING RECON ENGINE")

        self.output.create_structure()

        self.output.save_json(
            "metadata/scan_info.json",
            {
                "target": self.target,
                "mode": self.mode,
                "scan_root": str(self.scan_root),
                "started_at": str(self.start_time),
                "engine": "ReconEngineAsync",
                "status": "initialized",
                "critical_tools": sorted(self.CRITICAL_TOOLS),
                "optional_tools": sorted(self.OPTIONAL_TOOLS),
            },
        )

        self.logger.success(
            f"Recon engine initialized for {self.target}"
        )

    async def verify_dependencies_phase(self) -> bool:
        self.logger.phase("DEPENDENCY VERIFICATION")

        if not self.verify_tools:
            self.logger.warning("Dependency verification skipped")
            return True

        report = self.dependency_checker.check_all()

        installed = report.get("installed", [])
        missing = report.get("missing", [])

        missing_critical = [
            tool for tool in missing
            if tool in self.CRITICAL_TOOLS
        ]

        missing_optional = [
            tool for tool in missing
            if tool in self.OPTIONAL_TOOLS
        ]

        dependency_report = {
            "installed": installed,
            "missing": missing,
            "missing_critical": missing_critical,
            "missing_optional": missing_optional,
            "critical_tools": sorted(self.CRITICAL_TOOLS),
            "optional_tools": sorted(self.OPTIONAL_TOOLS),
        }

        self.output.save_json(
            "metadata/tools_used.json",
            dependency_report,
        )

        if missing_critical:
            self.logger.warning(
                f"Missing critical tools: {missing_critical}"
            )
            return False

        if missing_optional:
            self.logger.warning(
                f"Optional tools missing, continuing scan: {missing_optional}"
            )

        self.logger.success("All critical tools are available")
        return True

    async def run_workflow(self) -> Dict[str, Any]:
        self.logger.phase("RUNNING WORKFLOW ENGINE")

        result = await self.workflow.run_full_workflow()

        self.logger.success("Workflow execution completed")

        return result

    async def save_execution_metadata(
        self,
        status: str,
    ) -> None:
        self.end_time = datetime.now()
        duration = self.end_time - self.start_time

        self.output.save_json(
            "metadata/execution_time.json",
            {
                "started_at": str(self.start_time),
                "ended_at": str(self.end_time),
                "duration": str(duration),
                "status": status,
            },
        )

        statistics = {
            "target": self.target,
            "mode": self.mode,
            "status": status,
            "subdomains": len(self.result.get("subdomains", [])),
            "alive_hosts": len(self.result.get("alive_hosts", [])),
            "urls": len(self.result.get("urls", [])),
            "parameters": len(self.result.get("parameters", [])),
            "gf_findings": {
                key: len(value)
                for key, value in self.result.get("gf_findings", {}).items()
            },
            "directories": len(self.result.get("directories", [])),
        }

        self.output.save_json(
            "metadata/statistics.json",
            statistics,
        )

    async def generate_phase_reports(self) -> None:
        self.output.save_subdomain_report(
            {
                "target": self.target,
                "count": len(self.result.get("subdomains", [])),
                "output_file": self.output.get_subdomains_file(),
                "generated_at": str(datetime.now()),
            }
        )

        self.output.save_httpx_report(
            {
                "target": self.target,
                "count": len(self.result.get("alive_hosts", [])),
                "output_file": self.output.get_alive_hosts_file(),
                "generated_at": str(datetime.now()),
            }
        )

        self.output.save_url_report(
            {
                "target": self.target,
                "count": len(self.result.get("urls", [])),
                "output_file": self.output.get_urls_file(),
                "generated_at": str(datetime.now()),
            }
        )

        self.output.save_parameter_report(
            {
                "target": self.target,
                "count": len(self.result.get("parameters", [])),
                "output_file": self.output.get_parameters_file(),
                "generated_at": str(datetime.now()),
            }
        )

        self.output.save_gf_report(
            {
                "target": self.target,
                "groups": {
                    key: len(value)
                    for key, value in self.result.get("gf_findings", {}).items()
                },
                "output_folder": self.output.get_path("gf_patterns"),
                "generated_at": str(datetime.now()),
            }
        )

        self.output.save_directory_report(
            {
                "target": self.target,
                "count": len(self.result.get("directories", [])),
                "output_file": self.output.get_directories_file(),
                "generated_at": str(datetime.now()),
            }
        )

        self.output.save_final_report(
            {
                "target": self.target,
                "mode": self.mode,
                "status": self.result.get("status", "completed"),
                "scan_root": str(self.scan_root),
                "subdomains": len(self.result.get("subdomains", [])),
                "alive_hosts": len(self.result.get("alive_hosts", [])),
                "urls": len(self.result.get("urls", [])),
                "parameters": len(self.result.get("parameters", [])),
                "gf_findings": {
                    key: len(value)
                    for key, value in self.result.get("gf_findings", {}).items()
                },
                "directories": len(self.result.get("directories", [])),
                "generated_at": str(datetime.now()),
            }
        )

    async def generate_summary(self) -> None:
        self.logger.phase("GENERATING SUMMARY")

        summary = f"""
========================================
VAPT RECON SUMMARY
========================================

Target:
{self.target}

Mode:
{self.mode}

Subdomains:
{len(self.result.get("subdomains", []))}

Alive Hosts:
{len(self.result.get("alive_hosts", []))}

URLs:
{len(self.result.get("urls", []))}

Parameters:
{len(self.result.get("parameters", []))}

GF Groups:
{len(self.result.get("gf_findings", {}))}

Directories:
{len(self.result.get("directories", []))}

Scan Root:
{self.scan_root}

Files:
Subdomains  : {self.output.get_subdomains_file()}
Alive Hosts : {self.output.get_alive_hosts_file()}
URLs        : {self.output.get_urls_file()}
Parameters  : {self.output.get_parameters_file()}
Directories : {self.output.get_directories_file()}

========================================
"""

        self.output.save_text(
            "reports/summary.txt",
            summary,
        )

        self.logger.success("Summary generated")

    async def cleanup(self) -> None:
        self.logger.phase("CLEANUP")
        self.logger.success("Cleanup completed")

    async def run(self) -> Dict[str, Any]:
        try:
            await self.initialize()

            dependencies_ok = await self.verify_dependencies_phase()

            if not dependencies_ok:
                self.result = {
                    "target": self.target,
                    "status": "failed",
                    "reason": "missing_critical_dependencies",
                }

                await self.save_execution_metadata(status="failed")
                await self.generate_phase_reports()
                return self.result

            self.result = await self.run_workflow()
            self.result["status"] = "completed"

            await self.generate_phase_reports()
            await self.generate_summary()
            await self.save_execution_metadata(status="completed")
            await self.cleanup()

            self.logger.success("Recon scan completed successfully")

            return self.result

        except KeyboardInterrupt:
            self.logger.warning("Scan interrupted by user")

            self.result = {
                "target": self.target,
                "status": "interrupted",
            }

            await self.save_execution_metadata(status="interrupted")
            await self.generate_phase_reports()

            return self.result

        except Exception as e:
            self.logger.error(f"Recon scan failed: {e}")

            self.result = {
                "target": self.target,
                "status": "failed",
                "error": str(e),
            }

            await self.save_execution_metadata(status="failed")
            await self.generate_phase_reports()

            return self.result


async def start_async_scan(
    target: str,
    mode: str = "normal",
    verify_tools: bool = True,
) -> Dict[str, Any]:

    engine = ReconEngineAsync(
        target=target,
        mode=mode,
        verify_tools=verify_tools,
    )

    return await engine.run()


def run_scan(
    target: str,
    mode: str = "normal",
    verify_tools: bool = True,
) -> Dict[str, Any]:

    return asyncio.run(
        start_async_scan(
            target=target,
            mode=mode,
            verify_tools=verify_tools,
        )
    )