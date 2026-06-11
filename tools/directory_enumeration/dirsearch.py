# Auto-generated file
# =========================================
# FILE: tools/directory/dirsearch.py
# =========================================

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_dirsearch(
    target: str,
    output_dir: str | Path,
) -> Path:

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / "dirsearch.txt"

    info(f"Running Dirsearch for {target}")

    url = (
        target
        if target.startswith("http")
        else f"https://{target}"
    )

    execute_tool(
        command=(
            f"dirsearch "
            f"-u {url} "
            f"--quiet"
        ),
        output_file=str(output_file),
    )

    return output_file