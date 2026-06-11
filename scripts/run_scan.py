# =========================================
# FILE: scripts/run_scan.py
# QUICK SCAN LAUNCHER
# =========================================

from __future__ import annotations

import sys
import argparse
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
from core.recon_engine import start_scan

logger = Logger()


# =========================================
# ARGUMENTS
# =========================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="VAPT Automation Framework"
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain",
    )

    parser.add_argument(
        "-m",
        "--mode",
        default="normal",
        choices=[
            "quick",
            "normal",
            "deep",
        ],
        help="Scan mode",
    )

    parser.add_argument(
        "--skip-tools-check",
        action="store_true",
        help="Skip dependency verification",
    )

    return parser.parse_args()


# =========================================
# BANNER
# =========================================

def banner():

    print(
        r"""
 __      ___    ____ _____
 \ \    / / \  |  _ \_   _|
  \ \/\/ / _ \ | |_) || |
   \_/\_/_/ \_\|____/ |_|

VAPT AUTOMATION FRAMEWORK
"""
    )


# =========================================
# MAIN
# =========================================

def main():

    banner()

    args = parse_arguments()

    logger.phase("SCAN CONFIGURATION")

    logger.info(
        f"Target : {args.domain}"
    )

    logger.info(
        f"Mode   : {args.mode}"
    )

    logger.info(
        f"Verify : {not args.skip_tools_check}"
    )

    try:

        result = start_scan(
            target=args.domain,
            mode=args.mode,
            verify_tools=not args.skip_tools_check,
        )

        print("\n")
        print("=" * 70)
        print("SCAN COMPLETED")
        print("=" * 70)

        print(
            f"Status       : {result.get('status')}"
        )

        print(
            f"Subdomains   : {len(result.get('subdomains', []))}"
        )

        print(
            f"Alive Hosts  : {len(result.get('alive_hosts', []))}"
        )

        print(
            f"URLs         : {len(result.get('urls', []))}"
        )

        print(
            f"Parameters   : {len(result.get('parameters', []))}"
        )

        print(
            f"Directories  : {len(result.get('directories', []))}"
        )

        print("=" * 70)

    except KeyboardInterrupt:

        logger.warning(
            "Scan interrupted by user"
        )

        sys.exit(1)

    except Exception as exc:

        logger.error(
            f"Scan failed: {exc}"
        )

        sys.exit(1)


# =========================================
# ENTRYPOINT
# =========================================

if __name__ == "__main__":
    main()