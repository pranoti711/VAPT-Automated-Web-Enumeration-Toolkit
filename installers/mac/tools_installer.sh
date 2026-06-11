#!/bin/bash

# =========================================
# PRO RECON ENGINE - macOS TOOL INSTALLER
# =========================================

set -euo pipefail

echo "======================================"
echo "[TOOLS INSTALLER] macOS Recon Stack"
echo "======================================"
echo ""

# =========================
# PATH SETUP
# =========================
GO_BIN="$HOME/go/bin"
export PATH="$PATH:$GO_BIN"

TOOLS_DIR="$HOME/vapt-tools"
mkdir -p "$TOOLS_DIR"

# =========================
# CHECK DEPENDENCIES
# =========================
command -v go >/dev/null 2>&1 || {
    echo "[ERROR] Go not installed"
    exit 1
}

command -v python3 >/dev/null 2>&1 || {
    echo "[ERROR] Python3 not installed"
    exit 1
}

echo "[OK] Go & Python detected"
echo ""

# =========================
# GO TOOLS (13-14 CORE RECON TOOLS)
# =========================

GO_TOOLS=(
"github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
"github.com/projectdiscovery/httpx/cmd/httpx@latest"
"github.com/projectdiscovery/katana/cmd/katana@latest"
"github.com/lc/gau/v2/cmd/gau@latest"
"github.com/tomnomnom/waybackurls@latest"
"github.com/tomnomnom/assetfinder@latest"
"github.com/hakluke/hakrawler@latest"
"github.com/tomnomnom/gf@latest"
"github.com/ffuf/ffuf/v2@latest"
"github.com/owasp-amass/amass/v4/...@master"
"github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
"github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
"github.com/tomnomnom/qsreplace@latest"
"github.com/tomnomnom/unfurl@latest"
)

echo "======================================"
echo "[GO TOOLS INSTALLATION]"
echo "======================================"
echo ""

install_go_tool() {
    tool=$1

    echo "[INSTALLING] $tool"

    if go install "$tool" >/dev/null 2>&1; then
        echo "[OK] Installed"
    else
        echo "[WARN] Failed: $tool"
    fi

    echo ""
}

for tool in "${GO_TOOLS[@]}"; do
    install_go_tool "$tool"
done

# =========================
# PYTHON TOOLS
# =========================

echo "======================================"
echo "[PYTHON TOOLS INSTALLATION]"
echo "======================================"
echo ""

PY_TOOLS=(
arjun
uro
wafw00f
paramspider
subscraper
)

for tool in "${PY_TOOLS[@]}"; do
    echo "[INSTALLING] $tool"

    if python3 -m pip install "$tool" >/dev/null 2>&1; then
        echo "[OK] Installed"
    else
        echo "[WARN] Failed: $tool"
    fi

    echo ""
done

# =========================
# GITHUB / MANUAL TOOLS
# =========================

echo "======================================"
echo "[GITHUB TOOLS]"
echo "======================================"
echo ""

# DIRSEARCH
if [ ! -d "$TOOLS_DIR/dirsearch" ]; then
    git clone https://github.com/maurosoria/dirsearch.git "$TOOLS_DIR/dirsearch"
    echo "[OK] dirsearch installed"
else
    echo "[WARN] dirsearch already exists"
fi

echo ""

# SQLMAP
if [ ! -d "$TOOLS_DIR/sqlmap" ]; then
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git "$TOOLS_DIR/sqlmap"
    echo "[OK] sqlmap installed"
else
    echo "[WARN] sqlmap already exists"
fi

echo ""

# GF PATTERNS
if [ ! -d "$HOME/.gf" ]; then
    git clone https://github.com/1ndianl33t/Gf-Patterns.git "$HOME/.gf"
    echo "[OK] gf patterns installed"
else
    echo "[WARN] gf patterns exist"
fi

echo ""

# =========================
# OPTIONAL BREW TOOLS (MAC ONLY)
# =========================

if command -v brew >/dev/null 2>&1; then
    echo "======================================"
    echo "[BREW TOOLS]"
    echo "======================================"
    echo ""

    brew install feroxbuster findomain || true
else
    echo "[WARN] Homebrew not installed - skipping brew tools"
fi

# =========================
# VERIFY INSTALLATION
# =========================

echo ""
echo "======================================"
echo "[VERIFYING TOOLS]"
echo "======================================"
echo ""

TOOLS_VERIFY=(
subfinder httpx katana gau waybackurls assetfinder
hakrawler gf ffuf amass nuclei dnsx
qsreplace unfurl
arjun uro wafw00f paramspider
)

for t in "${TOOLS_VERIFY[@]}"; do
    if command -v "$t" >/dev/null 2>&1; then
        echo "[OK] $t"
    else
        echo "[MISSING] $t"
    fi
done

echo ""
echo "======================================"
echo "[INSTALLATION COMPLETE]"
echo "======================================"
echo ""

echo "PRO RECON ENGINE READY ON macOS"
echo ""
echo "Next step:"
echo "source ~/.zshrc"
echo ""