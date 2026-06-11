# =========================================
# FILE: tools/httpx/httpx_pipeline.py
# FINAL HTTPX PIPELINE
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
from core.live_monitor import (
    info,
    success,
    warning,
)

# =========================================
# HELPERS
# =========================================

def read_lines(
    file_path: str | Path,
) -> List[str]:

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


def write_lines(
    file_path: str | Path,
    data: List[str],
) -> Path:

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


# =========================================
# CREATE DIRECTORIES
# =========================================

def create_httpx_directories(
    output_dir: str | Path,
) -> Dict[str, Path]:

    base = Path(output_dir)

    paths = {
        "raw": base / "httpx" / "raw",
        "cleaned": base / "httpx" / "cleaned",
        "final": base / "httpx" / "final",
    }

    for directory in paths.values():
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    return paths


# =========================================
# HTTPX EXECUTION
# =========================================

async def run_httpx(
    input_file: Path,
    output_file: Path,
) -> Dict:

    info("Running HTTPX")

    result = await executor.run_tool(
        tool_name="httpx",
        input_file=str(input_file),
        output_file=str(output_file),
    )

    stdout = result.get(
        "stdout",
        "",
    )

    if stdout:
        output_file.write_text(
            stdout,
            encoding="utf-8",
            errors="ignore",
        )

    return result


# =========================================
# PIPELINE
# =========================================

async def run_httpx_pipeline(
    subdomains_file: str | Path,
    output_dir: str | Path,
) -> Dict[str, List[str]]:

    info("Starting HTTPX Pipeline")

    parser = Parser()
    validator = Validator()

    paths = create_httpx_directories(
        output_dir,
    )

    raw_dir = paths["raw"]
    cleaned_dir = paths["cleaned"]
    final_dir = paths["final"]

    subdomains_file = Path(
        subdomains_file,
    )

    if not subdomains_file.exists():

        warning(
            f"Input file not found: "
            f"{subdomains_file}"
        )

        return {
            "alive_hosts": [],
        }

    # =====================================
    # RAW OUTPUT
    # =====================================

    raw_output = raw_dir / "httpx_raw.txt"

    result = await run_httpx(
        input_file=subdomains_file,
        output_file=raw_output,
    )

    if not result.get("success"):

        warning(
            "HTTPX execution failed"
        )

    # =====================================
    # READ RAW DATA
    # =====================================

    raw_lines = read_lines(
        raw_output,
    )

    # =====================================
    # PARSE URLS
    # =====================================

    parsed_urls = []

    for line in raw_lines:

        parsed = parser.parse_urls(
            line,
        )

        if isinstance(
            parsed,
            list,
        ):
            parsed_urls.extend(parsed)

    parsed_file = (
        cleaned_dir
        / "parsed_urls.txt"
    )

    write_lines(
        parsed_file,
        parsed_urls,
    )

    # =====================================
    # VALIDATE URLS
    # =====================================

    valid_urls = validator.validate_urls(
        parsed_urls,
    )

    valid_urls = sorted(
        set(valid_urls)
    )

    final_file = (
        final_dir
        / "alive_hosts.txt"
    )

    write_lines(
        final_file,
        valid_urls,
    )

    # =====================================
    # FINAL STATUS
    # =====================================

    success(
        f"Alive Hosts Found: "
        f"{len(valid_urls)}"
    )

    print("\nGenerated Files:\n")

    print(
        "[RAW HTTPX]"
    )
    print(raw_output)

    print(
        "\n[PARSED URLS]"
    )
    print(parsed_file)

    print(
        "\n[ALIVE HOSTS]"
    )
    print(final_file)

    return {
        "alive_hosts": valid_urls,
    }


# =========================================
# SYNC WRAPPER
# =========================================

def run_httpx_pipeline_sync(
    subdomains_file: str | Path,
    output_dir: str | Path,
):

    return asyncio.run(
        run_httpx_pipeline(
            subdomains_file=subdomains_file,
            output_dir=output_dir,
        )
    )


# =========================================
# DIRECT TEST
# =========================================

if __name__ == "__main__":

    import argparse

    cli = argparse.ArgumentParser()

    cli.add_argument(
        "-i",
        "--input",
        required=True,
        help="Subdomains file",
    )

    cli.add_argument(
        "-o",
        "--output",
        default="outputs/test_scan",
    )

    args = cli.parse_args()

    run_httpx_pipeline_sync(
        subdomains_file=args.input,
        output_dir=args.output,
    )