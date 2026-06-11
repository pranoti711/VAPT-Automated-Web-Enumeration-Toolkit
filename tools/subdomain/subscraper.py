"""Subscraper wrapper.

This repo's `subdomain_pipeline.py` expects to be able to run `subscraper`
and persist results into a file.

Output file convention used by the pipeline:
- <output_dir>/subscraper.txt
"""

from __future__ import annotations

from pathlib import Path

from core.tool_executor import execute_tool
from core.live_monitor import info


def _ensure_subscraper_deps() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    subscraper_requirements = repo_root / "tools" / "external" / "subscraper" / "requirements.txt"

    if not subscraper_requirements.exists():
        # Fail silently here; the actual subscraper invocation will surface the root error.
        return

    # Install/upgrade deps into the active Python environment.
    # Use --disable-pip-version-check to reduce noise.
    execute_tool(
        command=(
            f"python -m pip install --disable-pip-version-check --upgrade "
            f"-r "
            f"\"{str(subscraper_requirements)}\""
        ),
        output_file=None,
    )


def run_subscraper(target: str, output_dir: str | Path) -> Path:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_file = output_dir_path / "subscraper.txt"

    _ensure_subscraper_deps()

    # Verify imports and CLI entrypoint availability to avoid runtime surprises
    # (e.g., `taser` not installed in the active Python environment).
    execute_tool(
        command="python -c \"import subscraper; import taser; print('subscraper/taser-import-ok')\"",
        output_file=None,
    )

    info(f"Running Subscraper for {target}")

    execute_tool(
        command=f"subscraper -d {target}",
        output_file=str(output_file),
    )

    return output_file

