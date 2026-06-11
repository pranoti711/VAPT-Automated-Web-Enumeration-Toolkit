"""github-subdomains wrapper."""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def run_github_subdomains(target: str, output_dir: str | Path) -> Path:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_file = output_dir_path / "github_subdomains.txt"

    info(f"Running github-subdomains for {target}")
    execute_tool(
        command=f"github-subdomains -d {target}",
        output_file=str(output_file),
    )

    return output_file

