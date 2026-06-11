

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from threading import Lock


class Logger:

    _lock = Lock()

    def __init__(
        self,
        log_dir: str | Path = "outputs/logs",
    ):

        self.log_dir = Path(log_dir)

        self.log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.framework_log = self.log_dir / "framework.log"
        self.error_log = self.log_dir / "errors.log"
        self.tools_log = self.log_dir / "tools.log"
        self.debug_log = self.log_dir / "debug.log"
        self.live_log = self.log_dir / "live_output.log"

        self.info("Logger initialized")


    def _write(
        self,
        level: str,
        message: str,
        file_path: Path,
    ) -> None:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = f"[{timestamp}] [{level}] {message}"

        with self._lock:

            # Console output
            try:
                print(line, flush=True)
            except Exception:
                pass

            # File output
            try:
                with open(
                    file_path,
                    "a",
                    encoding="utf-8",
                ) as f:
                    f.write(line + "\n")
            except Exception:
                pass


    def info(
        self,
        message: str,
    ) -> None:

        self._write(
            "INFO",
            message,
            self.framework_log,
        )

    def success(
        self,
        message: str,
    ) -> None:

        self._write(
            "SUCCESS",
            message,
            self.framework_log,
        )

    def warning(
        self,
        message: str,
    ) -> None:

        self._write(
            "WARNING",
            message,
            self.framework_log,
        )

    def error(
        self,
        message: str,
    ) -> None:

        self._write(
            "ERROR",
            message,
            self.error_log,
        )

    def debug(
        self,
        message: str,
    ) -> None:

        self._write(
            "DEBUG",
            message,
            self.debug_log,
        )

    def tool(
        self,
        tool_name: str,
        message: str,
    ) -> None:

        self._write(
            tool_name.upper(),
            message,
            self.tools_log,
        )


    def live(
        self,
        message: str,
    ) -> None:

        self._write(
            "LIVE",
            message,
            self.live_log,
        )

    def exception(
        self,
        exc: Exception,
    ) -> None:

        self.error(
            f"{type(exc).__name__}: {exc}"
        )


    def separator(
        self,
        title: str = "",
    ) -> None:

        line = "=" * 70

        if title:
            self.info(
                f"{line} {title} {line}"
            )
        else:
            self.info(line)

    def banner(
        self,
        title: str,
    ) -> None:

        border = "=" * 80

        self.info(border)
        self.info(title)
        self.info(border)


    def phase(
        self,
        phase_name: str,
    ) -> None:

        self.separator(
            f"STARTING {phase_name}"
        )

    def get_log_directory(self) -> Path:

        return self.log_dir

    def get_framework_log(self) -> Path:

        return self.framework_log

    def get_error_log(self) -> Path:

        return self.error_log

    def get_tools_log(self) -> Path:

        return self.tools_log

    def get_debug_log(self) -> Path:

        return self.debug_log

    def get_live_log(self) -> Path:

        return self.live_log