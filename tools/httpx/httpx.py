"""httpx wrapper for alive checks."""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_httpx_alive(subdomains_file: str | Path, output_file: str | Path) -> Path:
    subdomains_path = Path(subdomains_file)
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    info("Running HTTPX alive check")
    # -l input list, -silent suppresses banner/logging
    execute_tool(
        command=f"httpx -l {subdomains_path} -silent",
        output_file=str(out_path),
    )

    return out_path

