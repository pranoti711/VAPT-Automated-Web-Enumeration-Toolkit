"""Subfinder wrapper.

This repository uses `core.tool_executor.execute_tool()` to run external tools
and persist outputs.

Pipeline usage:
- Expected by `tools/subdomain/subdomain_pipeline.py` (direct shell calls)
- Also available as a helper `run_subfinder()` for other pipeline stages.
"""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_subfinder(target: str, output_dir: str) -> Path:
    """Run subfinder and write results to `<output_dir>/subfinder.txt`."""

    output_dir_path = Path(output_dir)
    output_file = output_dir_path / "subfinder.txt"
    output_dir_path.mkdir(parents=True, exist_ok=True)

    info(f"Running Subfinder for {target}")
    execute_tool(
        command=f"subfinder -d {target} -silent",
        output_file=str(output_file),
    )

    return output_file

