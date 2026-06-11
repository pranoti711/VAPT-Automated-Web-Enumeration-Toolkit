#!/bin/bash
#!/bin/bash

# =========================================
# PRO RECON ENGINE - PYTHON SETUP
# =========================================

set -e

# =========================
# COLORS
# =========================
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${CYAN}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =========================
# CHECK PYTHON
# =========================
info "Checking Python3..."

if ! command -v python3 &>/dev/null; then
    error "Python3 not installed"
    exit 1
fi

success "Python3 detected: $(python3 --version)"

# =========================
# INSTALL PIP
# =========================
info "Ensuring pip is installed..."

sudo apt update -y
sudo apt install -y python3-pip python3-venv

# =========================
# UPGRADE CORE TOOLS
# =========================
info "Upgrading pip ecosystem..."

python3 -m pip install --upgrade pip setuptools wheel

success "pip upgraded"

# =========================
# CREATE GLOBAL VENV (OPTIONAL BUT CLEAN)
# =========================
VENV_DIR="$HOME/pro-recon-env"

if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    success "Virtual environment created at $VENV_DIR"
else
    warning "Virtual environment already exists"
fi

# =========================
# ACTIVATE VENV (FOR INSTALL)
# =========================
source "$VENV_DIR/bin/activate"

# =========================
# CORE RECON PYTHON PACKAGES
# =========================
info "Installing Recon Python libraries..."

pip install \
    requests \
    beautifulsoup4 \
    lxml \
    dnspython \
    urllib3 \
    colorama \
    tqdm \
    rich \
    aiohttp \
    tldextract \
    pyfiglet

success "Core libraries installed"

# =========================
# RECON SECURITY TOOLS (PYTHON BASED)
# =========================
info "Installing Python recon tools..."

pip install \
    arjun \
    paramspider \
    uro \
    waybackurls \
    subscraper

success "Recon tools installed"

# =========================
# SAFE VERIFICATION
# =========================
info "Verifying Python setup..."

python -c "import requests, dns, bs4; print('Core imports OK')" || warning "Some imports failed"

# =========================
# ENVIRONMENT EXPORT
# =========================
BASHRC="$HOME/.bashrc"

if ! grep -q "pro-recon-env" "$BASHRC"; then
    echo "" >> "$BASHRC"
    echo "# PRO RECON ENGINE PYTHON ENV" >> "$BASHRC"
    echo "source $VENV_DIR/bin/activate" >> "$BASHRC"
fi

# =========================
# FINAL STATUS
# =========================
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} PYTHON SETUP COMPLETE${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Virtual Env: $VENV_DIR"
echo "Status: READY FOR PRO RECON ENGINE"
echo ""
echo "Next step:"
echo "  run: recon -d example.com"
echo ""