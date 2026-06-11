# =========================================
# FILE: tools/directory/directory_pipeline.py
# FINAL DIRECTORY ENUMERATION PIPELINE
# =========================================

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Dict, List

# =========================================
# PROJECT ROOT
# =========================================

_REPO_ROOT = Path(__file__).resolve().parents[2]

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# =========================================
# IMPORTS
# =========================================

from core.executor import executor
from core.parser import Parser
from core.validator import Validator
from core.merger import merger
from core.live_monitor import (
    info,
    success,
    warning,
)


# =========================================
# HELPERS
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


def write_lines(file_path: str | Path, data: List[str]) -> Path:
    path = Path(file_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        "\n".join(data),
        encoding="utf-8",
        errors="ignore",
    )

    return path


def safe_filename(value: str) -> str:
    return (
        value.replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace(":", "_")
        .strip("_")
    )


# =========================================
# CREATE DIRECTORIES
# =========================================

def create_directory_enum_directories(output_dir: str | Path) -> Dict[str, Path]:
    base = Path(output_dir)

    paths = {
        "raw": base / "directories" / "raw",
        "cleaned": base / "directories" / "cleaned",
        "final": base / "directories" / "final",
    }

    for directory in paths.values():
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    return paths


# =========================================
# RUN DIRECTORY TOOL
# =========================================

async def run_directory_tool(
    tool_name: str,
    target: str,
    output_file: Path,
    wordlist: str | None = None,
) -> List[str]:
    info(f"Running {tool_name} on {target}")

    result = await executor.run_tool(
        tool_name=tool_name,
        target=target,
        output_file=str(output_file),
        wordlist=wordlist,
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
# PARSE TOOL OUTPUT
# =========================================

def parse_directory_output(
    parser: Parser,
    tool_name: str,
    lines: List[str],
    target: str,
) -> List[str]:
    if tool_name == "ffuf":
        return parser.parse_ffuf(
            lines=lines,
            base_url=target,
        )

    if tool_name == "dirsearch":
        return parser.parse_dirsearch(
            lines=lines,
            base_url=target,
        )

    if tool_name == "feroxbuster":
        return parser.parse_feroxbuster(
            lines=lines,
        )

    return parser.parse_urls(lines)


# =========================================
# PIPELINE
# =========================================

async def run_directory_pipeline(
    alive_hosts_file: str | Path,
    output_dir: str | Path,
    wordlist: str | None = None,
) -> Dict[str, List[str]]:
    info("Starting Directory Enumeration Pipeline")

    parser = Parser()
    validator = Validator()

    paths = create_directory_enum_directories(output_dir)

    raw_dir = paths["raw"]
    cleaned_dir = paths["cleaned"]
    final_dir = paths["final"]

    alive_hosts = read_lines(alive_hosts_file)
    if not alive_hosts:
        warning("No alive hosts found for directory enumeration")
        return {"directories": []}

    requested_tools = [
        "ffuf",
        "dirsearch",
        "feroxbuster",
    ]

    # Skip tools that are not installed to avoid ending directory enumeration with empty outputs.
    directory_tools: List[str] = []
    for t in requested_tools:
        if executor.is_tool_installed(t):
            directory_tools.append(t)
        else:
            warning(f"Skipping {t}: tool not installed (missing binary in PATH)")

    raw_results: Dict[str, List[str]] = {}
    parsed_results: Dict[str, List[str]] = {}

    # No tools available => produce empty but successful output files.
    if not directory_tools:
        warning("No directory enumeration tools installed; skipping directory scan.")

    for host in alive_hosts:
        host_name = safe_filename(host)

        for tool_name in directory_tools:
            output_file = raw_dir / f"{tool_name}_{host_name}.txt"

            raw_lines = await run_directory_tool(
                tool_name=tool_name,
                target=host,
                output_file=output_file,
                wordlist=wordlist,
            )

            raw_key = f"{tool_name}_{host_name}"
            raw_results[raw_key] = raw_lines

            parsed = parse_directory_output(
                parser=parser,
                tool_name=tool_name,
                lines=raw_lines,
                target=host,
            )
            parsed_results[raw_key] = parsed

            parsed_file = cleaned_dir / f"{tool_name}_{host_name}_parsed.txt"
            write_lines(parsed_file, parsed)

    # =====================================
    # MERGE PARSED RESULTS
    # =====================================

    info("Merging directory enumeration results")

    merged_directories = merger.merge_tool_outputs(parsed_results)

    merged_file = cleaned_dir / "merged_directories.txt"
    write_lines(merged_file, merged_directories)

    # =====================================
    # VALIDATE URLS / DIRECTORIES
    # =====================================

    valid_directories = validator.validate_urls(merged_directories)
    valid_directories = sorted(set(valid_directories))

    final_file = final_dir / "directories.txt"
    write_lines(final_file, valid_directories)

    # =====================================
    # FINAL STATUS
    # =====================================

    success(
        f"Directory Enumeration Completed: "
        f"{len(valid_directories)} results"
    )

    print("\nGenerated Files:\n")
    print("[RAW]")
    print(str(raw_dir))

    print("\n[MERGED]")
    print(str(merged_file))

    print("\n[FINAL DIRECTORIES]")
    print(str(final_file))

    return {"directories": valid_directories}


# =========================================
# SYNC WRAPPER
# =========================================

def run_directory_pipeline_sync(
    alive_hosts_file: str | Path,
    output_dir: str | Path,
    wordlist: str | None = None,
) -> Dict[str, List[str]]:
    return asyncio.run(
        run_directory_pipeline(
            alive_hosts_file=alive_hosts_file,
            output_dir=output_dir,
            wordlist=wordlist,
        )
    )


# =========================================
# DIRECT TEST
# =========================================

if __name__ == "__main__":
    import argparse

    cli = argparse.ArgumentParser(
        description="Run directory enumeration pipeline"
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

    cli.add_argument(
        "-w",
        "--wordlist",
        default=None,
        help="Optional wordlist path",
    )

    args = cli.parse_args()

    run_directory_pipeline_sync(
        alive_hosts_file=args.input,
        output_dir=args.output,
        wordlist=args.wordlist,
    )

