# Auto-generated file
# =========================================
# FILE: tools/directory/ffuf.py
# =========================================

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_ffuf(
    target: str,
    output_dir: str | Path,
) -> Path:

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / "ffuf.txt"

    info(f"Running FFUF for {target}")

    url = (
        target
        if target.startswith("http")
        else f"https://{target}"
    )

    execute_tool(
        command=(
            f'ffuf '
            f'-u {url}/FUZZ '
            f'-w wordlists/common.txt '
            f'-mc 200,204,301,302,307,401,403 '
            f'-s'
        ),
        output_file=str(output_file),
    )

    return output_file