# =========================================
# FILE: scripts/check_tools.py
# TOOL VERIFICATION SCRIPT
# =========================================

from __future__ import annotations

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
from core.dependency_checker import DependencyChecker


logger = Logger()


def print_summary(report: dict) -> None:

    installed = report.get(
        "installed",
        [],
    )

    missing = report.get(
        "missing",
        [],
    )

    print("\n" + "=" * 70)
    print("TOOL VERIFICATION SUMMARY")
    print("=" * 70)

    print(
        f"\nInstalled Tools: {len(installed)}"
    )

    for tool in installed:
        print(f"  [+] {tool}")

    print(
        f"\nMissing Tools: {len(missing)}"
    )

    if missing:

        for tool in missing:
            print(f"  [-] {tool}")

    else:

        print("  None")

    print("\n" + "=" * 70)


def main():

    logger.phase(
        "CHECKING TOOL DEPENDENCIES"
    )

    checker = DependencyChecker()

    report = checker.check_all()

    print_summary(report)

    missing = report.get(
        "missing",
        [],
    )

    if missing:

        logger.warning(
            f"{len(missing)} tools missing"
        )

        sys.exit(1)

    logger.success(
        "All required tools are installed"
    )

    sys.exit(0)


if __name__ == "__main__":
    main()