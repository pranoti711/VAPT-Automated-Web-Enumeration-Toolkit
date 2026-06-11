
from __future__ import annotations

from typing import Dict, List


TOOLS: Dict[str, Dict] = {

    "subfinder": {
        "name": "subfinder",
        "category": "subdomain",
        "mode": "passive",
        "binary": "subfinder",
        "threads": 50,
        "timeout": 300,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "subdomains",
        "tags": ["passive", "fast", "subdomain"],
    },

    "assetfinder": {
        "name": "assetfinder",
        "category": "subdomain",
        "mode": "passive",
        "binary": "assetfinder",
        "threads": 30,
        "timeout": 300,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "subdomains",
        "tags": ["passive", "subdomain"],
    },

    "amass": {
        "name": "amass",
        "category": "subdomain",
        "mode": "active",
        "binary": "amass",
        "threads": 50,
        "timeout": 1200,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "subdomains",
        "tags": ["active", "subdomain", "intel"],
    },

    "findomain": {
        "name": "findomain",
        "category": "subdomain",
        "mode": "passive",
        "binary": "findomain",
        "threads": 50,
        "timeout": 300,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "subdomains",
        "tags": ["subdomain", "fast"],
    },

    "github-subdomains": {
        "name": "github-subdomains",
        "category": "subdomain",
        "mode": "passive",
        "binary": "github-subdomains",
        "alternative_binaries": [
            "github-subdomains.exe",
        ],
        "threads": 20,
        "timeout": 600,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "subdomains",
        "tags": ["github", "subdomain", "osint"],
    },

    "subscraper": {
        "name": "subscraper",
        "category": "subdomain",
        "mode": "passive",
        "binary": "python",
        "script_path": "tools/external/subscraper/subscraper.py",
        "threads": 30,
        "timeout": 600,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "subdomains",
        "tags": ["subdomain", "osint"],
    },

    "httpx": {
        "name": "httpx",
        "category": "http_probe",
        "mode": "active",
        "binary": "httpx",
        "threads": 100,
        "timeout": 600,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "urls",
        "tags": ["http", "probe", "alive"],
    },

    "gau": {
        "name": "gau",
        "category": "url_collection",
        "mode": "passive",
        "binary": "gau",
        "threads": 50,
        "timeout": 600,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "urls",
        "tags": ["archive", "urls"],
    },

    "waybackurls": {
        "name": "waybackurls",
        "category": "url_collection",
        "mode": "passive",
        "binary": "waybackurls",
        "threads": 40,
        "timeout": 600,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "urls",
        "tags": ["archive", "wayback", "urls"],
    },

    "katana": {
        "name": "katana",
        "category": "crawler",
        "mode": "active",
        "binary": "katana",
        "threads": 50,
        "timeout": 1200,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "urls",
        "tags": ["crawler", "spider", "javascript"],
    },

    "paramspider": {
        "name": "paramspider",
        "category": "parameter_discovery",
        "mode": "passive",
        "binary": "paramspider",
        "alternative_binaries": [
            "paramspider.exe",
        ],
        "python_modules": [
            "paramspider",
            "ParamSpider",
        ],
        "threads": 20,
        "timeout": 1200,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "parameters",
        "tags": ["parameters", "passive"],
    },

    "arjun": {
        "name": "arjun",
        "category": "parameter_discovery",
        "mode": "active",
        "binary": "arjun",
        "threads": 25,
        "timeout": 1200,
        "retries": 2,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "parameters",
        "tags": ["parameters", "active"],
    },

    "gf": {
        "name": "gf",
        "category": "vulnerability_pattern",
        "mode": "passive",
        "binary": "gf",
        "threads": 10,
        "timeout": 300,
        "retries": 1,
        "enabled": True,
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "patterns",
        "tags": ["gf", "patterns", "filtering"],
    },

    "ffuf": {
        "name": "ffuf",
        "category": "directory_enum",
        "mode": "active",
        "binary": "ffuf",
        "threads": 100,
        "timeout": 1800,
        "retries": 2,
        "enabled": True,
        "wordlist_required": True,
        "default_wordlist": "wordlists/directories",
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "directories",
        "tags": ["fuzzing", "directories", "content_discovery"],
    },

    "dirsearch": {
        "name": "dirsearch",
        "category": "directory_enum",
        "mode": "active",
        "binary": "dirsearch",
        "alternative_binaries": [
            "dirsearch.exe",
        ],
        "python_modules": [
            "dirsearch",
        ],
        "threads": 50,
        "timeout": 1800,
        "retries": 2,
        "enabled": True,
        "wordlist_required": True,
        "default_wordlist": "wordlists/directories",
        "supports": {"linux": True, "windows": True, "macos": True},
        "output_type": "directories",
        "tags": ["directories", "python", "content_discovery"],
    },

    "feroxbuster": {
        "category": "directory_enum",
        "mode": "active",
        "binary": "feroxbuster",
        "alternative_binaries": [
            "feroxbuster.exe",
        ],
        "threads": 100,
        "timeout": 1800,
        "retries": 2,
        "enabled": True,
        "wordlist_required": True,
        "default_wordlist": "wordlists/directories",
        "supports": {"linux": True, "windows": True, "macos": True},
        "windows_requires": [
            "Visual Studio Build Tools",
            "MSVC C++ Compiler",
            "Windows SDK",
        ],
        "output_type": "directories",
        "tags": ["rust", "directories", "recursive"],
    },
}


class ToolRegistry:
    def __init__(self):
        self.tools = TOOLS

    def get_tool(self, name: str) -> Dict:
        return self.tools.get(name, {})

    def tool_exists(self, name: str) -> bool:
        return name in self.tools

    def get_all_tools(self) -> List[str]:
        return list(self.tools.keys())

    def get_tools_by_category(self, category: str) -> List[str]:
        return [
            tool_name
            for tool_name, tool_data in self.tools.items()
            if tool_data.get("category") == category
        ]

    def get_passive_tools(self) -> List[str]:
        return [
            tool_name
            for tool_name, tool_data in self.tools.items()
            if tool_data.get("mode") == "passive"
        ]

    def get_active_tools(self) -> List[str]:
        return [
            tool_name
            for tool_name, tool_data in self.tools.items()
            if tool_data.get("mode") == "active"
        ]

    def get_enabled_tools(self) -> List[str]:
        return [
            tool_name
            for tool_name, tool_data in self.tools.items()
            if tool_data.get("enabled", True)
        ]

    def get_timeout(self, tool_name: str) -> int:
        return self.get_tool(tool_name).get("timeout", 300)

    def get_threads(self, tool_name: str) -> int:
        return self.get_tool(tool_name).get("threads", 10)

    def get_binary(self, tool_name: str) -> str:
        return self.get_tool(tool_name).get("binary", tool_name)

    def get_alternative_binaries(self, tool_name: str) -> List[str]:
        return self.get_tool(tool_name).get("alternative_binaries", [])

    def get_python_modules(self, tool_name: str) -> List[str]:
        return self.get_tool(tool_name).get("python_modules", [])

    def get_script_path(self, tool_name: str) -> str | None:
        return self.get_tool(tool_name).get("script_path")

    def supports_platform(self, tool_name: str, platform_name: str) -> bool:
        return self.get_tool(tool_name).get("supports", {}).get(platform_name, False)

    def requires_wordlist(self, tool_name: str) -> bool:
        return self.get_tool(tool_name).get("wordlist_required", False)

    def get_default_wordlist(self, tool_name: str) -> str | None:
        return self.get_tool(tool_name).get("default_wordlist")

    def get_output_type(self, tool_name: str) -> str:
        return self.get_tool(tool_name).get("output_type", "unknown")


registry = ToolRegistry()
ALL_TOOLS = list(TOOLS.keys())