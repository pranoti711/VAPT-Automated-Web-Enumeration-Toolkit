
from __future__ import annotations

import re

from urllib.parse import (
    urlparse,
    parse_qsl,
    urlencode,
    urlunparse,
)

from typing import (
    List,
    Dict,
    Any,
)

from core.logger import Logger
from core.parser import parser


class Validator:

    """
    ENTERPRISE VALIDATOR ENGINE

    Responsibilities:
    -----------------
    - Validate URLs
    - Validate domains
    - Normalize URLs
    - Remove duplicates
    - Remove garbage
    - Filter static files
    - Validate parameters
    - Clean nuclei findings
    - Clean httpx results
    - Clean directory results
    - Filter scope
    - Normalize query strings
    - Remove malformed URLs
    """

    def __init__(self):

        self.logger = Logger()

        self.valid_status_codes = {
            100, 101,
            200, 201, 202, 203, 204,
            300, 301, 302, 303, 304, 307, 308,
            400, 401, 402, 403, 404, 405,
            429,
            500, 501, 502, 503, 504,
        }

        self.valid_severities = {
            "info",
            "low",
            "medium",
            "high",
            "critical",
        }

        self.garbage_keywords = {

            "",
            "null",
            "undefined",
            "[inf]",
            "[err]",
            "[dbg]",
            "[debug]",
            "error",
            "warning",
            "traceback",
            "false",
            "true",

        }


    def remove_duplicates(
        self,
        data: List[str],
    ) -> List[str]:

        return sorted(set(data))

    def validate_domain(
        self,
        domain: str,
    ) -> bool:

        try:

            domain = domain.strip().lower()

            if not domain:
                return False

            if " " in domain:
                return False

            if "*" in domain:
                return False

            if "@" in domain:
                return False

            regex = re.compile(
                r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
            )

            return bool(regex.match(domain))

        except Exception:
            return False

    # =========================================
    # VALIDATE SUBDOMAINS
    # =========================================

    def validate_subdomains(
        self,
        subdomains: List[str],
    ) -> List[str]:

        self.logger.info(
            "Validating subdomains..."
        )

        validated = []

        for subdomain in subdomains:

            if self.validate_domain(subdomain):

                validated.append(
                    subdomain.lower()
                )

        result = self.remove_duplicates(validated)

        self.logger.success(
            f"Valid subdomains: {len(result)}"
        )

        return result



    def normalize_url(
        self,
        url: str,
    ) -> str | None:

        try:

            parsed = urlparse(url)

            scheme = parsed.scheme.lower()

            netloc = parsed.netloc.lower()

            path = re.sub(
                r"/+",
                "/",
                parsed.path,
            )

            # SORT QUERY PARAMETERS
            query = urlencode(
                sorted(parse_qsl(parsed.query))
            )

            normalized = urlunparse(
                (
                    scheme,
                    netloc,
                    path.rstrip("/"),
                    "",
                    query,
                    "",
                )
            )

            return normalized

        except Exception:
            return None

    # =========================================
    # VALIDATE URL
    # =========================================

    def validate_url(
        self,
        url: str,
    ) -> bool:

        try:

            url = url.strip()

            if not url:
                return False

            if " " in url:
                return False

            lower = url.lower()

            if lower in self.garbage_keywords:
                return False

            parsed = urlparse(url)

            if parsed.scheme not in {
                "http",
                "https",
            }:
                return False

            if not parsed.netloc:
                return False

            if "localhost" in parsed.netloc:
                return False

            if parsed.netloc.startswith("127."):
                return False

            return True

        except Exception:
            return False


    def validate_urls(
        self,
        urls: List[str],
    ) -> List[str]:

        self.logger.info(
            "Validating URLs..."
        )

        validated = []

        for url in urls:

            if not self.validate_url(url):
                continue

            normalized = self.normalize_url(url)

            if not normalized:
                continue

            validated.append(normalized)

        result = self.remove_duplicates(validated)

        self.logger.success(
            f"Valid URLs: {len(result)}"
        )

        return result

    def filter_static_urls(
        self,
        urls: List[str],
    ) -> List[str]:

        self.logger.info(
            "Filtering static URLs..."
        )

        filtered = []

        for url in urls:

            if parser.is_static_file(url):
                continue

            filtered.append(url)

        result = self.remove_duplicates(filtered)

        self.logger.success(
            f"Filtered URLs: {len(result)}"
        )

        return result

    def filter_scope(
        self,
        urls: List[str],
        domain: str,
    ) -> List[str]:

        self.logger.info(
            "Filtering scope..."
        )

        scoped = []

        for url in urls:

            try:

                parsed = urlparse(url)

                if domain.lower() in parsed.netloc.lower():

                    scoped.append(url)

            except Exception:
                continue

        result = self.remove_duplicates(scoped)

        self.logger.success(
            f"In-scope URLs: {len(result)}"
        )

        return result


    def validate_parameters(
        self,
        parameters: List[str],
    ) -> List[str]:

        self.logger.info(
            "Validating parameters..."
        )

        validated = []

        for param in parameters:

            try:

                param = param.strip()

                if not param:
                    continue

                if len(param) < 2:
                    continue

                if " " in param:
                    continue

                validated.append(param)

            except Exception:
                continue

        result = self.remove_duplicates(validated)

        self.logger.success(
            f"Valid parameters: {len(result)}"
        )

        return result

    # =========================================
    # CLEAN HTTPX RESULTS
    # =========================================

    def clean_httpx_results(
        self,
        results: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        self.logger.info(
            "Cleaning httpx results..."
        )

        cleaned = []

        seen = set()

        for item in results:

            try:

                url = item.get("url", "")

                status = item.get("status", 0)

                if not self.validate_url(url):
                    continue

                if status not in self.valid_status_codes:
                    continue

                normalized = self.normalize_url(url)

                if normalized in seen:
                    continue

                seen.add(normalized)

                cleaned.append({

                    "url": normalized,
                    "status": status,
                    "raw": item.get("raw", ""),

                })

            except Exception:
                continue

        self.logger.success(
            f"Clean httpx results: {len(cleaned)}"
        )

        return cleaned


    def clean_nuclei_results(
        self,
        findings: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        self.logger.info(
            "Cleaning nuclei findings..."
        )

        cleaned = []

        seen = set()

        for item in findings:

            try:

                severity = (
                    item.get(
                        "severity",
                        "unknown"
                    )
                    .lower()
                    .strip()
                )

                target = item.get(
                    "target",
                    ""
                )

                template = item.get(
                    "template",
                    ""
                )

                if severity not in self.valid_severities:
                    continue

                if not self.validate_url(target):
                    continue

                key = (
                    severity,
                    template,
                    target,
                )

                if key in seen:
                    continue

                seen.add(key)

                cleaned.append({

                    "severity": severity,
                    "template": template,
                    "target": self.normalize_url(target),
                    "raw": item.get("raw", ""),

                })

            except Exception:
                continue

        self.logger.success(
            f"Clean nuclei findings: {len(cleaned)}"
        )

        return cleaned

    # =========================================
    # CLEAN DIRECTORY RESULTS
    # =========================================

    def clean_directory_results(
        self,
        urls: List[str],
    ) -> List[str]:

        self.logger.info(
            "Cleaning directory results..."
        )

        cleaned = []

        for url in urls:

            if not self.validate_url(url):
                continue

            normalized = self.normalize_url(url)

            if not normalized:
                continue

            cleaned.append(normalized)

        result = self.remove_duplicates(cleaned)

        self.logger.success(
            f"Clean directories: {len(result)}"
        )

        return result


    def clean_urls(
        self,
        urls: List[str],
    ) -> List[str]:

        urls = self.validate_urls(urls)

        urls = self.filter_static_urls(urls)

        return urls

    # =========================================
    # VALIDATE PARSER OUTPUT
    # =========================================

    def validate_parser_output(
        self,
        parsed_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        self.logger.info(
            "Validating parser output..."
        )

        validated = {

            "subdomains":
                self.validate_subdomains(
                    parsed_data.get(
                        "subdomains",
                        [],
                    )
                ),

            "urls":
                self.clean_urls(
                    parsed_data.get(
                        "urls",
                        [],
                    )
                ),

            "parameters":
                self.validate_parameters(
                    parsed_data.get(
                        "parameters",
                        [],
                    )
                ),

            "directories":
                self.clean_directory_results(
                    parsed_data.get(
                        "directories",
                        [],
                    )
                ),

            "js_files":
                self.validate_urls(
                    parsed_data.get(
                        "js_files",
                        [],
                    )
                ),

            "emails":
                self.remove_duplicates(
                    parsed_data.get(
                        "emails",
                        [],
                    )
                ),

            "technologies":
                self.remove_duplicates(
                    parsed_data.get(
                        "technologies",
                        [],
                    )
                ),

            "sensitive_files":
                self.validate_urls(
                    parsed_data.get(
                        "sensitive_files",
                        [],
                    )
                ),

            "api_endpoints":
                self.validate_urls(
                    parsed_data.get(
                        "api_endpoints",
                        [],
                    )
                ),

            "secrets":
                parsed_data.get(
                    "secrets",
                    {},
                ),

        }

        self.logger.success(
            "Parser output validated"
        )

        return validated


# =========================================
# GLOBAL INSTANCE
# =========================================

validator = Validator()


# =========================================
# HELPER FUNCTIONS
# =========================================

def validate_urls(urls):

    return validator.validate_urls(urls)


def validate_subdomains(subdomains):

    return validator.validate_subdomains(
        subdomains
    )


def clean_urls(urls):

    return validator.clean_urls(urls)


def clean_nuclei_results(results):

    return validator.clean_nuclei_results(
        results
    )