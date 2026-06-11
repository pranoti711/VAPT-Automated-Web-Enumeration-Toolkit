# =========================================
# FILE: tools/subdomain/subdomain_pipeline.py
# FINAL SUBDOMAIN ENUMERATION PIPELINE
# =========================================

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

# Ensure repository root is on sys.path when running directly
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.executor import executor
from core.live_monitor import info, success, warning
from core.merger import merger
from core.parser import Parser
from core.validator import Validator


# =========================================
# CREATE DIRECTORIES
# =========================================

def create_subdomain_directories(base_output: str | Path) -> Dict[str, Path]:
    base = Path(base_output)

    paths = {
        "raw": base / "subdomains" / "raw",
        "cleaned": base / "subdomains" / "cleaned",
        "final": base / "subdomains" / "final",
        "alive": base / "subdomains" / "alive",
    }

    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

    return paths


# =========================================
# WRITE LINES
# =========================================

def write_lines(file_path: str | Path, data: List[str]) -> Path:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        "\n".join(data),
        encoding="utf-8",
        errors="ignore",
    )

    return path


# =========================================
# READ LINES
# =========================================

def read_lines(file_path: str | Path) -> List[str]:
    path = Path(file_path)
    if not path.exists():
        return []

    return [
        line.strip()
        for line in path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()
        if line.strip()
    ]


# =========================================
# RUN SUBDOMAIN TOOL
# =========================================

async def run_subdomain_tool(
    tool_name: str,
    target: str,
    output_file: Path,
) -> List[str]:
    info(f"Running {tool_name}")

    result = await executor.run_tool(
        tool_name=tool_name,
        target=target,
        output_file=str(output_file),
    )

    stdout = result.get("stdout", "")
    if stdout:
        output_file.write_text(
            stdout,
            encoding="utf-8",
            errors="ignore",
        )

    if not result.get("success"):
        warning(f"{tool_name} failed or returned no verified success")

    return read_lines(output_file)


# =========================================
# RUN HTTPX ALIVE CHECK
# =========================================

async def run_httpx_alive_check(
    input_file: Path,
    output_file: Path,
) -> List[str]:
    info("Running httpx alive check")

    result = await executor.run_tool(
        tool_name="httpx",
        input_file=str(input_file),
        output_file=str(output_file),
    )

    stdout = result.get("stdout", "")
    if stdout:
        output_file.write_text(
            stdout,
            encoding="utf-8",
            errors="ignore",
        )

    if not result.get("success"):
        warning("httpx failed or returned no verified success")

    return read_lines(output_file)


# =========================================
# RUN SUBDOMAIN PIPELINE
# =========================================

async def run_subdomain_pipeline(
    target: str,
    output_dir: str | Path,
    run_httpx: bool = True,
) -> Dict[str, List[str]]:
    info("Starting Subdomain Enumeration Phase")

    parser = Parser()
    validator = Validator()

    paths = create_subdomain_directories(output_dir)

    raw_dir = paths["raw"]
    cleaned_dir = paths["cleaned"]
    final_dir = paths["final"]
    alive_dir = paths["alive"]

    requested_tools = [
        "subfinder",
        "assetfinder",
        "amass",
        "findomain",
        "github-subdomains",
        "subscraper",
    ]

    # Skip tools that are not installed to avoid ending the whole scan with empty results.
    tools: List[str] = []
    for t in requested_tools:
        if executor.is_tool_installed(t):
            tools.append(t)
        else:
            warning(f"Skipping {t}: tool not installed (missing binary in PATH)")

    raw_results: Dict[str, List[str]] = {}

    # =====================================
    # RUN ALL SUBDOMAIN TOOLS
    # =====================================
    for tool_name in tools:
        output_file = raw_dir / f"{tool_name}.txt"
        raw_results[tool_name] = await run_subdomain_tool(
            tool_name=tool_name,
            target=target,
            output_file=output_file,
        )

    # =====================================
    # MERGE RAW OUTPUTS
    # =====================================
    info("Merging subdomain results")
    merged_raw = merger.merge_tool_outputs(raw_results)

    merged_raw_file = cleaned_dir / "merged_raw.txt"
    write_lines(merged_raw_file, merged_raw)

    # =====================================
    # PARSE SUBDOMAINS
    # =====================================
    info("Parsing subdomains")
    parsed_subdomains = parser.parse_subdomains(merged_raw)

    parsed_file = cleaned_dir / "parsed_subdomains.txt"
    write_lines(parsed_file, parsed_subdomains)

    # =====================================
    # VALIDATE SUBDOMAINS
    # =====================================
    info("Validating subdomains")
    valid_subdomains = validator.validate_subdomains(parsed_subdomains)

    final_subdomains_file = final_dir / "subdomains.txt"
    write_lines(final_subdomains_file, valid_subdomains)

    alive_hosts: List[str] = []

    # =====================================
    # HTTPX ALIVE CHECK
    # =====================================
    if run_httpx and valid_subdomains:
        alive_file = alive_dir / "alive_subdomains.txt"
        alive_raw = await run_httpx_alive_check(
            input_file=final_subdomains_file,
            output_file=alive_file,
        )

        alive_hosts = validator.validate_urls(alive_raw)
        write_lines(alive_file, alive_hosts)

    # =====================================
    # FINAL STATUS
    # =====================================
    success("Subdomain Enumeration Completed")

    print("\nGenerated Files:\n")
    print("[RAW]")
    print(str(raw_dir))

    print("\n[MERGED]")
    print(str(merged_raw_file))

    print("\n[FINAL SUBDOMAINS]")
    print(str(final_subdomains_file))

    if run_httpx:
        print("\n[ALIVE SUBDOMAINS]")
        print(str(alive_dir / "alive_subdomains.txt"))

    return {
        "subdomains": valid_subdomains,
        "alive_hosts": alive_hosts,
    }


# =========================================
# SYNC WRAPPER
# =========================================

def run_subdomain_pipeline_sync(
    target: str,
    output_dir: str | Path,
    run_httpx: bool = True,
) -> Dict[str, List[str]]:
    import asyncio

    return asyncio.run(
        run_subdomain_pipeline(
            target=target,
            output_dir=output_dir,
            run_httpx=run_httpx,
        )
    )


# =========================================
# DIRECT TEST
# =========================================

if __name__ == "__main__":
    import argparse

    parser_cli = argparse.ArgumentParser(
        description="Run subdomain enumeration pipeline"
    )

    parser_cli.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain",
    )

    parser_cli.add_argument(
        "-o",
        "--output",
        default="outputs/test_scan",
        help="Output directory",
    )

    parser_cli.add_argument(
        "--no-httpx",
        action="store_true",
        help="Disable httpx alive probing",
    )

    args = parser_cli.parse_args()

    run_subdomain_pipeline_sync(
        target=args.domain,
        output_dir=args.output,
        run_httpx=not args.no_httpx,
    )

