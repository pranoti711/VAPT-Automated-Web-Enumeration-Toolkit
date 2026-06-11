#!/bin/bash

# =========================================
# PRO RECON ENGINE - TOOL INSTALLER (UPGRADED)
# =========================================

set -e

# =========================
# COLORS
# =========================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${CYAN}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =========================
# DIRECTORIES
# =========================
TOOLS_DIR="$HOME/vapt-tools"
mkdir -p "$TOOLS_DIR"

# =========================
# SAFE GO ENV FIX (IMPORTANT)
# =========================
if ! command -v go &>/dev/null; then
    error "Go is not installed. Run go_setup.sh first."
    exit 1
fi

export PATH=$PATH:$(go env GOPATH)/bin

# =========================
# SAFE PYTHON CHECK
# =========================
if ! command -v python3 &>/dev/null; then
    error "Python3 not installed"
    exit 1
fi

# =========================
# SYSTEM UPDATE
# =========================
info "Updating system..."
sudo apt update -y

# =========================
# BASE PACKAGES
# =========================
info "Installing base dependencies..."

sudo apt install -y \
    git curl wget unzip jq \
    build-essential python3-pip python3-dev \
    cargo rustc

success "Base packages installed"

# =========================
# GO TOOLS LIST (CLEANED)
# =========================
go_tools=(
"github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
"github.com/projectdiscovery/httpx/cmd/httpx@latest"
"github.com/projectdiscovery/katana/cmd/katana@latest"
"github.com/lc/gau/v2/cmd/gau@latest"
"github.com/tomnomnom/waybackurls@latest"
"github.com/tomnomnom/assetfinder@latest"
"github.com/hakluke/hakrawler@latest"
"github.com/ffuf/ffuf/v2@latest"
"github.com/tomnomnom/gf@latest"
"github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
"github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
)

# =========================
# INSTALL GO TOOLS (SAFE)
# =========================
info "Installing Go tools..."

for tool in "${go_tools[@]}"; do
    echo -e "${YELLOW}[GO]${NC} $tool"
    go install "$tool" || warning "Failed: $tool"
done

success "Go tools installed"

# =========================
# AMASS
# =========================
info "Installing Amass..."
go install github.com/owasp-amass/amass/v4/...@master || warning "Amass failed"

# =========================
# RUST TOOLS
# =========================
info "Installing Feroxbuster..."
cargo install feroxbuster || warning "Feroxbuster failed"

# =========================
# FINDOMAIN
# =========================
info "Installing Findomain..."
sudo apt install -y findomain || warning "Findomain not available via apt"

# =========================
# PYTHON TOOLS (FIXED)
# =========================
info "Installing Python tools..."

python3 -m pip install --upgrade pip setuptools wheel

python3 -m pip install \
    arjun \
    paramspider \
    uro \
    requests \
    beautifulsoup4 \
    dnspython \
    tqdm \
    colorama

success "Python tools installed"

# =========================
# DIRSEARCH
# =========================
info "Installing Dirsearch..."

if [ ! -d "$TOOLS_DIR/dirsearch" ]; then
    git clone https://github.com/maurosoria/dirsearch.git "$TOOLS_DIR/dirsearch"
    success "Dirsearch installed"
else
    warning "Dirsearch already exists"
fi

# =========================
# SQLMAP
# =========================
info "Installing SQLMap..."

if [ ! -d "$TOOLS_DIR/sqlmap" ]; then
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git "$TOOLS_DIR/sqlmap"
    success "SQLMap installed"
else
    warning "SQLMap already exists"
fi

# =========================
# GF PATTERNS
# =========================
info "Installing GF patterns..."

if [ ! -d "$HOME/.gf" ]; then
    git clone https://github.com/1ndianl33t/Gf-Patterns.git "$HOME/.gf"
    success "GF patterns installed"
else
    warning "GF patterns already exist"
fi

# =========================
# VERIFY INSTALLATION
# =========================
info "Verifying tools..."

tools_to_check=(
subfinder httpx katana gau waybackurls assetfinder hakrawler gf ffuf nuclei dnsx
amass feroxbuster arjun paramspider uro
)

for t in "${tools_to_check[@]}"; do
    if command -v "$t" &>/dev/null; then
        success "$t OK"
    else
        warning "$t missing"
    fi
done

# =========================
# FINAL MESSAGE
# =========================
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} PRO RECON ENGINE READY${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next step:"
echo "  run: recon -d example.com"
echo ""
echo "Tools installed for:"
echo " - Subdomain Enumeration"
echo " - Crawling"
echo " - URL Discovery"
echo " - Vulnerability scanning"
echo ""