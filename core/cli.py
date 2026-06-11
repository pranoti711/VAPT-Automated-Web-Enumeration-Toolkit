

from __future__ import annotations

import asyncio
import os
import re

from core.logger import Logger
from core.live_monitor import (
    banner,
    info,
    success,
    warning,
    error,
)
from core.dependency_checker import (
    verify_tools,
    auto_fix_dependencies,
)
from core.tool_installer import (
    install_all_tools,
    install_tool,
    install_category,
)
from core.recon_engine_async import start_async_scan
from core.output_manager import create_scan_structure


def is_valid_target(target: str) -> bool:
    pattern = re.compile(
        r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    )

    return bool(
        pattern.match(target.strip().lower())
    )


class CLI:
    """
    Final command-line controller.
    """

    def __init__(self):
        self.logger = Logger()

    def show_help(self) -> None:
        print(
            """

Commands:
---------

install
    Install all registered tools

install-tool <tool>
    Install one tool
    Example: install-tool subfinder

install-category <category>
    Install tools by category
    Example: install-category subdomain

check
    Check all dependencies

fix
    Auto-install missing dependencies

scan
    Start interactive scan setup

scan <target>
    Run normal scan directly
    Example: scan example.com

scan-fast <target>
    Run scan in fast mode

scan-stealth <target>
    Run scan in stealth mode

scan-noverify <target>
    Run scan without dependency verification

output <target>
    Create output folder structure only

clear
    Clear terminal

help
    Show this menu

exit
    Exit CLI

====================================================
"""
        )


    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")


    def install_all(self) -> None:
        info("Installing all tools...")
        install_all_tools()

    def install_single(self, tool_name: str) -> None:
        if not tool_name:
            error("Tool name missing")
            return

        install_tool(tool_name)

    def install_by_category(self, category: str) -> None:
        if not category:
            error("Category missing")
            return

        install_category(category)


    def check_dependencies(self) -> None:
        report = verify_tools()

        print("\nInstalled:")
        for tool in report.get("installed", []):
            print(f"  ✅ {tool}")

        print("\nMissing:")
        for tool in report.get("missing", []):
            print(f"  ❌ {tool}")

    def fix_dependencies(self) -> None:
        auto_fix_dependencies()


    def create_output(self, target: str) -> None:
        if not target:
            error("Target missing")
            return

        if not is_valid_target(target):
            error("Invalid target domain")
            return

        path = create_scan_structure(target)
        success(f"Output structure created: {path}")


    def interactive_scan_setup(self) -> tuple[str, str, bool] | None:
        print(
            "\n================ SCAN SETUP ================\n"
        )

        target = input("Enter Target Domain: ").strip()

        if not target:
            error("Target cannot be empty")
            return None

        if not is_valid_target(target):
            error("Invalid target domain")
            return None

        print(
            """
================ SCAN MODES ================

[1] FAST MODE
    Faster execution, more parallelism

[2] NORMAL MODE
    Balanced and recommended

[3] STEALTH MODE
    Slower execution with delays

============================================
"""
        )

        mode_choice = input("Select Scan Mode: ").strip()

        if mode_choice == "1":
            mode = "fast"
        elif mode_choice == "2":
            mode = "normal"
        elif mode_choice == "3":
            mode = "stealth"
        else:
            warning("Invalid mode selected, defaulting to NORMAL")
            mode = "normal"

        verify_choice = input(
            "Verify tools before scan? (y/n): "
        ).strip().lower()

        verify = verify_choice != "n"

        output_dir = create_scan_structure(target)

        print(
            f"""
================ SCAN SUMMARY ================

Target      : {target}
Mode        : {mode}
Verify      : {verify}
Output Dir  : {output_dir}

================================================
"""
        )

        confirm = input("Start scan? (y/n): ").strip().lower()

        if confirm != "y":
            warning("Scan cancelled")
            return None

        return target, mode, verify

    async def run_scan_async(
        self,
        target: str,
        mode: str = "normal",
        verify: bool = True,
    ) -> None:
        if not target:
            error("Target missing")
            return

        if not is_valid_target(target):
            error("Invalid target domain")
            return

        info(f"Starting scan for {target}")
        info(f"Mode: {mode}")

        result = await start_async_scan(
            target=target,
            mode=mode,
            verify_tools=verify,
        )

        if result.get("status") == "completed":
            success("Scan completed successfully")
        else:
            warning(
                f"Scan ended with status: {result.get('status')}"
            )

    def run_scan(
        self,
        target: str,
        mode: str = "normal",
        verify: bool = True,
    ) -> None:
        try:
            asyncio.run(
                self.run_scan_async(
                    target=target,
                    mode=mode,
                    verify=verify,
                )
            )

        except KeyboardInterrupt:
            warning("Scan interrupted by user")

        except Exception as e:
            error(f"Scan failed: {e}")

    def run_interactive_scan(self) -> None:
        setup = self.interactive_scan_setup()

        if setup is None:
            return

        target, mode, verify = setup

        self.run_scan(
            target=target,
            mode=mode,
            verify=verify,
        )

    def execute_command(self, command_line: str) -> bool:
        parts = command_line.strip().split()

        if not parts:
            return True

        command = parts[0].lower()
        args = parts[1:]

        if command == "install":
            self.install_all()

        elif command == "install-tool":
            self.install_single(
                args[0] if args else ""
            )

        elif command == "install-category":
            self.install_by_category(
                args[0] if args else ""
            )

        elif command == "check":
            self.check_dependencies()

        elif command == "fix":
            self.fix_dependencies()

        elif command == "scan":
            if args:
                self.run_scan(
                    args[0],
                    mode="normal",
                    verify=True,
                )
            else:
                self.run_interactive_scan()

        elif command == "scan-fast":
            self.run_scan(
                args[0] if args else "",
                mode="fast",
                verify=True,
            )

        elif command == "scan-stealth":
            self.run_scan(
                args[0] if args else "",
                mode="stealth",
                verify=True,
            )

        elif command == "scan-noverify":
            self.run_scan(
                args[0] if args else "",
                mode="normal",
                verify=False,
            )

        elif command == "output":
            self.create_output(
                args[0] if args else ""
            )

        elif command == "clear":
            self.clear()

        elif command == "help":
            self.show_help()

        elif command == "exit":
            warning("Exiting framework...")
            return False

        else:
            error(f"Unknown command: {command}")
            self.show_help()

        return True


    def interactive_loop(self) -> None:
        banner()
        self.show_help()

        while True:
            try:
                command_line = input("\nVAPT> ").strip()

                if not command_line:
                    continue

                running = self.execute_command(command_line)

                if running is False:
                    break

            except KeyboardInterrupt:
                print()
                warning("Use 'exit' to quit")

            except Exception as e:
                error(str(e))

def run_cli() -> None:
    cli = CLI()
    cli.interactive_loop()


if __name__ == "__main__":
    run_cli()