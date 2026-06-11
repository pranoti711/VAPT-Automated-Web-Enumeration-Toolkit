#!/bin/bash

# =========================================
# PRO RECON ENGINE - macOS PYTHON SETUP
# =========================================

set -euo pipefail

echo "======================================"
echo "[PYTHON SETUP] macOS Environment"
echo "======================================"
echo ""

# =========================
# CHECK PYTHON
# =========================
if command -v python3 >/dev/null 2>&1; then
    echo "[OK] Python already installed"
    python3 --version
else
    echo "[INFO] Installing Python via Homebrew..."
    brew install python
fi

# =========================
# VERIFY PIP
# =========================
echo "[INFO] Checking pip..."

if ! python3 -m pip --version >/dev/null 2>&1; then
    echo "[INFO] Bootstrapping pip..."
    python3 -m ensurepip --upgrade || true
fi

# =========================
# UPGRADE PIP CORE
# =========================
echo "[INFO] Upgrading pip..."
python3 -m pip install --upgrade pip setuptools wheel

# =========================
# CORE RECON PYTHON PACKAGES
# =========================
echo ""
echo "[INFO] Installing core Python libraries..."

CORE_PACKAGES=(
    requests
    urllib3
    beautifulsoup4
    lxml
    aiohttp
    colorama
    tqdm
    dnspython
    rich
)

for pkg in "${CORE_PACKAGES[@]}"; do
    echo "[PY] Installing $pkg"
    python3 -m pip install "$pkg" || echo "[WARN] Failed: $pkg"
done

# =========================
# RECON SECURITY TOOLS
# =========================
echo ""
echo "[INFO] Installing recon Python tools..."

RECON_TOOLS=(
    arjun
    uro
    wafw00f
    paramspider
    subscraper
)

for tool in "${RECON_TOOLS[@]}"; do
    echo "[TOOL] Installing $tool"
    python3 -m pip install "$tool" || echo "[WARN] Failed: $tool"
done

# =========================
# SPECIAL TOOLS
# =========================

echo ""
echo "[INFO] Installing additional security tools..."

python3 -m pip install sqlmap || true

# =========================
# DIRSEARCH (GIT INSTALL)
# =========================
TOOLS_DIR="$HOME/vapt-tools"

mkdir -p "$TOOLS_DIR"

if [ ! -d "$TOOLS_DIR/dirsearch" ]; then
    echo "[INFO] Cloning dirsearch..."
    git clone https://github.com/maurosoria/dirsearch.git "$TOOLS_DIR/dirsearch"
else
    echo "[WARN] dirsearch already exists"
fi

# =========================
# SQLMAP (GIT INSTALL)
# =========================
if [ ! -d "$TOOLS_DIR/sqlmap" ]; then
    echo "[INFO] Cloning sqlmap..."
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git "$TOOLS_DIR/sqlmap"
else
    echo "[WARN] sqlmap already exists"
fi

# =========================
# CLEANUP
# =========================
echo ""
echo "[INFO] Cleaning pip cache..."
python3 -m pip cache purge || true

# =========================
# FINAL STATUS
# =========================
echo ""
echo "======================================"
echo "[PYTHON SETUP COMPLETE]"
echo "======================================"
echo ""

echo "Installed:"
echo " - Core libraries (requests, bs4, aiohttp, etc.)"
echo " - Recon tools (arjun, uro, wafw00f, paramspider)"
echo " - dirsearch (git)"
echo " - sqlmap (git)"
echo ""

echo "Python Version:"
python3 --version

echo ""
echo "IMPORTANT:"
echo "Run: source ~/.zshrc"
echo ""