# Auto-generated file
# =========================================
# FILE: scripts/export_report.py
# EXPORT GENERATED REPORTS
# =========================================

from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.logger import Logger


logger = Logger()

OUTPUT_DIR = PROJECT_ROOT / "outputs"
EXPORT_DIR = PROJECT_ROOT / "exports"


def list_scan_folders() -> list[Path]:

    if not OUTPUT_DIR.exists():
        return []

    return sorted(
        [
            item
            for item in OUTPUT_DIR.iterdir()
            if item.is_dir()
        ],
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )


def copy_reports(
    scan_dir: Path,
    export_dir: Path,
) -> Path:

    reports_dir = scan_dir / "reports"
    metadata_dir = scan_dir / "metadata"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    destination = export_dir / f"{scan_dir.name}_export_{timestamp}"

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    if reports_dir.exists():
        shutil.copytree(
            reports_dir,
            destination / "reports",
            dirs_exist_ok=True,
        )

    if metadata_dir.exists():
        shutil.copytree(
            metadata_dir,
            destination / "metadata",
            dirs_exist_ok=True,
        )

    logger.success(
        f"Report exported to: {destination}"
    )

    return destination


def export_latest_scan() -> None:

    scans = list_scan_folders()

    if not scans:
        logger.warning("No scan folders found")
        return

    latest_scan = scans[0]

    logger.info(
        f"Exporting latest scan: {latest_scan.name}"
    )

    copy_reports(
        latest_scan,
        EXPORT_DIR,
    )


def export_selected_scan() -> None:

    scans = list_scan_folders()

    if not scans:
        logger.warning("No scan folders found")
        return

    print("\nAvailable scans:\n")

    for index, scan in enumerate(scans, start=1):
        print(f"{index}. {scan.name}")

    choice = input("\nSelect scan number: ").strip()

    if not choice.isdigit():
        logger.warning("Invalid choice")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(scans):
        logger.warning("Invalid scan number")
        return

    copy_reports(
        scans[index],
        EXPORT_DIR,
    )


def menu() -> None:

    while True:

        print(
            """
==================================
REPORT EXPORTER
==================================

1. Export Latest Scan Report
2. Export Selected Scan Report
3. Exit
"""
        )

        choice = input("Choice: ").strip()

        if choice == "1":
            export_latest_scan()

        elif choice == "2":
            export_selected_scan()

        elif choice == "3":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()