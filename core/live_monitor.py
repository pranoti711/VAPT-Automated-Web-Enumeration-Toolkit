
from __future__ import annotations

import sys
import time
import threading
from datetime import datetime
from typing import Optional

try:
    from colorama import Fore, Style, init # type: ignore

    init(autoreset=True)

except ImportError:
    class Fore:
        CYAN = ""
        GREEN = ""
        YELLOW = ""
        RED = ""
        MAGENTA = ""
        BLUE = ""
        WHITE = ""

    class Style:
        RESET_ALL = ""

    def init(*args, **kwargs):
        pass


INFO_COLOR = Fore.CYAN
SUCCESS_COLOR = Fore.GREEN
WARNING_COLOR = Fore.YELLOW
ERROR_COLOR = Fore.RED
DEBUG_COLOR = Fore.MAGENTA
PHASE_COLOR = Fore.BLUE
RESET = Style.RESET_ALL


def timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _print(
    prefix: str,
    color: str,
    message: str,
) -> None:

    try:
        print(
            f"{color}[{timestamp()}] "
            f"{prefix} {message}{RESET}",
            flush=True,
        )
    except Exception:
        pass


def info(message: str) -> None:
    _print("[INFO]", INFO_COLOR, message)


def success(message: str) -> None:
    _print("[SUCCESS]", SUCCESS_COLOR, message)


def warning(message: str) -> None:
    _print("[WARNING]", WARNING_COLOR, message)


def error(message: str) -> None:
    _print("[ERROR]", ERROR_COLOR, message)


def debug(message: str) -> None:
    _print("[DEBUG]", DEBUG_COLOR, message)


def live(message: str) -> None:
    _print("[LIVE]", Fore.WHITE, message)


def phase(title: str) -> None:
    line = "=" * 70

    print()
    print(f"{PHASE_COLOR}{line}{RESET}", flush=True)
    print(f"{PHASE_COLOR}[PHASE] {title.upper()}{RESET}", flush=True)
    print(f"{PHASE_COLOR}{line}{RESET}", flush=True)


def section(title: str) -> None:
    line = "-" * 60

    print()
    print(f"{PHASE_COLOR}{line}{RESET}", flush=True)
    print(f"{PHASE_COLOR}{title}{RESET}", flush=True)
    print(f"{PHASE_COLOR}{line}{RESET}", flush=True)


def banner() -> None:
    art = r"""
██╗   ██╗ █████╗ ██████╗ ████████╗
██║   ██║██╔══██╗██╔══██╗╚══██╔══╝
██║   ██║███████║██████╔╝   ██║
╚██╗ ██╔╝██╔══██║██╔═══╝    ██║
 ╚████╔╝ ██║  ██║██║        ██║
  ╚═══╝  ╚═╝  ╚═╝╚═╝        ╚═╝

 █████╗ ██╗   ██╗████████╗ ██████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
███████║██║   ██║   ██║   ██║   ██║
██╔══██║██║   ██║   ██║   ██║   ██║
██║  ██║╚██████╔╝   ██║   ╚██████╔╝
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝

VAPT AUTOMATION FRAMEWORK
Production Recon Engine
"""

    print(f"{Fore.RED}{art}{RESET}", flush=True)


def progress_bar(
    current: int,
    total: int,
    prefix: str = "",
    length: int = 40,
) -> None:

    if total <= 0:
        total = 1

    percent = current / total
    filled = int(length * percent)

    bar = "█" * filled + "-" * (length - filled)

    sys.stdout.write(
        f"\r{INFO_COLOR}"
        f"{prefix} "
        f"|{bar}| "
        f"{current}/{total}"
        f"{RESET}"
    )

    sys.stdout.flush()

    if current >= total:
        print()


class Spinner:
    """
    Live terminal spinner.
    """

    def __init__(
        self,
        message: str = "Processing",
    ):

        self.message = message
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.spinner_chars = ["|", "/", "-", "\\"]

    def _spin(self) -> None:
        idx = 0

        while self.running:
            char = self.spinner_chars[
                idx % len(self.spinner_chars)
            ]

            sys.stdout.write(
                f"\r{INFO_COLOR}"
                f"[{char}] "
                f"{self.message}"
                f"{RESET}"
            )

            sys.stdout.flush()

            idx += 1
            time.sleep(0.1)

    def start(self) -> None:
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._spin,
            daemon=True,
        )

        self.thread.start()

    def stop(
        self,
        success_status: bool = True,
    ) -> None:

        self.running = False

        if self.thread:
            self.thread.join()

        status = (
            f"{SUCCESS_COLOR}[DONE]"
            if success_status
            else f"{ERROR_COLOR}[FAILED]"
        )

        sys.stdout.write(
            f"\r{status} "
            f"{self.message}"
            f"{' ' * 20}\n"
        )

        sys.stdout.flush()


def tool_start(tool_name: str) -> None:
    info(f"Starting Tool: {tool_name}")


def tool_end(
    tool_name: str,
    duration: Optional[float] = None,
) -> None:

    if duration is not None:
        success(
            f"{tool_name} completed "
            f"in {duration:.2f}s"
        )
    else:
        success(f"{tool_name} completed")


def tool_success(tool_name: str) -> None:
    success(f"{tool_name} completed")


def tool_failed(
    tool_name: str,
    reason: str = "",
) -> None:

    if reason:
        error(f"{tool_name} failed: {reason}")
    else:
        error(f"{tool_name} failed")


def tool_missing(tool_name: str) -> None:
    warning(f"{tool_name} missing")


def tool_error(
    tool_name: str,
    err: str,
) -> None:

    error(f"{tool_name} failed: {err}")


def phase_start(phase_name: str) -> None:
    phase(f"STARTING {phase_name}")


def phase_done(phase_name: str) -> None:
    phase(f"COMPLETED {phase_name}")


def scan_start(target: str) -> None:
    phase("SCAN STARTED")
    info(f"Target: {target}")


def scan_done(target: str) -> None:
    phase("SCAN COMPLETED")
    success(f"Target completed: {target}")


def scan_failed(target: str, reason: str) -> None:
    phase("SCAN FAILED")
    error(f"Target failed: {target}")
    error(reason)


def count_result(label: str, count: int) -> None:
    success(f"{label}: {count}")


def final_summary(stats: dict) -> None:
    phase("FINAL RECON SUMMARY")

    for key, value in stats.items():
        print(
            f"{SUCCESS_COLOR}"
            f"{key:<20}: {value}"
            f"{RESET}",
            flush=True,
        )


def show_summary(summary: dict) -> None:
    final_summary(summary)


def separator(title: str = "") -> None:
    line = "=" * 70

    if title:
        print(
            f"{PHASE_COLOR}{line} {title} {line}{RESET}",
            flush=True,
        )
    else:
        print(
            f"{PHASE_COLOR}{line}{RESET}",
            flush=True,
        )