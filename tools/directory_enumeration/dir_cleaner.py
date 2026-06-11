# Auto-generated file
# =========================================
# FILE: tools/directory/directory_cleaner.py
# =========================================

"""
Directory Cleaner

Purpose:
--------
- remove duplicates
- remove blank lines
- normalize paths
"""

from __future__ import annotations

from pathlib import Path

from core.live_monitor import (
    info,
    success,
)


# =========================================
# CLEAN DIRECTORY RESULTS
# =========================================

def clean_directories(
    input_file: str | Path,
    output_file: str | Path,
) -> Path:

    input_path = Path(input_file)

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    info(f"Cleaning Directory Results: {input_path}")

    cleaned: set[str] = set()

    if input_path.exists():

        with open(
            input_path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                # Remove trailing slash
                line = line.rstrip("/")

                if line:
                    cleaned.add(line)

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as out:

        for item in sorted(cleaned):

            out.write(item + "\n")

    success(f"Cleaned Directory Results Saved: {output_path}")

    return output_path