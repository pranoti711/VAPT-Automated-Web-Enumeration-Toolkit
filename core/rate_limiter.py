
from __future__ import annotations

import asyncio
import random
import time
from collections import defaultdict
from typing import Dict, Optional

class RateLimiter:
    """
    Central async rate limiter.

    Responsibilities:
    -----------------
    - Per-tool delay control
    - Stealth mode support
    - Burst protection
    - Retry backoff
    - Target cooldowns
    - Global concurrency safety

    Used by:
    --------
    - executor.py
    - workflow_engine.py
    - recon_engine_async.py
    """

    def __init__(self):

        self.last_run: Dict[str, float] = defaultdict(float)

        self.target_last_run: Dict[str, float] = defaultdict(float)

        self.lock = asyncio.Lock()

        self.tool_delays = {

            # Subdomain tools
            "subfinder": 0.5,
            "assetfinder": 0.5,
            "amass": 2.0,
            "findomain": 0.5,
            "github-subdomains": 2.0,
            "subscraper": 1.0,

            # HTTP probing
            "httpx": 1.0,

            # URL discovery
            "gau": 1.0,
            "waybackurls": 1.0,
            "katana": 2.0,

            # Parameter discovery
            "paramspider": 2.0,
            "arjun": 3.0,

            # GF
            "gf": 0.2,

            # Directory enumeration
            "ffuf": 3.0,
            "dirsearch": 3.0,
            "feroxbuster": 3.0,
        }

        self.mode_multipliers = {
            "fast": 0.3,
            "normal": 1.0,
            "stealth": 3.0,
        }


    def get_delay(
        self,
        tool_name: str,
        mode: str = "normal",
        jitter: bool = True,
    ) -> float:

        base_delay = self.tool_delays.get(
            tool_name,
            1.0,
        )

        multiplier = self.mode_multipliers.get(
            mode,
            1.0,
        )

        delay = base_delay * multiplier

        if jitter:
            delay += random.uniform(
                0.1,
                0.8,
            )

        return delay

    async def wait(
        self,
        tool_name: str,
        mode: str = "normal",
    ) -> None:

        async with self.lock:

            now = time.time()

            delay = self.get_delay(
                tool_name,
                mode,
            )

            elapsed = now - self.last_run[tool_name]

            if elapsed < delay:

                await asyncio.sleep(
                    delay - elapsed
                )

            self.last_run[tool_name] = time.time()


    async def wait_target(
        self,
        target: str,
        delay: float = 1.0,
    ) -> None:

        async with self.lock:

            now = time.time()

            elapsed = now - self.target_last_run[target]

            if elapsed < delay:

                await asyncio.sleep(
                    delay - elapsed
                )

            self.target_last_run[target] = time.time()

    async def backoff(
        self,
        attempt: int,
        base: float = 2.0,
        maximum: float = 60.0,
        jitter: bool = True,
    ) -> None:

        delay = min(
            base * (2 ** attempt),
            maximum,
        )

        if jitter:
            delay += random.uniform(
                0.5,
                2.0,
            )

        await asyncio.sleep(delay)

    def set_tool_delay(
        self,
        tool_name: str,
        delay: float,
    ) -> None:

        self.tool_delays[tool_name] = delay

    def reset_tool(
        self,
        tool_name: str,
    ) -> None:

        if tool_name in self.last_run:
            del self.last_run[tool_name]


    def reset_all(self) -> None:

        self.last_run.clear()
        self.target_last_run.clear()


    def status(self) -> dict:

        return {
            "tracked_tools": list(self.last_run.keys()),
            "tracked_targets": list(self.target_last_run.keys()),
            "tool_delays": self.tool_delays,
        }

rate_limiter = RateLimiter()