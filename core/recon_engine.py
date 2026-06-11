
from __future__ import annotations

from typing import Any, Dict

from core.recon_engine_async import run_scan


class ReconEngine:
    """
    Synchronous wrapper for ReconEngineAsync.
    """

    def __init__(
        self,
        target: str,
        mode: str = "normal",
        verify_tools: bool = True,
    ):
        self.target = target.strip().lower()
        self.mode = mode
        self.verify_tools = verify_tools

    def run(self) -> Dict[str, Any]:
        return run_scan(
            target=self.target,
            mode=self.mode,
            verify_tools=self.verify_tools,
        )


def start_scan(
    target: str,
    mode: str = "normal",
    verify_tools: bool = True,
) -> Dict[str, Any]:

    engine = ReconEngine(
        target=target,
        mode=mode,
        verify_tools=verify_tools,
    )

    return engine.run()