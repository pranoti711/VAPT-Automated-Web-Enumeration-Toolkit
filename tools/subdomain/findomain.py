"""Findomain wrapper."""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_findomain(target: str, output_dir: str | Path) -> Path:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_file = output_dir_path / "findomain.txt"

    info(f"Running Findomain for {target}")
    # -q quiet, -t target
    execute_tool(
        command=f"findomain -t {target} -q",
        output_file=str(output_file),
    )

    return output_file

