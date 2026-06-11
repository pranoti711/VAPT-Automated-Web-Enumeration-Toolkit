# Auto-generated file
# =========================================
# FILE: tools/directory/directory_merger.py
# =========================================

"""
Directory Merger

Purpose:
--------
Merge outputs from:
- ffuf
- dirsearch
- feroxbuster

Removes duplicates automatically.
"""

from __future__ import annotations

from pathlib import Path

from core.live_monitor import (
    info,
    success,
)


# =========================================
# MERGE DIRECTORY FILES
# =========================================

def merge_directory_files(
    file_list: list[str | Path],
    output_file: str | Path,
) -> Path:

    info("Merging Directory Enumeration Results")

    all_results: set[str] = set()

    for file in file_list:

        file_path = Path(file)

        if not file_path.exists():
            continue

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as f:

            for line in f:

                line = line.strip()

                if line:
                    all_results.add(line)

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as out:

        for item in sorted(all_results):

            out.write(item + "\n")

    success(f"Merged Directory Results Saved: {output_path}")

    return output_path