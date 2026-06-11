# Auto-generated file
# =========================================
# FILE: scripts/clean_output.py
# CLEAN OUTPUT DIRECTORIES
# =========================================

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# =========================================
# PROJECT ROOT
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# =========================================
# IMPORTS
# =========================================

from core.logger import Logger

logger = Logger()

# =========================================
# DIRECTORIES TO CLEAN
# =========================================

OUTPUT_DIR = PROJECT_ROOT / "outputs"

SAFE_DIRECTORIES = [
    "subdomains",
    "httpx",
    "urls",
    "parameters",
    "gf_patterns",
    "directories",
    "reports",
    "metadata",
    "temp",
]

# =========================================
# REMOVE DIRECTORY
# =========================================

def remove_directory(
    directory: Path,
) -> bool:

    try:

        if directory.exists():

            shutil.rmtree(directory)

            logger.success(
                f"Removed: {directory}"
            )

        return True

    except Exception as exc:

        logger.error(
            f"Failed removing {directory}: {exc}"
        )

        return False


# =========================================
# REMOVE FILES
# =========================================

def remove_files(
    directory: Path,
) -> int:

    deleted = 0

    try:

        for item in directory.iterdir():

            if item.is_file():

                item.unlink()

                deleted += 1

        return deleted

    except Exception as exc:

        logger.error(
            f"Failed cleaning files: {exc}"
        )

        return deleted


# =========================================
# CLEAN SCAN DIRECTORY
# =========================================

def clean_scan_directory(
    scan_directory: Path,
) -> None:

    logger.info(
        f"Cleaning scan: {scan_directory.name}"
    )

    for folder in SAFE_DIRECTORIES:

        path = scan_directory / folder

        if path.exists():

            remove_directory(path)

    logger.success(
        f"Scan cleaned: {scan_directory.name}"
    )


# =========================================
# CLEAN ALL OUTPUTS
# =========================================

def clean_all_outputs() -> None:

    logger.phase(
        "CLEANING OUTPUT DIRECTORY"
    )

    if not OUTPUT_DIR.exists():

        logger.warning(
            "Outputs directory does not exist"
        )

        return

    scan_directories = [
        item
        for item in OUTPUT_DIR.iterdir()
        if item.is_dir()
    ]

    if not scan_directories:

        logger.warning(
            "No scan outputs found"
        )

        return

    for scan_dir in scan_directories:

        clean_scan_directory(
            scan_dir
        )

    logger.success(
        "Output cleanup completed"
    )


# =========================================
# DELETE EVERYTHING
# =========================================

def delete_all_outputs() -> None:

    logger.phase(
        "DELETING ALL OUTPUTS"
    )

    if not OUTPUT_DIR.exists():

        logger.warning(
            "Outputs directory not found"
        )

        return

    confirm = input(
        "\nDelete ALL output folders? (yes/no): "
    ).strip().lower()

    if confirm != "yes":

        logger.warning(
            "Operation cancelled"
        )

        return

    for item in OUTPUT_DIR.iterdir():

        try:

            if item.is_dir():

                shutil.rmtree(item)

            else:

                item.unlink()

        except Exception as exc:

            logger.error(
                f"Failed removing {item}: {exc}"
            )

    logger.success(
        "All outputs deleted"
    )


# =========================================
# SHOW STATISTICS
# =========================================

def show_statistics() -> None:

    logger.phase(
        "OUTPUT STATISTICS"
    )

    if not OUTPUT_DIR.exists():

        logger.warning(
            "Outputs directory not found"
        )

        return

    scans = [
        item
        for item in OUTPUT_DIR.iterdir()
        if item.is_dir()
    ]

    print(
        f"\nTotal Scan Folders: {len(scans)}"
    )

    for scan in scans:

        file_count = sum(
            1
            for _
            in scan.rglob("*")
            if _.is_file()
        )

        print(
            f" - {scan.name}: "
            f"{file_count} files"
        )


# =========================================
# MENU
# =========================================

def menu():

    while True:

        print(
            """
==================================
OUTPUT CLEANER
==================================

1. Clean Scan Contents
2. Delete All Outputs
3. Show Statistics
4. Exit
"""
        )

        choice = input(
            "Choice: "
        ).strip()

        if choice == "1":

            clean_all_outputs()

        elif choice == "2":

            delete_all_outputs()

        elif choice == "3":

            show_statistics()

        elif choice == "4":

            break

        else:

            print("Invalid choice")


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    menu()