
from __future__ import annotations

import re
from urllib.parse import (
    urlparse,
    parse_qsl,
    urlencode,
    urlunparse,
)

from typing import Any, Dict, List

class ResultDeduplicator:
    """
    Advanced result deduplication engine.

    Responsibilities:
    -----------------
    - Deduplicate subdomains
    - Deduplicate URLs
    - Normalize URLs
    - Normalize query parameters
    - Deduplicate parameters
    - Deduplicate directories
    - Deduplicate nuclei/tool findings
    - Remove empty/junk values
    """

    def __init__(self):

        self.static_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".css",
            ".ico",
            ".woff",
            ".woff2",
            ".ttf",
            ".eot",
            ".otf",
            ".mp4",
            ".mp3",
            ".avi",
            ".mov",
            ".webm",
            ".pdf",
            ".zip",
            ".rar",
            ".7z",
        }

    def clean_string(
        self,
        value: Any,
    ) -> str:

        return str(value).strip()

    def dedupe_list(
        self,
        items: List[Any],
    ) -> List[str]:

        cleaned = set()

        for item in items:

            value = self.clean_string(item)

            if value:
                cleaned.add(value)

        return sorted(cleaned)

    def normalize_subdomain(
        self,
        subdomain: str,
    ) -> str | None:

        subdomain = self.clean_string(subdomain).lower()

        if not subdomain:
            return None

        subdomain = re.sub(
            r"^https?://",
            "",
            subdomain,
            flags=re.IGNORECASE,
        )

        subdomain = subdomain.split("/")[0]

        subdomain = subdomain.strip(".")

        if not subdomain:
            return None

        return subdomain


    def dedupe_subdomains(
        self,
        subdomains: List[str],
    ) -> List[str]:

        results = set()

        for subdomain in subdomains:

            normalized = self.normalize_subdomain(subdomain)

            if normalized:
                results.add(normalized)

        return sorted(results)

    def normalize_url(
        self,
        url: str,
        sort_query: bool = True,
        remove_fragment: bool = True,
    ) -> str | None:

        try:

            url = self.clean_string(url)

            if not url:
                return None

            if " " in url:
                return None

            url = url.replace("\\", "/")

            parsed = urlparse(url)

            if parsed.scheme not in {
                "http",
                "https",
            }:
                return None

            if not parsed.netloc:
                return None

            scheme = parsed.scheme.lower()
            netloc = parsed.netloc.lower()
            path = re.sub(r"/+", "/", parsed.path).rstrip("/")

            query = parsed.query

            if sort_query and query:

                query = urlencode(
                    sorted(parse_qsl(query, keep_blank_values=True))
                )

            fragment = "" if remove_fragment else parsed.fragment

            normalized = urlunparse(
                (
                    scheme,
                    netloc,
                    path,
                    "",
                    query,
                    fragment,
                )
            )

            return normalized

        except Exception:
            return None

    def is_static_url(
        self,
        url: str,
    ) -> bool:

        try:

            parsed = urlparse(url)

            path = parsed.path.lower()

            return any(
                path.endswith(ext)
                for ext in self.static_extensions
            )

        except Exception:
            return False

    def dedupe_urls(
        self,
        urls: List[str],
        remove_static: bool = False,
    ) -> List[str]:

        results = set()

        for url in urls:

            normalized = self.normalize_url(url)

            if not normalized:
                continue

            if remove_static and self.is_static_url(normalized):
                continue

            results.add(normalized)

        return sorted(results)

    def dedupe_parameters(
        self,
        parameters: List[str],
    ) -> List[str]:

        results = set()

        for param in parameters:

            param = self.clean_string(param)

            if not param:
                continue

            if len(param) < 2:
                continue

            if " " in param:
                continue

            results.add(param)

        return sorted(results)

    def dedupe_directories(
        self,
        directories: List[str],
    ) -> List[str]:

        results = set()

        for item in directories:

            value = self.clean_string(item)

            if not value:
                continue

            if value.startswith("http://") or value.startswith("https://"):

                normalized = self.normalize_url(value)

                if normalized:
                    results.add(normalized)

            else:

                if not value.startswith("/"):
                    value = "/" + value

                value = re.sub(r"/+", "/", value).rstrip("/")

                if value:
                    results.add(value)

        return sorted(results)

    def dedupe_findings(
        self,
        findings: List[Dict[str, Any]],
        key_fields: List[str] | None = None,
    ) -> List[Dict[str, Any]]:

        if key_fields is None:

            key_fields = [
                "severity",
                "template",
                "target",
            ]

        seen = set()

        results: List[Dict[str, Any]] = []

        for finding in findings:

            try:

                key = tuple(
                    str(finding.get(field, "")).strip().lower()
                    for field in key_fields
                )

                if key in seen:
                    continue

                seen.add(key)

                results.append(finding)

            except Exception:
                continue

        return results

    def dedupe_parser_output(
        self,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "subdomains": self.dedupe_subdomains(
                data.get("subdomains", [])
            ),
            "urls": self.dedupe_urls(
                data.get("urls", []),
                remove_static=True,
            ),
            "parameters": self.dedupe_parameters(
                data.get("parameters", [])
            ),
            "directories": self.dedupe_directories(
                data.get("directories", [])
            ),
            "js_files": self.dedupe_urls(
                data.get("js_files", []),
                remove_static=False,
            ),
            "emails": self.dedupe_list(
                data.get("emails", [])
            ),
            "technologies": self.dedupe_list(
                data.get("technologies", [])
            ),
            "sensitive_files": self.dedupe_urls(
                data.get("sensitive_files", []),
                remove_static=False,
            ),
            "api_endpoints": self.dedupe_urls(
                data.get("api_endpoints", []),
                remove_static=False,
            ),
            "secrets": data.get("secrets", {}),
        }


    def merge_lists(
        self,
        *lists: List[Any],
    ) -> List[str]:

        merged = []

        for item_list in lists:

            merged.extend(item_list)

        return self.dedupe_list(merged)


    def merge_urls(
        self,
        *url_lists: List[str],
        remove_static: bool = False,
    ) -> List[str]:

        merged = []

        for urls in url_lists:

            merged.extend(urls)

        return self.dedupe_urls(
            merged,
            remove_static=remove_static,
        )

    def merge_subdomains(
        self,
        *subdomain_lists: List[str],
    ) -> List[str]:

        merged = []

        for subdomains in subdomain_lists:

            merged.extend(subdomains)

        return self.dedupe_subdomains(merged)


# =========================================
# GLOBAL INSTANCE
# =========================================

result_deduplicator = ResultDeduplicator()