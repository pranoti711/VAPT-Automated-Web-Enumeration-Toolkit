# =========================================
# FILE: tools/url/katana.py
# =========================================

"""
Katana wrapper.

Katana is used for:
- crawling
- endpoint discovery
- JavaScript crawling
- URL extraction

Output convention:
- <output_dir>/katana.txt
"""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


# =========================================
# RUN KATANA
# =========================================

def run_katana(
    target: str,
    output_dir: str | Path,
) -> Path:

    output_dir_path = Path(output_dir)

    output_dir_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir_path / "katana.txt"

    info(f"Running Katana for {target}")

    # =====================================
    # TARGET URL
    # =====================================

    url = (
        target
        if target.startswith("http")
        else f"https://{target}"
    )

    # =====================================
    # EXECUTE
    # =====================================

    execute_tool(
        command=(
            f"katana "
            f"-u {url} "
            f"-silent "
            f"-jc "
            f"-d 3"
        ),
        output_file=str(output_file),
    )

    return output_file