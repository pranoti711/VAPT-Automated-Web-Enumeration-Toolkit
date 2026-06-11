"""Amass wrapper.

Writes output to `<output_dir>/amass.txt`.
"""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_amass(target: str, output_dir: str | Path) -> Path:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_file = output_dir_path / "amass.txt"

    info(f"Running Amass for {target}")
    execute_tool(
        command=f"amass enum -passive -d {target}",
        output_file=str(output_file),
    )

    return output_file

