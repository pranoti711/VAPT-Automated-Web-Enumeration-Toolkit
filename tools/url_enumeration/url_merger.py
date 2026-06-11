"""URL merger.

Merges multiple URL text files into a single de-duplicated output.

Output convention:
- <output_file>
"""

from __future__ import annotations

from pathlib import Path

from core.live_monitor import info, success


def merge_url_files(file_list: list[str | Path], output_file: str | Path) -> Path:
    info("Merging URL files")

    urls: set[str] = set()

    for fp in file_list:
        p = Path(fp)
        if not p.exists():
            continue
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                u = line.strip()
                if u:
                    urls.add(u)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as out:
        for u in sorted(urls):
            out.write(u + "\n")

    success(f"Merged URLs saved: {output_path}")
    return output_path

