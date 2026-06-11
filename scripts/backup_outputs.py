# Auto-generated file
# =========================================
# FILE: scripts/backup.py
# PROJECT / OUTPUT BACKUP MANAGER
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
BACKUP_DIR = PROJECT_ROOT / "backups"


# =========================================
# TIMESTAMP
# =========================================

def timestamp() -> str:
    return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


# =========================================
# CREATE BACKUP DIR
# =========================================

def ensure_backup_dir() -> None:

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# =========================================
# ZIP DIRECTORY
# =========================================

def zip_directory(
    source: Path,
    destination_name: str,
) -> Path:

    ensure_backup_dir()

    archive_base = (
        BACKUP_DIR / destination_name
    )

    archive_path = shutil.make_archive(
        base_name=str(archive_base),
        format="zip",
        root_dir=str(source),
    )

    return Path(archive_path)


# =========================================
# BACKUP OUTPUTS
# =========================================

def backup_outputs() -> None:

    logger.phase(
        "BACKUP OUTPUTS"
    )

    if not OUTPUT_DIR.exists():

        logger.warning(
            "Outputs directory not found"
        )

        return

    backup_name = (
        f"outputs_backup_{timestamp()}"
    )

    archive = zip_directory(
        OUTPUT_DIR,
        backup_name,
    )

    logger.success(
        f"Backup created: {archive}"
    )


# =========================================
# BACKUP PROJECT
# =========================================

def backup_project() -> None:

    logger.phase(
        "BACKUP PROJECT"
    )

    backup_name = (
        f"project_backup_{timestamp()}"
    )

    archive = zip_directory(
        PROJECT_ROOT,
        backup_name,
    )

    logger.success(
        f"Backup created: {archive}"
    )


# =========================================
# LIST BACKUPS
# =========================================

def list_backups() -> None:

    logger.phase(
        "AVAILABLE BACKUPS"
    )

    ensure_backup_dir()

    backups = sorted(
        BACKUP_DIR.glob("*.zip"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not backups:

        logger.warning(
            "No backups found"
        )

        return

    print()

    for index, backup in enumerate(
        backups,
        start=1,
    ):

        size_mb = (
            backup.stat().st_size
            / (1024 * 1024)
        )

        print(
            f"{index}. "
            f"{backup.name} "
            f"({size_mb:.2f} MB)"
        )


# =========================================
# DELETE BACKUP
# =========================================

def delete_backup() -> None:

    ensure_backup_dir()

    backups = sorted(
        BACKUP_DIR.glob("*.zip"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not backups:

        logger.warning(
            "No backups available"
        )

        return

    print()

    for index, backup in enumerate(
        backups,
        start=1,
    ):
        print(
            f"{index}. {backup.name}"
        )

    choice = input(
        "\nBackup number: "
    ).strip()

    if not choice.isdigit():

        logger.warning(
            "Invalid selection"
        )

        return

    index = int(choice) - 1

    if index < 0 or index >= len(backups):

        logger.warning(
            "Invalid backup"
        )

        return

    backup = backups[index]

    backup.unlink()

    logger.success(
        f"Deleted: {backup.name}"
    )


# =========================================
# RESTORE BACKUP
# =========================================

def restore_backup() -> None:

    ensure_backup_dir()

    backups = sorted(
        BACKUP_DIR.glob("*.zip"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not backups:

        logger.warning(
            "No backups available"
        )

        return

    print()

    for index, backup in enumerate(
        backups,
        start=1,
    ):
        print(
            f"{index}. {backup.name}"
        )

    choice = input(
        "\nBackup number: "
    ).strip()

    if not choice.isdigit():

        logger.warning(
            "Invalid selection"
        )

        return

    index = int(choice) - 1

    if index < 0 or index >= len(backups):

        logger.warning(
            "Invalid backup"
        )

        return

    selected = backups[index]

    restore_dir = (
        BACKUP_DIR
        / f"restore_{timestamp()}"
    )

    restore_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.unpack_archive(
        str(selected),
        str(restore_dir),
    )

    logger.success(
        f"Restored to: {restore_dir}"
    )


# =========================================
# MENU
# =========================================

def menu() -> None:

    while True:

        print(
            """
==================================
BACKUP MANAGER
==================================

1. Backup Outputs
2. Backup Entire Project
3. List Backups
4. Restore Backup
5. Delete Backup
6. Exit
"""
        )

        choice = input(
            "Choice: "
        ).strip()

        if choice == "1":

            backup_outputs()

        elif choice == "2":

            backup_project()

        elif choice == "3":

            list_backups()

        elif choice == "4":

            restore_backup()

        elif choice == "5":

            delete_backup()

        elif choice == "6":

            break

        else:

            print(
                "Invalid choice"
            )


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    menu()