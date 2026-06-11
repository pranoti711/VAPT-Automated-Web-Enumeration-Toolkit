
from __future__ import annotations

import asyncio
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.logger import Logger
from core.tool_registry import registry


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Executor:
    """Central async command executor."""

    def __init__(self):
        self.logger = Logger()
        self.processes: List[asyncio.subprocess.Process] = []

    def _resolve_httpx_binary(self) -> str:
        """
        Force ProjectDiscovery Go httpx,
        not Python httpx package.
        """

        possible_paths = [
            Path.home() / "go" / "bin" / "httpx.exe",
            Path.home() / "go" / "bin" / "httpx",
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        return "httpx"

    def is_tool_installed(self, tool_name: str) -> bool:
        tool = registry.get_tool(tool_name)

        script_path = tool.get("script_path")

        if script_path:
            return (PROJECT_ROOT / script_path).exists()

        binary = registry.get_binary(tool_name)

        if binary == "python":
            return True

        if shutil.which(binary):
            return True

        for alt_binary in tool.get("alternative_binaries", []):
            if shutil.which(alt_binary):
                return True

        return False

    # =====================================
    # BUILD COMMANDS
    # =====================================

    def build_command(
        self,
        tool_name: str,
        target: str | None = None,
        input_file: str | None = None,
        output_file: str | None = None,
        wordlist: str | None = None,
        pattern: str | None = None,
    ) -> List[str] | str:

        binary = registry.get_binary(tool_name)
        tool = registry.get_tool(tool_name)

        script_path = tool.get("script_path")


        if tool_name == "subscraper" and script_path:
            return [
                sys.executable,
                str(PROJECT_ROOT / script_path),
                "-d",
                target or "",
            ]

        github_token = os.getenv("GITHUB_TOKEN", "").strip()

        commands: Dict[str, List[str] | str] = {

            "subfinder": [
                binary,
                "-d",
                target or "",
                "-silent",
            ],

            "assetfinder": [
                binary,
                "--subs-only",
                target or "",
            ],

            "amass": [
                binary,
                "enum",
                "-passive",
                "-d",
                target or "",
            ],

            "findomain": [
                binary,
                "-t",
                target or "",
                "-q",
            ],

            # github-subdomains NEEDS TOKEN
            "github-subdomains": (
                [
                    binary,
                    "-d",
                    target or "",
                    "-t",
                    github_token,
                    "-q",
                ]
                if github_token
                else (
                    ["cmd", "/c", "echo"]
                    if os.name == "nt"
                    else ["sh", "-c", "echo"]
                )
            ),


            "httpx": [
                self._resolve_httpx_binary(),
                "-l",
                input_file or "",
                "-silent",
                "-follow-redirects",
                "-status-code",
                "-threads",
                "100",
            ],

            "gau": [
                binary,
                target or "",
            ],

            "waybackurls": (
                f'echo "{target or ""}" | {binary}'
            ),

            "katana": [
                binary,
                "-u",
                target or "",
                "-silent",
                "-jc",
            ],
            "paramspider": [
                binary,
                "-d",
                target or "",
            ],

            "arjun": [
                binary,
                "-u",
                target or "",
                "--passive",
            ],


            "gf": [],

            "ffuf": [
                binary,
                "-u",
                f"{target.rstrip('/')}/FUZZ" if target else "",
                "-w",
                wordlist or "wordlists/directories",
                "-mc",
                "200,204,301,302,307,401,403",
                "-s",
            ],

            "dirsearch": [
                binary,
                "-u",
                target or "",
                "--quiet",
            ],
        }

        if tool_name == "gf":

            if not pattern or not input_file:
                raise ValueError(
                    "gf requires pattern and input_file"
                )

            if output_file:

                if os.name == "nt":
                    return (
                        f'type "{input_file}" | '
                        f'{binary} {pattern} > "{output_file}"'
                    )

                return (
                    f'cat "{input_file}" | '
                    f'{binary} {pattern} > "{output_file}"'
                )

            if os.name == "nt":
                return (
                    f'type "{input_file}" | '
                    f'{binary} {pattern}'
                )

            return (
                f'cat "{input_file}" | '
                f'{binary} {pattern}'
            )

        if tool_name not in commands:
            raise ValueError(
                f"Unsupported tool: {tool_name}"
            )

        return commands[tool_name]


    async def execute(
        self,
        command: List[str],
        tool_name: str,
        timeout: Optional[int] = None,
        cwd: str | None = None,
    ) -> Dict[str, Any]:

        start_time = time.time()

        if timeout is None:
            timeout = registry.get_timeout(tool_name)

        command_text = " ".join(command)

        try:

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            self.processes.append(process)

            try:

                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )

            except asyncio.TimeoutError:

                try:
                    process.kill()
                    await process.wait()
                except Exception:
                    pass

                return {
                    "tool": tool_name,
                    "command": command_text,
                    "success": False,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": "Timeout reached",
                    "duration": round(
                        time.time() - start_time,
                        2,
                    ),
                }

            stdout_text = stdout.decode(errors="ignore")
            stderr_text = stderr.decode(errors="ignore")

            return {
                "tool": tool_name,
                "command": command_text,
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "duration": round(
                    time.time() - start_time,
                    2,
                ),
            }

        except Exception as e:

            return {
                "tool": tool_name,
                "command": command_text,
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "duration": round(
                    time.time() - start_time,
                    2,
                ),
            }

    async def execute_shell(
        self,
        command: str,
        tool_name: str,
        timeout: Optional[int] = None,
        cwd: str | None = None,
    ) -> Dict[str, Any]:

        start_time = time.time()

        if timeout is None:
            timeout = registry.get_timeout(tool_name)

        try:

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            self.processes.append(process)

            try:

                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )

            except asyncio.TimeoutError:

                try:
                    process.kill()
                    await process.wait()
                except Exception:
                    pass

                return {
                    "tool": tool_name,
                    "command": command,
                    "success": False,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": "Timeout reached",
                    "duration": round(
                        time.time() - start_time,
                        2,
                    ),
                }

            return {
                "tool": tool_name,
                "command": command,
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": stdout.decode(errors="ignore"),
                "stderr": stderr.decode(errors="ignore"),
                "duration": round(
                    time.time() - start_time,
                    2,
                ),
            }

        except Exception as e:

            return {
                "tool": tool_name,
                "command": command,
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "duration": round(
                    time.time() - start_time,
                    2,
                ),
            }

    async def run_tool(
        self,
        tool_name: str,
        target: str | None = None,
        input_file: str | None = None,
        output_file: str | None = None,
        wordlist: str | None = None,
        pattern: str | None = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = None,
        cwd: str | None = None,
    ) -> Dict[str, Any]:

        if not registry.tool_exists(tool_name):

            return {
                "tool": tool_name,
                "success": False,
                "stdout": "",
                "stderr": "Tool not registered",
                "returncode": -1,
                "duration": 0,
            }

        if not self.is_tool_installed(tool_name):

            return {
                "tool": tool_name,
                "success": False,
                "stdout": "",
                "stderr": "Tool not installed",
                "returncode": -1,
                "duration": 0,
            }

        if retries is None:
            retries = registry.get_tool(tool_name).get(
                "retries",
                1,
            )

        command = self.build_command(
            tool_name=tool_name,
            target=target,
            input_file=input_file,
            output_file=output_file,
            wordlist=wordlist,
            pattern=pattern,
        )

        final_result: Dict[str, Any] = {
            "tool": tool_name,
            "success": False,
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "duration": 0,
        }

        for attempt in range(retries + 1):

            self.logger.info(
                f"Running {tool_name} | Attempt {attempt + 1}"
            )

            if isinstance(command, str):

                result = await self.execute_shell(
                    command=command,
                    tool_name=tool_name,
                    timeout=timeout,
                    cwd=cwd,
                )

            else:

                result = await self.execute(
                    command=command,
                    tool_name=tool_name,
                    timeout=timeout,
                    cwd=cwd,
                )

            final_result = result

            if result.get("success"):

                self.logger.success(
                    f"{tool_name} completed in "
                    f"{result.get('duration')}s"
                )

                break

            self.logger.warning(
                f"{tool_name} failed: "
                f"{result.get('stderr')}"
            )

        if output_file and tool_name != "gf":
            self.save_output(
                output_file,
                final_result.get("stdout", ""),
            )

        return final_result


    async def run_many(
        self,
        tool_names: List[str],
        target: str | None = None,
        input_file: str | None = None,
        output_dir: str | Path | None = None,
        wordlist: str | None = None,
    ) -> Dict[str, Dict[str, Any]]:

        results: Dict[str, Dict[str, Any]] = {}

        for tool_name in tool_names:

            output_file = None

            if output_dir:
                output_file = str(
                    Path(output_dir) / f"{tool_name}.txt"
                )

            result = await self.run_tool(
                tool_name=tool_name,
                target=target,
                input_file=input_file,
                output_file=output_file,
                wordlist=wordlist,
            )

            results[tool_name] = result

        return results

    def save_output(
        self,
        output_file: str | Path,
        content: str,
    ) -> Path:

        path = Path(output_file)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
            errors="ignore",
        )

        return path

    async def kill_all(self) -> None:

        for process in self.processes:

            try:
                if process.returncode is None:
                    process.kill()
                    await process.wait()

            except Exception:
                pass

        self.processes.clear()


executor = Executor()