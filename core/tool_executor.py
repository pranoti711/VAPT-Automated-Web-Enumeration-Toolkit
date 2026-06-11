
from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

from core.executor import executor
from core.logger import Logger


logger = Logger()


def is_tool_installed(tool_name: str) -> bool:
    return shutil.which(tool_name) is not None


def execute_tool(
    command: str,
    output_file: str | None = None,
    working_dir: str | None = None,
) -> bool:

    async def _run():
        result = await executor.execute_shell(
            command=command,
            tool_name="legacy",
            cwd=working_dir,
        )

        if output_file:
            path = Path(output_file)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                result.get("stdout", ""),
                encoding="utf-8",
                errors="ignore",
            )

        return result.get("success", False)

    try:
        return asyncio.run(_run())

    except RuntimeError:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_run())

    except Exception as e:
        logger.error(f"Legacy execute_tool failed: {e}")
        return False


def test_tool(tool_name: str) -> None:
    if is_tool_installed(tool_name):
        logger.success(f"{tool_name} is installed")
    else:
        logger.error(f"{tool_name} is NOT installed")