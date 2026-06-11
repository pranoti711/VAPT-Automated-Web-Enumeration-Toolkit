
from __future__ import annotations

import asyncio
import os
import signal
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

from core.logger import Logger


class ProcessManager:
    """
    Central process manager.

    Responsibilities:
    -----------------
    - Track running processes
    - Kill hanging tools
    - Stop all scans safely
    - Handle Ctrl+C cleanup
    - Store process metadata

    Used by:
    --------
    - executor.py
    - tool_executor.py
    - workflow_engine.py
    - recon_engine_async.py
    """

    def __init__(self):
        self.logger = Logger()
        self.processes: Dict[int, Dict[str, Any]] = {}

    def register_process(
        self,
        process: asyncio.subprocess.Process | subprocess.Popen,
        tool_name: str,
        command: str,
    ) -> None:

        pid = process.pid

        if pid is None:
            return

        self.processes[pid] = {
            "pid": pid,
            "tool_name": tool_name,
            "command": command,
            "process": process,
            "status": "running",
        }

        self.logger.debug(
            f"Registered process PID={pid} TOOL={tool_name}"
        )

    def unregister_process(
        self,
        pid: int,
    ) -> None:

        if pid in self.processes:
            self.processes[pid]["status"] = "finished"
            del self.processes[pid]

    def list_processes(self) -> list[Dict[str, Any]]:
        return [
            {
                "pid": data["pid"],
                "tool_name": data["tool_name"],
                "command": data["command"],
                "status": data["status"],
            }
            for data in self.processes.values()
        ]

    def get_process(
        self,
        pid: int,
    ) -> Optional[Dict[str, Any]]:

        return self.processes.get(pid)

    async def kill_async_process(
        self,
        process: asyncio.subprocess.Process,
    ) -> bool:

        try:
            if process.returncode is None:
                process.kill()
                await process.wait()

            return True

        except Exception as e:
            self.logger.error(
                f"Failed to kill async process: {e}"
            )
            return False

    def kill_sync_process(
        self,
        process: subprocess.Popen,
    ) -> bool:

        try:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)

            return True

        except Exception as e:
            self.logger.error(
                f"Failed to kill sync process: {e}"
            )
            return False

    async def kill_by_pid(
        self,
        pid: int,
    ) -> bool:

        data = self.processes.get(pid)

        if not data:
            return False

        process = data.get("process")

        try:
            if isinstance(process, asyncio.subprocess.Process):
                killed = await self.kill_async_process(process)
            else:
                killed = self.kill_sync_process(process)

            if killed:
                self.unregister_process(pid)
                self.logger.warning(f"Killed process PID={pid}")

            return killed

        except Exception as e:
            self.logger.error(
                f"Failed killing PID={pid}: {e}"
            )
            return False

    async def kill_tool(
        self,
        tool_name: str,
    ) -> int:

        killed = 0

        for pid, data in list(self.processes.items()):
            if data.get("tool_name") == tool_name:
                if await self.kill_by_pid(pid):
                    killed += 1

        return killed

    async def kill_all(self) -> int:
        killed = 0

        for pid in list(self.processes.keys()):
            if await self.kill_by_pid(pid):
                killed += 1

        self.processes.clear()

        self.logger.warning(
            f"Killed all running processes: {killed}"
        )

        return killed

    def terminate_by_os_pid(
        self,
        pid: int,
    ) -> bool:

        try:
            if os.name == "nt":
                subprocess.run(
                    [
                        "taskkill",
                        "/PID",
                        str(pid),
                        "/F",
                        "/T",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            else:
                os.kill(pid, signal.SIGTERM)

            return True

        except Exception as e:
            self.logger.error(
                f"OS terminate failed PID={pid}: {e}"
            )
            return False

    def has_running_processes(self) -> bool:
        return bool(self.processes)

    def count(self) -> int:
        return len(self.processes)

    def clear_finished(self) -> None:
        for pid, data in list(self.processes.items()):
            process = data.get("process")

            try:
                if isinstance(process, asyncio.subprocess.Process):
                    if process.returncode is not None:
                        self.unregister_process(pid)
                else:
                    if process.poll() is not None:
                        self.unregister_process(pid)
            except Exception:
                continue


process_manager = ProcessManager()