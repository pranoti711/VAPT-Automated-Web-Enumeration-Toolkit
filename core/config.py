
from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "outputs"

TOOLS_DIR = PROJECT_ROOT / "tools"

WORDLISTS_DIR = PROJECT_ROOT / "wordlists"

REPORTS_DIR = OUTPUT_DIR / "reports"

TEMP_DIR = OUTPUT_DIR / "temp"


FRAMEWORK_NAME = (
    "VAPT Automation Framework"
)

FRAMEWORK_VERSION = "2.0"

AUTHOR = "Pranoti"


DEFAULT_THREADS = 50

DEFAULT_TIMEOUT = 300

MAX_RETRIES = 3

ASYNC_WORKERS = 25

ENABLE_LIVE_MONITOR = True

ENABLE_LOGGING = True

ENABLE_CACHE = False

HTTPX_THREADS = 100

HTTPX_TIMEOUT = 10

HTTPX_RETRIES = 2

KATANA_DEPTH = 3

KATANA_JS_CRAWL = True

KATANA_CONCURRENCY = 20

GAU_THREADS = 10

WAYBACK_THREADS = 10

ARJUN_THREADS = 20

PARAMSPIDER_THREADS = 10

FFUF_THREADS = 50

DIRSEARCH_THREADS = 50

FEROX_THREADS = 50

COMMON_WORDLIST = (
    WORDLISTS_DIR
    / "common.txt"
)

BIG_WORDLIST = (
    WORDLISTS_DIR
    / "big.txt"
)

PARAM_WORDLIST = (
    WORDLISTS_DIR
    / "parameters.txt"
)

SUBDOMAIN_WORDLIST = (
    WORDLISTS_DIR
    / "subdomains.txt"
)

TOOL_TIMEOUTS = {

    "subfinder": 300,

    "assetfinder": 300,

    "amass": 1800,

    "findomain": 300,

    "github-subdomains": 600,

    "subscraper": 600,

    "httpx": 600,

    "gau": 600,

    "waybackurls": 600,

    "katana": 1200,

    "arjun": 1200,

    "paramspider": 1200,

    "gf": 300,

    "ffuf": 1800,

    "dirsearch": 1800,

    "feroxbuster": 1800,
}

PHASE_SUBDOMAINS = "subdomains"

PHASE_HTTPX = "httpx"

PHASE_URLS = "urls"

PHASE_PARAMETERS = "parameters"

PHASE_DIRECTORIES = "directories"

PHASE_GF = "gf"

PHASE_REPORTING = "reporting"

SUBDOMAIN_TOOLS = [

    "subfinder",

    "assetfinder",

    "amass",

    "findomain",

    "github-subdomains",

    "subscraper",
]

URL_TOOLS = [

    "gau",

    "waybackurls",

    "katana",
]

PARAMETER_TOOLS = [

    "arjun",

    "paramspider",
]

DIRECTORY_TOOLS = [

    "ffuf",

    "dirsearch",

    "feroxbuster",
]

GF_PATTERNS = [

    "xss",

    "sqli",

    "ssrf",

    "lfi",

    "redirect",

    "idor",

    "rce",
]

EXPORT_JSON = True

EXPORT_CSV = True

EXPORT_TXT = True

EXPORT_MARKDOWN = True

GENERATE_SUMMARY = True

GENERATE_EXECUTIVE_REPORT = True

GENERATE_TECH_REPORT = True

def get_timeout(
    tool_name: str,
) -> int:

    return TOOL_TIMEOUTS.get(
        tool_name,
        DEFAULT_TIMEOUT,
    )


def get_output_dir() -> Path:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return OUTPUT_DIR