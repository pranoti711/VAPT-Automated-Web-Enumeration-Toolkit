
from __future__ import annotations

import json
import re
from urllib.parse import urlparse, parse_qs, urlunparse
from typing import List, Dict, Any, Set

from core.logger import Logger


class Parser:
    """
    FINAL ADVANCED RECON PARSER - HYBRID OPTIMIZED
    
    Combines strict formatting/JSONL tracking with O(1) lookups
    and pre-compiled regex loops for multi-megabyte log parsing.
    """

    def __init__(self):
        self.logger = Logger()

        # Compiled Regex Optimizations
        self.url_regex = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
        self.domain_regex = re.compile(r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}\b")
        self.email_regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", re.IGNORECASE)
        self.status_pattern = re.compile(r"\[(\d{3})\]")
        self.path_pattern = re.compile(r"\s(/[^\s]+)")
        self.param_clean_pattern = re.compile(r"[A-Za-z0-9_\-]{2,80}")

        self.garbage_keywords = {
            "", "null", "undefined", "[inf]", "[err]", "[dbg]", 
            "[debug]", "error", "warning", "traceback", "false", "true"
        }

        self.static_extensions = {
            ".png", ".jpg", ".jpeg", ".gif", ".svg", ".css", ".ico", 
            ".woff", ".woff2", ".ttf", ".eot", ".otf", ".mp4", ".mp3", 
            ".avi", ".mov", ".webm", ".pdf", ".zip", ".rar", ".7z", 
            ".tar", ".gz", ".docx", ".xlsx", ".webp"
        }

    def clean_lines(self, data: str | List[str]) -> List[str]:
        if isinstance(data, str):
            lines = data.splitlines()
        else:
            lines = data

        cleaned = []
        for line in lines:
            line_str = str(line).strip()
            if not line_str or len(line_str) < 2:
                continue
            if line_str.lower() in self.garbage_keywords:
                continue
            cleaned.append(line_str)
        return cleaned

    def unique(self, data: List[str]) -> List[str]:
        return sorted(set(x.strip() for x in data if x and x.strip()))

    def normalize_url(self, url: str) -> str | None:
        try:
            url = url.strip().strip("\"'<>[](){},")
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return None

            scheme = parsed.scheme.lower()
            netloc = parsed.netloc.lower()
            path = re.sub(r"/+", "/", parsed.path)
            if path != "/":
                path = path.rstrip("/")

            return urlunparse((scheme, netloc, path, "", parsed.query, ""))
        except Exception:
            return None

    def clean_url(self, url: str) -> str | None:
        try:
            url = url.strip().strip("\"'<>[](){},")
            url = url.replace("\\", "/")
            if " " in url:
                return None

            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                return None

            return self.normalize_url(url)
        except Exception:
            return None

    def is_static_file(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            path = parsed.path.lower()
            dot_idx = path.rfind('.')
            if dot_idx != -1:
                return path[dot_idx:] in self.static_extensions
            return False
        except Exception:
            return False

    def filter_scope(self, urls: List[str], domain: str) -> List[str]:
        domain = domain.lower().strip().lstrip(".")
        scoped = []
        for url in urls:
            try:
                parsed = urlparse(url)
                host = parsed.netloc.lower()
                if host == domain or host.endswith("." + domain):
                    scoped.append(url)
            except Exception:
                continue
        return self.unique(scoped)

    def parse_subdomains(self, lines: List[str]) -> List[str]:
        self.logger.info("Parsing subdomains...")
        subdomains = set()
        for line in self.clean_lines(lines):
            matches = self.domain_regex.findall(line)
            for match in matches:
                match = match.lower().strip().strip(".")
                if any(x in match for x in ("@", "*", "_")):
                    continue
                if match.startswith("-") or match.endswith("-"):
                    continue
                subdomains.add(match)
        result = sorted(subdomains)
        self.logger.success(f"Subdomains parsed: {len(result)}")
        return result

    def parse_urls(self, lines: List[str]) -> List[str]:
        self.logger.info("Parsing URLs...")
        urls = set()
        for line in self.clean_lines(lines):
            matches = self.url_regex.findall(line)
            for url in matches:
                cleaned = self.clean_url(url)
                if cleaned:
                    urls.add(cleaned)
        result = sorted(urls)
        self.logger.success(f"URLs parsed: {len(result)}")
        return result

    def parse_httpx(self, lines: List[str]) -> List[str]:
        self.logger.info("Parsing httpx output...")
        urls = set()
        for line in self.clean_lines(lines):
            line = line.strip()
            if not line:
                continue
            if line.startswith("{") and line.endswith("}"):
                try:
                    item = json.loads(line)
                    url = item.get("url") or item.get("input") or item.get("host") or ""
                    if url and not url.startswith(("http://", "https://")):
                        url = "https://" + url
                    cleaned = self.clean_url(url)
                    if cleaned:
                        urls.add(cleaned)
                    continue
                except Exception:
                    pass

            match = self.url_regex.search(line)
            if match:
                cleaned = self.clean_url(match.group(0))
                if cleaned:
                    urls.add(cleaned)
                continue

            if self.domain_regex.fullmatch(line):
                urls.add("https://" + line.lower())

        result = sorted(urls)
        self.logger.success(f"httpx URLs parsed: {len(result)}")
        return result

    def parse_httpx_details(self, lines: List[str]) -> List[Dict[str, Any]]:
        self.logger.info("Parsing httpx details...")
        findings = []
        for line in self.clean_lines(lines):
            try:
                if line.startswith("{") and line.endswith("}"):
                    item = json.loads(line)
                    url = item.get("url") or item.get("input") or ""
                    status = item.get("status_code") or item.get("status") or 0
                    cleaned = self.clean_url(url)
                    if cleaned:
                        findings.append({
                            "url": cleaned,
                            "status": int(status) if status else 0,
                            "raw": line
                        })
                    continue

                url_match = self.url_regex.search(line)
                if not url_match:
                    continue

                url = self.clean_url(url_match.group(0))
                if not url:
                    continue

                status_match = self.status_pattern.search(line)
                status = int(status_match.group(1)) if status_match else 0
                findings.append({"url": url, "status": status, "raw": line})
            except Exception:
                continue
        self.logger.success(f"httpx details parsed: {len(findings)}")
        return findings

    def parse_archive_urls(self, lines: List[str]) -> List[str]:
        self.logger.info("Parsing archive URLs...")
        urls = set()
        for line in self.clean_lines(lines):
            if line.startswith("{") and line.endswith("}"):
                try:
                    item = json.loads(line)
                    for value in item.values():
                        if isinstance(value, str):
                            for url in self.url_regex.findall(value):
                                cleaned = self.clean_url(url)
                                if cleaned:
                                    urls.add(cleaned)
                    continue
                except Exception:
                    pass

            matches = self.url_regex.findall(line)
            for url in matches:
                cleaned = self.clean_url(url)
                if cleaned:
                    urls.add(cleaned)
        return sorted(urls)

    def parse_parameters(self, urls: List[str]) -> List[str]:
        self.logger.info("Parsing parameters...")
        parameters = set()
        for item in self.clean_lines(urls):
            try:
                if "=" not in item and "?" not in item:
                    if self.param_clean_pattern.fullmatch(item):
                        parameters.add(item)
                    continue

                urls_found = self.url_regex.findall(item)
                if urls_found:
                    for url in urls_found:
                        parsed = urlparse(url)
                        query = parse_qs(parsed.query, keep_blank_values=True)
                        for param in query.keys():
                            param = param.strip()
                            if len(param) >= 2:
                                parameters.add(param)
                    continue

                if "=" in item:
                    query_part = item.split("?", 1)[-1]
                    query = parse_qs(query_part, keep_blank_values=True)
                    for param in query.keys():
                        param = param.strip()
                        if len(param) >= 2:
                            parameters.add(param)
            except Exception:
                continue
        result = sorted(parameters)
        self.logger.success(f"Parameters parsed: {len(result)}")
        return result

    def parse_gf_output(self, lines: List[str]) -> List[str]:
        return self.parse_urls(lines)

    def parse_ffuf(self, lines: List[str], base_url: str) -> List[str]:
        self.logger.info("Parsing ffuf output...")
        findings = set()
        base_url_stripped = base_url.rstrip('/')
        for line in self.clean_lines(lines):
            try:
                if line.startswith("{") and line.endswith("}"):
                    item = json.loads(line)
                    url = item.get("url") or item.get("input") or ""
                    cleaned = self.clean_url(url)
                    if cleaned:
                        findings.add(cleaned)
                    continue

                if "[Status:" in line:
                    path = line.split("[Status:", 1)[0].strip()
                    if path:
                        full_url = f"{base_url_stripped}/{path.lstrip('/')}"
                        cleaned = self.clean_url(full_url)
                        if cleaned:
                            findings.add(cleaned)
                    continue

                for url in self.url_regex.findall(line):
                    cleaned = self.clean_url(url)
                    if cleaned:
                        findings.add(cleaned)
            except Exception:
                continue
        result = sorted(findings)
        self.logger.success(f"FFUF results parsed: {len(result)}")
        return result

    def parse_dirsearch(self, lines: List[str], base_url: str) -> List[str]:
        self.logger.info("Parsing dirsearch output...")
        findings = set()
        base_url_stripped = base_url.rstrip('/')
        for line in self.clean_lines(lines):
            try:
                urls = self.url_regex.findall(line)
                for url in urls:
                    cleaned = self.clean_url(url)
                    if cleaned:
                        findings.add(cleaned)
                if urls:
                    continue

                path_match = self.path_pattern.search(line)
                if not path_match:
                    continue

                path = path_match.group(1)
                full_url = f"{base_url_stripped}{path}"
                cleaned = self.clean_url(full_url)
                if cleaned:
                    findings.add(cleaned)
            except Exception:
                continue
        result = sorted(findings)
        self.logger.success(f"Dirsearch results parsed: {len(result)}")
        return result

    def extract_directories(self, urls: List[str]) -> List[str]:
        directories = set()
        for url in urls:
            try:
                parsed = urlparse(url)
                path = parsed.path.strip()
                if path and path != "/":
                    directories.add(path.rstrip("/"))
            except Exception:
                continue
        return sorted(directories)

    def extract_js_files(self, urls: List[str]) -> List[str]:
        js_files = set()
        for url in urls:
            try:
                parsed = urlparse(url)
                if parsed.path.lower().endswith(".js"):
                    js_files.add(url)
            except Exception:
                continue
        return sorted(js_files)

    def extract_emails(self, lines: List[str]) -> List[str]:
        emails = set()
        for line in self.clean_lines(lines):
            matches = self.email_regex.findall(line)
            for email in matches:
                emails.add(email.lower())
        return sorted(emails)

    def extract_technologies(self, lines: List[str]) -> List[str]:
        known = {
            "wordpress", "drupal", "laravel", "django", "apache", 
            "nginx", "react", "vue", "jquery", "bootstrap", 
            "nextjs", "express", "cloudflare"
        }
        detected = set()
        for line in self.clean_lines(lines):
            lower = line.lower()
            for tech in known:
                if tech in lower:
                    detected.add(tech)
        return sorted(detected)

    def extract_secrets(self, lines: List[str]) -> Dict[str, List[str]]:
        patterns = {
            "aws_keys": r"AKIA[0-9A-Z]{16}",
            "google_api": r"AIza[0-9A-Za-z\-_]{35}",
            "github_token": r"github_pat_[A-Za-z0-9_]+",
            "slack_token": r"xox[baprs]-[A-Za-z0-9-]+",
            "jwt_token": r"eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",
            "stripe_live": r"sk_live_[0-9a-zA-Z]{24}",
            "private_key": r"-----BEGIN PRIVATE KEY-----",
            "firebase": r"AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}",
            "discord_token": r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}",
            "twilio": r"SK[0-9a-fA-F]{32}",
            "shopify": r"shpss_[a-fA-F0-9]{32}",
        }
        findings: Dict[str, List[str]] = {}
        for secret_type, pattern in patterns.items():
            matches = set()
            regex = re.compile(pattern)
            for line in self.clean_lines(lines):
                found = regex.findall(line)
                for item in found:
                    matches.add(item)
            findings[secret_type] = sorted(matches)
        return findings

    def extract_sensitive_files(self, urls: List[str]) -> List[str]:
        sensitive = set()
        keywords = {
            ".env", ".git", "config", "backup", "db", "sql", 
            ".bak", ".old", ".zip", ".tar", ".gz", "admin", "phpinfo"
        }
        for url in urls:
            lower = url.lower()
            if any(key in lower for key in keywords):
                sensitive.add(url)
        return sorted(sensitive)

    def extract_api_endpoints(self, urls: List[str]) -> List[str]:
        api_urls = set()
        keywords = {"/api/", "/graphql", "/v1/", "/v2/", "/rest/", "/swagger"}
        for url in urls:
            lower = url.lower()
            if any(key in lower for key in keywords):
                api_urls.add(url)
        return sorted(api_urls)

    def filter_static_urls(self, urls: List[str]) -> List[str]:
        filtered = [url for url in urls if not self.is_static_file(url)]
        return sorted(set(filtered))

    def parse_all(self, raw_data: str | List[str]) -> Dict[str, Any]:
        self.logger.info("Running FULL Parser Engine...")
        lines = self.clean_lines(raw_data)
        subdomains = self.parse_subdomains(lines)
        urls = self.parse_urls(lines)
        urls = self.filter_static_urls(urls)

        result = {
            "subdomains": subdomains,
            "urls": urls,
            "parameters": self.parse_parameters(urls),
            "directories": self.extract_directories(urls),
            "js_files": self.extract_js_files(urls),
            "emails": self.extract_emails(lines),
            "technologies": self.extract_technologies(lines),
            "secrets": self.extract_secrets(lines),
            "sensitive_files": self.extract_sensitive_files(urls),
            "api_endpoints": self.extract_api_endpoints(urls),
        }
        self.logger.success("FULL parsing completed")
        return result


parser = Parser()

def parse_lines(data): return parser.clean_lines(data)
def parse_urls(data): return parser.parse_urls(parser.clean_lines(data))
def parse_subdomains(data): return parser.parse_subdomains(parser.clean_lines(data))
def parse_parameters(data): return parser.parse_parameters(parser.parse_urls(parser.clean_lines(data)))