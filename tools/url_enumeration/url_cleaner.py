"""URL cleaner.

Takes an input URL list and produces a de-duplicated cleaned output.

Output convention:
- <output_dir>/cleaned.txt
"""

from __future__ import annotations

from pathlib import Path

from core.live_monitor import info, success


def clean_urls(input_file: str | Path, output_file: str | Path) -> Path:
    input_path = Path(input_file)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    info(f"Cleaning URLs from {input_path}")

    urls: set[str] = set()
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            urls.add(line)

    with open(output_path, "w", encoding="utf-8") as out:
        for u in sorted(urls):
            out.write(u + "\n")

    success(f"Cleaned URLs saved: {output_path}")
    return output_path

