
from __future__ import annotations

import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from core.logger import Logger


class ErrorHandler:
    """
    Central error handler for the framework.

    Responsibilities:
    -----------------
    - Handle crashes
    - Handle tool failures
    - Track exceptions
    - Save error reports
    - Support retry decisions
    """

    def __init__(
        self,
        log_dir: str | Path = "outputs/logs",
    ):
        self.logger = Logger(log_dir=log_dir)
        self.errors: list[Dict[str, Any]] = []

    def capture_exception(
        self,
        exc: Exception,
        context: str = "",
        fatal: bool = False,
    ) -> Dict[str, Any]:

        error_data = {
            "timestamp": str(datetime.now()),
            "type": type(exc).__name__,
            "message": str(exc),
            "context": context,
            "fatal": fatal,
            "traceback": traceback.format_exc(),
        }

        self.errors.append(error_data)

        self.logger.error(
            f"{error_data['type']} | {context} | {error_data['message']}"
        )

        return error_data

    def capture_tool_error(
        self,
        tool_name: str,
        stderr: str = "",
        returncode: int | None = None,
        command: str = "",
    ) -> Dict[str, Any]:

        error_data = {
            "timestamp": str(datetime.now()),
            "tool": tool_name,
            "command": command,
            "returncode": returncode,
            "stderr": stderr,
        }

        self.errors.append(error_data)

        self.logger.tool(
            tool_name,
            f"FAILED | code={returncode} | {stderr}",
        )

        return error_data

    def should_retry(
        self,
        error_text: str,
        attempt: int,
        max_retries: int,
    ) -> bool:

        if attempt >= max_retries:
            return False

        retry_keywords = [
            "timeout",
            "temporarily unavailable",
            "connection reset",
            "connection refused",
            "rate limit",
            "too many requests",
            "network",
            "dns",
        ]

        lower = error_text.lower()

        return any(
            keyword in lower
            for keyword in retry_keywords
        )

    def save_report(
        self,
        output_file: str | Path,
    ) -> Path:

        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)

        content = []

        for item in self.errors:
            content.append("=" * 70)
            for key, value in item.items():
                content.append(f"{key}: {value}")
            content.append("")

        path.write_text(
            "\n".join(content),
            encoding="utf-8",
            errors="ignore",
        )

        return path

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def clear(self) -> None:
        self.errors.clear()


error_handler = ErrorHandler()