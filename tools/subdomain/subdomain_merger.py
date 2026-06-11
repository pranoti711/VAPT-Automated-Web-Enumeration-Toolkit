"""Subdomain merging utilities.

The main subdomain pipeline can merge raw tool outputs into a single cleaned
list.

This module provides:
- `merge_unique_lines(files, output_file)`
- Optional normalization (strip whitespace)
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from core.live_monitor import success


def merge_unique_lines(files: Iterable[str | Path], output_file: str | Path) -> Path:
    """Merge multiple text files into one file with unique non-empty lines."""

    unique: set[str] = set()

    for f in files:
        path = Path(f)
        if not path.exists():
            continue

        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    unique.add(line)

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as out:
        for item in sorted(unique):
            out.write(item + "\n")

    success("Merged File Created:")
    print(str(out_path))
    return out_path

