

from __future__ import annotations

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict


class CacheManager:
    """
    Cache manager for recon results.

    Responsibilities:
    -----------------
    - Cache tool outputs
    - Avoid duplicate scans
    - Store temporary intelligence
    - Load cached results
    - Expire old cache entries
    - Cache per tool + target
    """

    def __init__(
        self,
        cache_dir: str | Path = "outputs/cache",
        default_ttl_hours: int = 24,
    ):

        self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.default_ttl_hours = default_ttl_hours



    def make_key(
        self,
        *parts: str,
    ) -> str:

        raw = "::".join(
            str(part)
            for part in parts
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()


    def get_cache_path(
        self,
        key: str,
    ) -> Path:

        return self.cache_dir / f"{key}.json"

    def save(
        self,
        key: str,
        data: Any,
        ttl_hours: int | None = None,
    ) -> Path:

        ttl_hours = (
            ttl_hours
            if ttl_hours is not None
            else self.default_ttl_hours
        )

        now = datetime.now()

        payload = {
            "created_at": now.isoformat(),
            "expires_at": (
                now + timedelta(hours=ttl_hours)
            ).isoformat(),
            "ttl_hours": ttl_hours,
            "data": data,
        }

        path = self.get_cache_path(key)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                payload,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return path


    def load(
        self,
        key: str,
    ) -> Any | None:

        path = self.get_cache_path(key)

        if not path.exists():
            return None

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as f:

                payload = json.load(f)

            expires_at = datetime.fromisoformat(
                payload.get("expires_at", "")
            )

            if datetime.now() > expires_at:

                self.delete(key)

                return None

            return payload.get("data")

        except Exception:

            return None



    def exists(
        self,
        key: str,
    ) -> bool:

        return self.load(key) is not None


    def delete(
        self,
        key: str,
    ) -> bool:

        path = self.get_cache_path(key)

        if path.exists():

            try:

                path.unlink()

                return True

            except Exception:

                return False

        return False


    def clear(
        self,
    ) -> None:

        for file in self.cache_dir.glob("*.json"):

            try:

                file.unlink()

            except Exception:

                pass


    def clean_expired(
        self,
    ) -> int:

        removed = 0

        for file in self.cache_dir.glob("*.json"):

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8",
                ) as f:

                    payload = json.load(f)

                expires_at = datetime.fromisoformat(
                    payload.get("expires_at", "")
                )

                if datetime.now() > expires_at:

                    file.unlink()

                    removed += 1

            except Exception:

                try:

                    file.unlink()

                    removed += 1

                except Exception:

                    pass

        return removed

    def make_tool_key(
        self,
        tool_name: str,
        target: str,
        extra: str = "",
    ) -> str:

        return self.make_key(
            "tool",
            tool_name,
            target,
            extra,
        )



    def save_tool_result(
        self,
        tool_name: str,
        target: str,
        data: Any,
        extra: str = "",
        ttl_hours: int | None = None,
    ) -> Path:

        key = self.make_tool_key(
            tool_name,
            target,
            extra,
        )

        return self.save(
            key,
            data,
            ttl_hours=ttl_hours,
        )

    def load_tool_result(
        self,
        tool_name: str,
        target: str,
        extra: str = "",
    ) -> Any | None:

        key = self.make_tool_key(
            tool_name,
            target,
            extra,
        )

        return self.load(key)


    def make_scan_key(
        self,
        target: str,
        mode: str = "normal",
    ) -> str:

        return self.make_key(
            "scan",
            target,
            mode,
        )


    def save_scan_result(
        self,
        target: str,
        mode: str,
        data: Any,
        ttl_hours: int | None = None,
    ) -> Path:

        key = self.make_scan_key(
            target,
            mode,
        )

        return self.save(
            key,
            data,
            ttl_hours=ttl_hours,
        )

    def load_scan_result(
        self,
        target: str,
        mode: str = "normal",
    ) -> Any | None:

        key = self.make_scan_key(
            target,
            mode,
        )

        return self.load(key)



    def stats(
        self,
    ) -> Dict[str, int]:

        files = list(
            self.cache_dir.glob("*.json")
        )

        expired_removed = self.clean_expired()

        remaining = list(
            self.cache_dir.glob("*.json")
        )

        return {
            "cache_files_before_cleanup": len(files),
            "expired_removed": expired_removed,
            "cache_files_after_cleanup": len(remaining),
        }



    def list_cache_files(
        self,
    ) -> list[str]:

        return sorted(
            str(file)
            for file in self.cache_dir.glob("*.json")
        )


cache_manager = CacheManager()