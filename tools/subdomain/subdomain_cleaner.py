"""Subdomain cleaning utilities.

Some tools may output malformed lines, blank lines, or duplicates.
This module provides a simple cleaner to normalize and filter.

Note: Full validation of domain syntax is intentionally lightweight here.
"""

from __future__ import annotations

from pathlib import Path


def clean_subdomains(input_file: str | Path, output_file: str | Path) -> Path:
    """Strip whitespace, drop empty lines, and deduplicate."""

    in_path = Path(input_file)
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    unique: set[str] = set()
    if in_path.exists():
        with in_path.open("r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                # Drop protocol if present (http(s)://sub.example.com)
                if "://" in line:
                    line = line.split("://", 1)[1]
                # Drop trailing paths
                if "/" in line:
                    line = line.split("/", 1)[0]
                if line:
                    unique.add(line)

    with out_path.open("w", encoding="utf-8") as out:
        for item in sorted(unique):
            out.write(item + "\n")

    return out_path

