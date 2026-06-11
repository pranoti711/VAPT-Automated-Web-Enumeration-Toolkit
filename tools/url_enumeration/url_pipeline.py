# =========================================
# FILE: tools/url/url_pipeline.py
# FINAL URL + PARAMETER + GF PIPELINE
# =========================================

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[2]

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.executor import executor
from core.parser import Parser
from core.validator import Validator
from core.merger import merger
from core.live_monitor import info, success, warning


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


def write_lines(file_path: str | Path, data: List[str]) -> Path:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        "\n".join(data),
        encoding="utf-8",
        errors="ignore",
    )

    return path


def create_url_directories(output_dir: str | Path) -> Dict[str, Path]:
    base = Path(output_dir)

    paths = {
        "raw": base / "urls" / "raw",
        "cleaned": base / "urls" / "cleaned",
        "final": base / "urls" / "final",
        "parameters_raw": base / "parameters" / "raw",
        "parameters_final": base / "parameters" / "final",
        "gf": base / "gf",
    }

    for directory in paths.values():
        directory.mkdir(parents=True, exist_ok=True)

    return paths


async def run_url_tool(
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


async def run_parameter_tool(
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


async def run_gf_pattern(
    pattern: str,
    input_file: Path,
    output_file: Path,
) -> List[str]:

    info(f"Running GF pattern: {pattern}")

    result = await executor.run_tool(
        tool_name="gf",
        input_file=str(input_file),
        output_file=str(output_file),
        pattern=pattern,
    )

    if not result.get("success"):
        warning(f"GF pattern failed: {pattern}")

    return read_lines(output_file)


async def run_url_pipeline(
    alive_hosts_file: str | Path,
    output_dir: str | Path,
) -> Dict[str, List[str] | Dict[str, List[str]]]:

    info("Starting URL Discovery Pipeline")

    parser = Parser()
    validator = Validator()

    paths = create_url_directories(output_dir)

    raw_dir = paths["raw"]
    cleaned_dir = paths["cleaned"]
    final_dir = paths["final"]
    parameters_raw_dir = paths["parameters_raw"]
    parameters_final_dir = paths["parameters_final"]
    gf_dir = paths["gf"]

    alive_hosts = read_lines(alive_hosts_file)

    if not alive_hosts:
        warning("No alive hosts found for URL discovery")
        return {
            "urls": [],
            "parameters": [],
            "gf_findings": {},
        }

    url_tools = [
        "gau",
        "waybackurls",
        "katana",
    ]

    parameter_tools = [
        "paramspider",
        "arjun",
    ]

    gf_patterns = [
        "xss",
        "sqli",
        "ssrf",
        "lfi",
        "redirect",
        "rce",
        "idor",
    ]

    raw_url_results: Dict[str, List[str]] = {}
    raw_parameter_results: Dict[str, List[str]] = {}

    # =====================================
    # URL DISCOVERY: GAU / WAYBACK / KATANA
    # =====================================

    for host in alive_hosts:

        clean_host = (
            host.replace("https://", "")
            .replace("http://", "")
            .strip("/")
        )

        for tool_name in url_tools:

            output_file = (
                raw_dir
                / f"{tool_name}_{clean_host.replace('/', '_')}.txt"
            )

            result_lines = await run_url_tool(
                tool_name=tool_name,
                target=host,
                output_file=output_file,
            )

            raw_url_results.setdefault(tool_name, [])
            raw_url_results[tool_name].extend(result_lines)

    # =====================================
    # MERGE URLS
    # =====================================

    merged_raw_urls = merger.merge_tool_outputs(raw_url_results)

    merged_raw_file = cleaned_dir / "merged_raw_urls.txt"

    write_lines(
        merged_raw_file,
        merged_raw_urls,
    )

    # =====================================
    # PARSE URLS
    # =====================================

    parsed_urls = parser.parse_urls(
        merged_raw_urls
    )

    parsed_urls_file = cleaned_dir / "parsed_urls.txt"

    write_lines(
        parsed_urls_file,
        parsed_urls,
    )

    # =====================================
    # VALIDATE URLS
    # =====================================

    valid_urls = validator.validate_urls(
        parsed_urls
    )

    final_urls_file = final_dir / "urls.txt"

    write_lines(
        final_urls_file,
        valid_urls,
    )

    # =====================================
    # PARAMETER DISCOVERY: PARAMSPIDER / ARJUN
    # =====================================

    info("Starting Parameter Discovery")

    for host in alive_hosts:

        clean_host = (
            host.replace("https://", "")
            .replace("http://", "")
            .strip("/")
        )

        for tool_name in parameter_tools:

            output_file = (
                parameters_raw_dir
                / f"{tool_name}_{clean_host.replace('/', '_')}.txt"
            )

            result_lines = await run_parameter_tool(
                tool_name=tool_name,
                target=host,
                output_file=output_file,
            )

            raw_parameter_results.setdefault(tool_name, [])
            raw_parameter_results[tool_name].extend(result_lines)

    merged_parameter_raw = merger.merge_tool_outputs(
        raw_parameter_results
    )

    param_urls_from_tools = parser.parse_urls(
        merged_parameter_raw
    )

    all_urls_for_params = merger.merge_urls(
        valid_urls,
        param_urls_from_tools,
    )

    parameters = parser.parse_parameters(
        all_urls_for_params
    )

    valid_parameters = validator.validate_parameters(
        parameters
    )

    final_parameters_file = parameters_final_dir / "parameters.txt"

    write_lines(
        final_parameters_file,
        valid_parameters,
    )

    # =====================================
    # GF PATTERN MATCHING
    # =====================================

    info("Starting GF Pattern Matching")

    gf_findings: Dict[str, List[str]] = {}

    for pattern in gf_patterns:

        pattern_dir = gf_dir / pattern
        pattern_dir.mkdir(parents=True, exist_ok=True)

        output_file = pattern_dir / f"{pattern}.txt"

        findings = await run_gf_pattern(
            pattern=pattern,
            input_file=final_urls_file,
            output_file=output_file,
        )

        gf_findings[pattern] = findings

    # =====================================
    # FINAL STATUS
    # =====================================

    success("URL Discovery Pipeline Completed")

    print("\nGenerated Files:\n")

    print("[URLS]")
    print(str(final_urls_file))

    print("\n[PARAMETERS]")
    print(str(final_parameters_file))

    print("\n[GF FINDINGS]")
    print(str(gf_dir))

    return {
        "urls": valid_urls,
        "parameters": valid_parameters,
        "gf_findings": gf_findings,
    }


def run_url_pipeline_sync(
    alive_hosts_file: str | Path,
    output_dir: str | Path,
) -> Dict[str, List[str] | Dict[str, List[str]]]:

    return asyncio.run(
        run_url_pipeline(
            alive_hosts_file=alive_hosts_file,
            output_dir=output_dir,
        )
    )


if __name__ == "__main__":

    import argparse

    cli = argparse.ArgumentParser(
        description="Run URL discovery, parameter discovery, and GF pipeline"
    )

    cli.add_argument(
        "-i",
        "--input",
        required=True,
        help="Alive hosts file",
    )

    cli.add_argument(
        "-o",
        "--output",
        default="outputs/test_scan",
        help="Output directory",
    )

    args = cli.parse_args()

    run_url_pipeline_sync(
        alive_hosts_file=args.input,
        output_dir=args.output,
    )