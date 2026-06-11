

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.dependency_checker import DependencyChecker
from core.environment import (
    set_environment,
    setup_environment,
    show_environment,
)
from core.live_monitor import (
    banner,
    error,
    info,
    phase,
    progress_bar,
    success,
    warning,
)
from core.os_detector import show_system_info
from core.recon_engine import start_scan
from core.tool_installer import ToolInstaller


SUBDOMAIN_TOOLS = [
    "subfinder",
    "assetfinder",
    "amass",
    "findomain",
    "github-subdomains",
    "subscraper",
]

HTTP_TOOLS = ["httpx"]

URL_ENUM_TOOLS = [
    "gau",
    "waybackurls",
    "katana",
    "paramspider",
    "arjun",
    "gf",
]

DIRECTORY_TOOLS = [
    "ffuf",
    "dirsearch",
]


ALL_TOOLS = SUBDOMAIN_TOOLS + HTTP_TOOLS + URL_ENUM_TOOLS + DIRECTORY_TOOLS


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def valid_domain(domain: str) -> bool:
    """Validate that input is a domain like example.com or google.com."""

    domain = (domain or "").strip().lower()
    if not domain:
        return False

    # Reject obvious non-domain inputs
    if " " in domain or "*" in domain or "@" in domain:
        return False

    # If user pasted a full URL, extract hostname
    if "://" in domain:
        try:
            from urllib.parse import urlparse

            host = urlparse(domain).hostname or ""
            domain = host.lower()
        except Exception:
            return False

    # If user pasted scheme-less host like www.google.com/path, strip path
    domain = domain.split("/", 1)[0]
    if not domain:
        return False

    pattern = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))


def ask_os() -> str:
    print(
        """
==================================================
SELECT OPERATING SYSTEM
==================================================

1. Windows
2. Linux
3. macOS
4. Auto Detect
"""
    )

    choice = input("Choice: ").strip()

    if choice == "1":
        return "windows"
    if choice == "2":
        return "linux"
    if choice == "3":
        return "macos"

    return "auto"


def print_tool_summary() -> None:
    print(
        f"""
==================================================
TOOL SUMMARY
==================================================

Total Tools      : {len(ALL_TOOLS)}

Subdomain Tools  : {len(SUBDOMAIN_TOOLS)}
HTTP Tools       : {len(HTTP_TOOLS)}
URL/Param/GF     : {len(URL_ENUM_TOOLS)}
Directory Tools  : {len(DIRECTORY_TOOLS)}

Tools:
{", ".join(ALL_TOOLS)}
"""
    )


def install_tools_sequential(title: str, tools: List[str]) -> None:
    installer = ToolInstaller()

    phase(title)
    total = len(tools)

    for index, tool in enumerate(tools, start=1):
        info(f"[{index}/{total}] Current tool: {tool}")

        progress_bar(current=index - 1, total=total, prefix=f"Installing {tool}")
        ok = installer.install_tool(tool)
        progress_bar(current=index, total=total, prefix=f"Installing {tool}")

        if ok:
            success(f"{tool} installed/ready")
        else:
            warning(f"{tool} manual install may be required")

        print()

    success(f"{title} completed")


def install_flow() -> None:
    phase("ENVIRONMENT SETUP")

    selected_os = ask_os()

    if selected_os == "auto":
        info("Using auto-detected operating system")
        setup_environment()
    else:
        info(f"Selected OS: {selected_os}")
        set_environment(selected_os)

    show_system_info()
    show_environment()
    print_tool_summary()

    print(
        """
==================================================
TOOL INSTALLATION SEQUENCE
==================================================

[1] Subdomain Tools
    subfinder → assetfinder → amass → findomain
    → github-subdomains → subscraper

[2] HTTP Probe
    httpx

[3] URL / Parameter / GF Tools
    gau → waybackurls → katana
    → paramspider → arjun → gf

[4] Directory Enumeration Tools
    ffuf → dirsearch → feroxbuster
"""
    )

    confirm = input("Start installation? (y/n): ").strip().lower()

    if confirm != "y":
        warning("Installation cancelled")
        return

    install_tools_sequential("SUBDOMAIN TOOL INSTALLATION", SUBDOMAIN_TOOLS)
    install_tools_sequential("HTTPX TOOL INSTALLATION", HTTP_TOOLS)
    install_tools_sequential(
        "URL / PARAMETER / GF TOOL INSTALLATION",
        URL_ENUM_TOOLS,
    )
    install_tools_sequential("DIRECTORY TOOL INSTALLATION", DIRECTORY_TOOLS)

    success("All installation phases completed")


def check_tools_flow() -> None:
    phase("TOOL DEPENDENCY CHECK")

    checker = DependencyChecker()
    report = checker.check_all()

    installed = report.get("installed", [])
    missing = report.get("missing", [])

    print("\n==========================================")
    print("INSTALLED TOOLS")
    print("==========================================")

    for tool in installed:
        print(f"  ✅ {tool}")
    if not installed:
        print("  None")

    print("\n==========================================")
    print("MISSING TOOLS")
    print("==========================================")

    for tool in missing:
        print(f"  ❌ {tool}")
    if not missing:
        print("  None - All tools ready!")

    if missing:
        warning(f"{len(missing)} tools missing")
    else:
        success("All tools are installed")


def scan_flow(
    domain: Optional[str] = None,
    mode: str = "normal",
    verify_tools: bool = True,
) -> None:
    phase("RECON SCAN SETUP")

    if not domain:
        domain = input("Enter target domain: ").strip()

    if not valid_domain(domain):
        error("Invalid domain format")
        return

    print(
        f"""
==================================================
SCAN WORKFLOW: {domain}
==================================================

[1] Subdomain Enumeration
    subfinder → assetfinder → amass → findomain
    → github-subdomains → subscraper

    Final Output:
    outputs/scans/{domain}/subdomains/final/subdomains.txt

[2] HTTP Alive Check
    httpx

    Final Output:
    outputs/scans/{domain}/httpx/final/alive_hosts.txt

[3] URL / Parameter / GF Enumeration
    gau → waybackurls → katana
    → paramspider → arjun → gf

    URL Output:
    outputs/scans/{domain}/urls/final/urls.txt

    Parameter Output:
    outputs/scans/{domain}/parameters/final/parameters.txt

    GF Output:
    outputs/scans/{domain}/gf_patterns/

[4] Directory Enumeration
    ffuf → dirsearch → feroxbuster

    Final Output:
    outputs/scans/{domain}/directories/final/directories.txt

[5] Reports
    outputs/scans/{domain}/reports/report.json
    outputs/scans/{domain}/reports/summary.txt

==================================================

Mode         : {mode}
Verify Tools : {verify_tools}
"""
    )

    confirm = input("Start scan? (y/n): ").strip().lower()

    if confirm != "y":
        warning("Scan cancelled")
        return

    result = start_scan(target=domain, mode=mode, verify_tools=verify_tools)

    phase("SCAN COMPLETED")

    print("\n==========================================")
    print("SCAN RESULTS")
    print("==========================================")
    print(f"Status       : {result.get('status')}")
    print(f"Target       : {result.get('target')}")
    print(f"Subdomains   : {len(result.get('subdomains', []))}")
    print(f"Alive Hosts  : {len(result.get('alive_hosts', []))}")
    print(f"URLs         : {len(result.get('urls', []))}")
    print(f"Parameters   : {len(result.get('parameters', []))}")
    print(f"GF Groups    : {len(result.get('gf_findings', {}))}")
    print(f"Directories  : {len(result.get('directories', []))}")

    print("\n==========================================")
    print("OUTPUT LOCATIONS")
    print("==========================================")
    print(f"Scan Root     : {PROJECT_ROOT / 'outputs' / 'scans' / domain}")
    print(f"Subdomains    : outputs/scans/{domain}/subdomains/final/subdomains.txt")
    print(f"Alive Hosts   : outputs/scans/{domain}/httpx/final/alive_hosts.txt")
    print(f"URLs          : outputs/scans/{domain}/urls/final/urls.txt")
    print(f"Parameters    : outputs/scans/{domain}/parameters/final/parameters.txt")
    print(f"GF Patterns   : outputs/scans/{domain}/gf_patterns/")
    print(f"Directories   : outputs/scans/{domain}/directories/final/directories.txt")
    print(f"Report        : outputs/scans/{domain}/reports/report.json")

    success("Recon scan finished successfully")


def run_script(script_name: str) -> None:
    script_path = PROJECT_ROOT / "scripts" / script_name

    if not script_path.exists():
        error(f"Script not found: {script_name}")
        return

    subprocess.run([sys.executable, str(script_path)], check=False)


def menu() -> None:
    while True:
        print(
            """
╔════════════════════════════════════════════════════╗
║        VAPT AUTOMATION FRAMEWORK                  ║
║        Cross Platform Recon Engine                ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  1. Install Tools                                  ║
║  2. Check Tools                                    ║
║  3. Run Recon Scan                                 ║
║  4. Clean Outputs                                  ║
║  5. Export Reports                                 ║
║  6. Backup Project / Outputs                       ║
║  7. Update Tools                                   ║
║  8. Show Environment                               ║
║  9. Show System Info                               ║
║ 10. Launch Interactive CLI                         ║
║  0. Exit                                           ║
║                                                    ║
╚════════════════════════════════════════════════════╝
"""
        )

        choice = input("Select option: ").strip()

        if choice == "1":
            install_flow()
        elif choice == "2":
            check_tools_flow()
        elif choice == "3":
            scan_flow()
        elif choice == "4":
            run_script("clean_outputs.py")
        elif choice == "5":
            run_script("export_reports.py")
        elif choice == "6":
            run_script("backup.py")
        elif choice == "7":
            run_script("update_tools.py")
        elif choice == "8":
            show_environment()
        elif choice == "9":
            show_system_info()
        elif choice == "10":
            info("Launching CLI...")
            from core.cli import run_cli

            run_cli()
        elif choice == "0":
            success("Exiting framework")
            break
        else:
            warning("Invalid option")


def parse_args():
    parser = argparse.ArgumentParser(
        description="VAPT Automation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py install
  python main.py check
  python main.py scan -d example.com
  python main.py scan -d example.com -m normal
  python main.py scan -d example.com --skip-tools-check
        """,
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "install",
            "check",
            "scan",
            "clean",
            "export",
            "backup",
            "update",
            "menu",
        ],
        default="menu",
    )

    parser.add_argument(
        "-d",
        "--domain",
        help="Target domain for scan",
    )

    parser.add_argument(
        "-m",
        "--mode",
        default="normal",
        choices=[
            "quick",
            "normal",
            "deep",
            "fast",
            "stealth",
        ],
        help="Scan mode",
    )

    parser.add_argument(
        "--skip-tools-check",
        action="store_true",
        help="Skip tool verification",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    clear_screen()
    banner()
    setup_environment()

    if args.command == "install":
        install_flow()
    elif args.command == "check":
        check_tools_flow()
    elif args.command == "scan":
        scan_flow(
            domain=args.domain,
            mode=args.mode,
            verify_tools=not args.skip_tools_check,
        )
    elif args.command == "clean":
        run_script("clean_outputs.py")
    elif args.command == "export":
        run_script("export_reports.py")
    elif args.command == "backup":
        run_script("backup.py")
    elif args.command == "update":
        run_script("update_tools.py")
    else:
        menu()


if __name__ == "__main__":
    main()

