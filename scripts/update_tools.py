# Auto-generated file
# =========================================
# FILE: scripts/update_tools.py
# TOOL UPDATE MANAGER
# =========================================

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.logger import Logger
from core.tool_installer import ToolInstaller


TOOLS = [
    "subfinder",
    "assetfinder",
    "amass",
    "findomain",
    "github-subdomains",
    "subscraper",
    "httpx",
    "gau",
    "waybackurls",
    "katana",
    "paramspider",
    "arjun",
    "gf",
    "ffuf",
    "dirsearch",
    "feroxbuster",
]

CATEGORIES = {
    "subdomain": [
        "subfinder",
        "assetfinder",
        "amass",
        "findomain",
        "github-subdomains",
        "subscraper",
    ],
    "http": [
        "httpx",
    ],
    "url": [
        "gau",
        "waybackurls",
        "katana",
    ],
    "parameters": [
        "paramspider",
        "arjun",
    ],
    "gf": [
        "gf",
    ],
    "directory": [
        "ffuf",
        "dirsearch",
        "feroxbuster",
    ],
}


logger = Logger()


class ToolUpdater:

    def __init__(self):
        self.installer = ToolInstaller()

    def update_tool(self, tool_name: str) -> bool:
        if tool_name not in TOOLS:
            logger.error(f"Unknown tool: {tool_name}")
            return False

        logger.info(f"Updating {tool_name}")

        try:
            success = self.installer.install_tool(tool_name)

            if success:
                logger.success(f"{tool_name} updated")
            else:
                logger.warning(f"{tool_name} update failed")

            return success

        except Exception as exc:
            logger.error(f"{tool_name} update error: {exc}")
            return False

    def update_all(self) -> None:
        logger.phase("UPDATING ALL TOOLS")

        success_count = 0
        failed_count = 0

        for tool_name in TOOLS:
            if self.update_tool(tool_name):
                success_count += 1
            else:
                failed_count += 1

        logger.success(f"Updated: {success_count}")
        logger.warning(f"Failed: {failed_count}")

    def update_category(self, category: str) -> None:
        logger.phase(f"UPDATING CATEGORY: {category}")

        tools = CATEGORIES.get(category)

        if not tools:
            logger.warning(f"Unknown category: {category}")
            return

        for tool_name in tools:
            self.update_tool(tool_name)

    def show_tools(self) -> None:
        logger.phase("REGISTERED TOOLS")

        for tool_name in TOOLS:
            print(f" - {tool_name}")

    def show_categories(self) -> None:
        logger.phase("TOOL CATEGORIES")

        for category, tools in CATEGORIES.items():
            print(f"\n{category}:")
            for tool in tools:
                print(f"  - {tool}")


def menu() -> None:
    updater = ToolUpdater()

    while True:
        print(
            """
==================================
TOOL UPDATE MANAGER
==================================

1. Update All Tools
2. Update Single Tool
3. Update Category
4. List Tools
5. List Categories
6. Exit
"""
        )

        choice = input("Choice: ").strip()

        if choice == "1":
            updater.update_all()

        elif choice == "2":
            tool_name = input("Tool Name: ").strip().lower()
            updater.update_tool(tool_name)

        elif choice == "3":
            category = input("Category: ").strip().lower()
            updater.update_category(category)

        elif choice == "4":
            updater.show_tools()

        elif choice == "5":
            updater.show_categories()

        elif choice == "6":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()