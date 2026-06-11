"""GF (Grep-Filter) wrapper.

GF is typically used to filter URLs for patterns.
This wrapper applies gf to provided input URLs.

Output convention:
- <output_dir>/gf.txt
"""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_gf(pattern: str, input_file: str | Path, output_dir: str | Path) -> Path:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    input_file_path = Path(input_file)
    output_file = output_dir_path / f"{pattern}.txt"

    info(f"Running GF pattern={pattern} on {input_file_path}")

    execute_tool(
        command=f"cat {input_file_path} | gf {pattern}",
        output_file=str(output_file),
    )

    return output_file

