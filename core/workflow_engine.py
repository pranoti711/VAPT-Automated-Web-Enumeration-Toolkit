
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from core.logger import Logger
from core.executor import executor
from core.parser import Parser
from core.validator import Validator
from core.output_manager import OutputManager


SUBDOMAIN_TOOLS = [
    "subfinder",
    "assetfinder",
    "amass",
    "findomain",
    "github-subdomains",
    "subscraper",
]

URL_TOOLS = [
    "gau",
    "waybackurls",
    "katana",
]

PARAMETER_TOOLS = [
    "paramspider",
    "arjun",
]

DIRECTORY_TOOLS = [
    "ffuf",
    "dirsearch",
]

GF_PATTERNS = [
    "xss",
    "sqli",
    "ssrf",
    "lfi",
    "redirect",
    "idor",
    "rce",
    "debug_logic",
]


class WorkflowEngine:

    def __init__(
        self,
        target: str,
        output: OutputManager,
    ):
        self.target = target.strip().lower()
        self.output = output
        self.logger = Logger()
        self.parser = Parser()
        self.validator = Validator()

        self.scan_root = Path(
            self.output.get_scan_root()
        )

        self.temp_dir = self.scan_root / "temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _merge_stdout(
        self,
        results: Dict[str, Dict[str, Any]],
    ) -> List[str]:

        merged: List[str] = []

        for result in results.values():
            stdout = result.get("stdout", "")

            if stdout:
                merged.extend(stdout.splitlines())

        return merged

    def _save_lines(
        self,
        relative_path: str,
        data: List[str],
    ) -> str:

        self.output.save_text(
            relative_path,
            data,
        )

        path = self.output.get_path(relative_path)

        self.logger.success(
            f"Saved: {path}"
        )

        return path

    async def run_subdomain_phase(self) -> List[str]:
        self.logger.phase(
            "SUBDOMAIN ENUMERATION: subfinder, assetfinder, amass, findomain, github-subdomains, subscraper"
        )

        results = await executor.run_many(
            tool_names=SUBDOMAIN_TOOLS,
            target=self.target,
            output_dir=self.scan_root / "subdomains" / "raw",
        )

        raw_lines = self._merge_stdout(results)

        self._save_lines(
            "subdomains/cleaned/merged_subdomains_raw.txt",
            raw_lines,
        )

        parsed = self.parser.parse_subdomains(raw_lines)

        clean = self.validator.validate_subdomains(parsed)

        self.output.save_subdomains(clean)

        self.output.save_subdomain_report(
            {
                "target": self.target,
                "tools": SUBDOMAIN_TOOLS,
                "raw_count": len(raw_lines),
                "final_count": len(clean),
                "output_file": self.output.get_subdomains_file(),
            }
        )

        return clean

    async def run_httpx_phase(
        self,
        subdomains: List[str],
    ) -> List[str]:

        self.logger.phase("HTTPX ALIVE DISCOVERY: httpx")

        if not subdomains:
            self.logger.warning(
                "No subdomains found. Skipping HTTPX phase."
            )

            self.output.save_alive_hosts([])

            self.output.save_httpx_report(
                {
                    "target": self.target,
                    "input_count": 0,
                    "alive_count": 0,
                    "status": "skipped",
                    "reason": "no_subdomains",
                    "output_file": self.output.get_alive_hosts_file(),
                }
            )

            return []

        input_file = self._save_lines(
            "temp/httpx_input.txt",
            subdomains,
        )

        result = await executor.run_tool(
            tool_name="httpx",
            input_file=input_file,
            output_file=self.output.get_path(
                "httpx/raw/httpx.txt"
            ),
        )

        raw_lines = result.get("stdout", "").splitlines()

        self._save_lines(
            "httpx/cleaned/httpx_raw_lines.txt",
            raw_lines,
        )

        parsed = self.parser.parse_httpx(raw_lines)

        clean = self.validator.validate_urls(parsed)

        self.output.save_alive_hosts(clean)

        self.output.save_httpx_report(
            {
                "target": self.target,
                "input_count": len(subdomains),
                "raw_count": len(raw_lines),
                "alive_count": len(clean),
                "success": result.get("success", False),
                "returncode": result.get("returncode"),
                "stderr": result.get("stderr", ""),
                "output_file": self.output.get_alive_hosts_file(),
            }
        )

        return clean

    async def run_url_phase(
        self,
        alive_hosts: List[str],
    ) -> List[str]:

        self.logger.phase(
            "URL DISCOVERY: gau, waybackurls, katana"
        )

        if not alive_hosts:
            self.logger.warning(
                "No alive hosts found. Skipping URL phase."
            )

            self.output.save_urls([])

            self.output.save_url_report(
                {
                    "target": self.target,
                    "input_count": 0,
                    "url_count": 0,
                    "status": "skipped",
                    "reason": "no_alive_hosts",
                    "output_file": self.output.get_urls_file(),
                }
            )

            return []

        all_raw_lines: List[str] = []

        for host in alive_hosts:
            results = await executor.run_many(
                tool_names=URL_TOOLS,
                target=host,
                output_dir=self.scan_root / "urls" / "raw",
            )

            all_raw_lines.extend(
                self._merge_stdout(results)
            )

        self._save_lines(
            "urls/cleaned/merged_urls_raw.txt",
            all_raw_lines,
        )

        parsed = self.parser.parse_archive_urls(
            all_raw_lines
        )

        parsed = self.parser.filter_static_urls(parsed)

        clean = self.validator.validate_urls(parsed)

        clean = self.validator.filter_scope(
            clean,
            self.target,
        )

        self.output.save_urls(clean)

        self.output.save_url_report(
            {
                "target": self.target,
                "input_alive_hosts": len(alive_hosts),
                "raw_count": len(all_raw_lines),
                "url_count": len(clean),
                "tools": URL_TOOLS,
                "output_file": self.output.get_urls_file(),
            }
        )

        return clean

    async def run_parameter_phase(
        self,
        urls: List[str],
    ) -> List[str]:

        self.logger.phase(
            "PARAMETER DISCOVERY: paramspider, arjun"
        )

        if not urls:
            self.logger.warning(
                "No URLs discovered. Skipping parameter phase."
            )

            self.output.save_parameters([])

            self.output.save_parameter_report(
                {
                    "target": self.target,
                    "input_urls": 0,
                    "parameter_count": 0,
                    "status": "skipped",
                    "reason": "no_urls",
                    "output_file": self.output.get_parameters_file(),
                }
            )

            return []

        results: Dict[str, Dict[str, Any]] = {}

        results["paramspider"] = await executor.run_tool(
            tool_name="paramspider",
            target=self.target,
            output_file=self.output.get_path(
                "parameters/raw/paramspider.txt"
            ),
        )

        for index, url in enumerate(urls[:20]):
            results[f"arjun_{index}"] = await executor.run_tool(
                tool_name="arjun",
                target=url,
                output_file=self.output.get_path(
                    f"parameters/raw/arjun_{index}.txt"
                ),
            )

        raw_lines = self._merge_stdout(results)
        raw_lines.extend(urls)

        self._save_lines(
            "parameters/cleaned/merged_parameters_raw.txt",
            raw_lines,
        )

        parsed = self.parser.parse_parameters(raw_lines)

        clean = self.validator.validate_parameters(parsed)

        self.output.save_parameters(clean)

        self.output.save_parameter_report(
            {
                "target": self.target,
                "input_urls": len(urls),
                "raw_count": len(raw_lines),
                "parameter_count": len(clean),
                "tools": PARAMETER_TOOLS,
                "output_file": self.output.get_parameters_file(),
            }
        )

        return clean

    async def run_gf_phase(
        self,
        urls: List[str],
    ) -> Dict[str, List[str]]:

        self.logger.phase("GF PATTERN ANALYSIS: gf")

        if not urls:
            self.logger.warning(
                "No URLs discovered. Skipping GF phase."
            )

            self.output.save_gf_report(
                {
                    "target": self.target,
                    "status": "skipped",
                    "reason": "no_urls",
                    "patterns": GF_PATTERNS,
                    "total_findings": 0,
                }
            )

            return {}

        url_file = self._save_lines(
            "temp/gf_input.txt",
            urls,
        )

        findings: Dict[str, List[str]] = {}

        for pattern in GF_PATTERNS:
            output_path = f"gf_patterns/{pattern}.txt"

            result = await executor.run_tool(
                tool_name="gf",
                input_file=url_file,
                output_file=self.output.get_path(output_path),
                pattern=pattern,
            )

            raw_lines = result.get("stdout", "").splitlines()

            parsed = self.parser.parse_gf_output(raw_lines)

            clean = self.validator.validate_urls(parsed)

            findings[pattern] = clean

            self._save_lines(
                output_path,
                clean,
            )

        self.output.save_gf_report(
            {
                "target": self.target,
                "patterns": GF_PATTERNS,
                "counts": {
                    key: len(value)
                    for key, value in findings.items()
                },
                "total_findings": sum(
                    len(value)
                    for value in findings.values()
                ),
                "output_folder": self.output.get_path("gf_patterns"),
            }
        )

        return findings

    async def run_directory_phase(
        self,
        alive_hosts: List[str],
        wordlist: str = "wordlists/directories",
    ) -> List[str]:

        self.logger.phase(
            "DIRECTORY ENUMERATION: ffuf, dirsearch"
        )

        if not alive_hosts:
            self.logger.warning(
                "No alive hosts found. Skipping directory phase."
            )

            self.output.save_directories([])

            self.output.save_directory_report(
                {
                    "target": self.target,
                    "input_alive_hosts": 0,
                    "directory_count": 0,
                    "status": "skipped",
                    "reason": "no_alive_hosts",
                    "output_file": self.output.get_directories_file(),
                }
            )

            return []

        all_results: List[str] = []

        for host in alive_hosts[:20]:
            results = await executor.run_many(
                tool_names=DIRECTORY_TOOLS,
                target=host,
                output_dir=self.scan_root / "directories" / "raw",
                wordlist=wordlist,
            )

            raw_lines = self._merge_stdout(results)

            all_results.extend(
                self.parser.parse_ffuf(raw_lines, host)
            )

            all_results.extend(
                self.parser.parse_dirsearch(raw_lines, host)
            )

        self._save_lines(
            "directories/cleaned/merged_directories_raw.txt",
            all_results,
        )

        clean = self.validator.clean_directory_results(
            all_results
        )

        self.output.save_directories(clean)

        self.output.save_directory_report(
            {
                "target": self.target,
                "input_alive_hosts": len(alive_hosts),
                "tested_hosts": min(len(alive_hosts), 20),
                "directory_count": len(clean),
                "tools": DIRECTORY_TOOLS,
                "output_file": self.output.get_directories_file(),
            }
        )

        return clean

    async def run_full_workflow(self) -> Dict[str, Any]:
        self.logger.phase("FULL RECON WORKFLOW")

        subdomains = await self.run_subdomain_phase()

        alive_hosts = await self.run_httpx_phase(
            subdomains
        )

        urls = await self.run_url_phase(
            alive_hosts
        )

        parameters = await self.run_parameter_phase(
            urls
        )

        gf_findings = await self.run_gf_phase(
            urls
        )

        directories = await self.run_directory_phase(
            alive_hosts
        )

        final_result = {
            "target": self.target,
            "tools_used": {
                "subdomain_tools": SUBDOMAIN_TOOLS,
                "http_probe_tools": ["httpx"],
                "url_tools": URL_TOOLS,
                "parameter_tools": PARAMETER_TOOLS,
                "gf_tools": ["gf"],
                "directory_tools": DIRECTORY_TOOLS,
            },
            "subdomains": subdomains,
            "alive_hosts": alive_hosts,
            "urls": urls,
            "parameters": parameters,
            "gf_findings": gf_findings,
            "directories": directories,
        }

        self.output.save_json(
            "reports/report.json",
            final_result,
        )

        self.output.save_final_report(
            {
                "target": self.target,
                "subdomains": len(subdomains),
                "alive_hosts": len(alive_hosts),
                "urls": len(urls),
                "parameters": len(parameters),
                "gf_findings": {
                    key: len(value)
                    for key, value in gf_findings.items()
                },
                "gf_total": sum(
                    len(value)
                    for value in gf_findings.values()
                ),
                "directories": len(directories),
                "tools_used": final_result["tools_used"],
            }
        )

        self.output.save_json(
            "metadata/final_counts.json",
            {
                "subdomains": len(subdomains),
                "alive_hosts": len(alive_hosts),
                "urls": len(urls),
                "parameters": len(parameters),
                "gf_patterns": sum(
                    len(value)
                    for value in gf_findings.values()
                ),
                "directories": len(directories),
            },
        )

        self.output.save_json(
            "metadata/tools_used.json",
            final_result["tools_used"],
        )

        self.logger.success(
            "Full recon workflow completed"
        )

        return final_result