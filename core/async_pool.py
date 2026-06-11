

from __future__ import annotations

import asyncio

from typing import (
    Any,
    Awaitable,
    Callable,
)


class AsyncPool:

    """
    Generic Async Worker Pool

    Responsibilities:
    -----------------
    - Concurrency limiting
    - Queue management
    - Batch execution
    - Safe exception handling
    - Task scheduling
    - Parallel recon execution

    Used By:
    --------
    - executor.py
    - tool_executor.py
    - workflow_engine.py
    - recon_engine_async.py
    """

    def __init__(
        self,
        workers: int = 20,
    ):

        self.workers = max(
            1,
            workers,
        )

        self.semaphore = asyncio.Semaphore(
            self.workers
        )

        self.tasks: list[
            tuple[
                str,
                Callable[..., Awaitable[Any]],
                tuple,
                dict,
            ]
        ] = []

  

    def add_task(
        self,
        name: str,
        coroutine: Callable[..., Awaitable[Any]],
        *args,
        **kwargs,
    ) -> None:

        self.tasks.append(
            (
                name,
                coroutine,
                args,
                kwargs,
            )
        )

    # =====================================
    # SAFE RUNNER
    # =====================================

    async def _run_task(
        self,
        name: str,
        coroutine: Callable[..., Awaitable[Any]],
        *args,
        **kwargs,
    ) -> tuple[str, Any]:

        async with self.semaphore:

            try:

                result = await coroutine(
                    *args,
                    **kwargs,
                )

                return (
                    name,
                    result,
                )

            except Exception as e:

                return (
                    name,
                    {
                        "error": str(e),
                    },
                )

    # =====================================
    # RUN ALL TASKS
    # =====================================

    async def run(
        self,
    ) -> dict:

        if not self.tasks:
            return {}

        jobs = []

        for (
            name,
            coroutine,
            args,
            kwargs,
        ) in self.tasks:

            jobs.append(

                self._run_task(
                    name,
                    coroutine,
                    *args,
                    **kwargs,
                )

            )

        results = await asyncio.gather(
            *jobs,
            return_exceptions=False,
        )

        output = {}

        for name, result in results:

            output[name] = result

        return output

    # =====================================
    # CLEAR TASKS
    # =====================================

    def clear(
        self,
    ) -> None:

        self.tasks.clear()

    # =====================================
    # SIZE
    # =====================================

    def size(
        self,
    ) -> int:

        return len(
            self.tasks
        )

    # =====================================
    # IS EMPTY
    # =====================================

    def empty(
        self,
    ) -> bool:

        return (
            len(self.tasks) == 0
        )


# =========================================
# HELPER FUNCTION
# =========================================

async def run_parallel(
    tasks: list[
        tuple[
            str,
            Callable[..., Awaitable[Any]],
            tuple,
            dict,
        ]
    ],
    workers: int = 20,
) -> dict:

    pool = AsyncPool(
        workers=workers
    )

    for (
        name,
        coroutine,
        args,
        kwargs,
    ) in tasks:

        pool.add_task(
            name,
            coroutine,
            *args,
            **kwargs,
        )

    return await pool.run()