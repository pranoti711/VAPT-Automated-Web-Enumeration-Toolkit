"""Arjun wrapper.

Arjun is used for parameter discovery.
If the tool is not installed, this will fail gracefully via execute_tool.

Output convention:
- <output_dir>/arjun.txt
"""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_arjun(target: str, output_dir: str | Path) -> Path:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_file = output_dir_path / "arjun.txt"

    info(f"Running Arjun for {target}")

    # Arjun expects URL. If user passes domain, prepend https.
    url = target if target.startswith("http") else f"https://{target}"

    execute_tool(
        command=f"arjun -u {url}",
        output_file=str(output_file),
    )

    return output_file

