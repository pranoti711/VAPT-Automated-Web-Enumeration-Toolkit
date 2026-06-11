

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def readable_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =========================================
# PATH HELPERS
# =========================================

def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent(file_path: str | Path) -> Path:
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def file_exists(path: str | Path) -> bool:
    return Path(path).exists()


# =========================================
# FILE HELPERS
# =========================================

def read_lines(file_path: str | Path) -> list[str]:
    path = Path(file_path)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [
            line.strip()
            for line in f
            if line.strip()
        ]


def write_lines(file_path: str | Path, lines: Iterable[Any]) -> Path:
    path = ensure_parent(file_path)

    cleaned = [
        str(item).strip()
        for item in lines
        if str(item).strip()
    ]

    path.write_text(
        "\n".join(cleaned),
        encoding="utf-8",
        errors="ignore",
    )

    return path


def append_line(file_path: str | Path, line: Any) -> Path:
    path = ensure_parent(file_path)

    with open(path, "a", encoding="utf-8", errors="ignore") as f:
        f.write(str(line) + "\n")

    return path


def read_text(file_path: str | Path) -> str:
    path = Path(file_path)

    if not path.exists():
        return ""

    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def write_text(file_path: str | Path, content: Any) -> Path:
    path = ensure_parent(file_path)

    path.write_text(
        str(content),
        encoding="utf-8",
        errors="ignore",
    )

    return path


# =========================================
# JSON HELPERS
# =========================================

def read_json(file_path: str | Path) -> dict:
    path = Path(file_path)

    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


def write_json(file_path: str | Path, data: dict) -> Path:
    path = ensure_parent(file_path)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )

    return path


# =========================================
# CLEANING HELPERS
# =========================================

def clean_domain(domain: str) -> str:
    domain = (domain or "").strip().lower()

    domain = re.sub(
        r"^https?://",
        "",
        domain,
        flags=re.IGNORECASE,
    )

    domain = domain.split("/")[0]
    domain = domain.strip(".")

    return domain


def is_valid_domain(domain: str) -> bool:
    domain = clean_domain(domain)

    pattern = re.compile(
        r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    )

    return bool(pattern.match(domain))


def normalize_url(url: str) -> str | None:
    try:
        url = (url or "").strip()

        if not url or " " in url:
            return None

        url = url.replace("\\", "/")

        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return None

        if not parsed.netloc:
            return None

        path = re.sub(r"/+", "/", parsed.path).rstrip("/")

        final = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"

        if parsed.query:
            final += f"?{parsed.query}"

        return final

    except Exception:
        return None


def unique(items: Iterable[Any]) -> list[str]:
    return sorted(
        set(
            str(item).strip()
            for item in items
            if str(item).strip()
        )
    )


def chunk_list(data: list[Any], size: int = 100) -> list[list[Any]]:
    if size <= 0:
        size = 100

    return [
        data[i:i + size]
        for i in range(0, len(data), size)
    ]


# =========================================
# TOOL HELPERS
# =========================================

def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def sanitize_filename(name: str) -> str:
    name = (name or "").strip()

    name = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        name,
    )

    return name or "file"


# =========================================
# TARGET HELPERS
# =========================================

def target_to_url(target: str) -> str:
    target = target.strip()

    if target.startswith("http://") or target.startswith("https://"):
        return target.rstrip("/")

    return f"https://{target.rstrip('/')}"


def extract_hostname(url: str) -> str:
    try:
        parsed = urlparse(url)

        if parsed.netloc:
            return parsed.netloc.lower()

        return clean_domain(url)

    except Exception:
        return clean_domain(url)