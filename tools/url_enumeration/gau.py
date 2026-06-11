from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_gau(target: str, output_dir: str | Path) -> Path:

    output_dir_path = Path(output_dir)

    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_file = output_dir_path / "gau.txt"

    info(f"Running GAU For {target}")

    execute_tool(
        command=f"gau {target}",
        output_file=str(output_file),
    )

    return output_file