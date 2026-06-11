#!/bin/bash

# =========================================
# FILE: installers/linux/tools_installer.sh
# =========================================

#
# RECON TOOLS INSTALLER
#
# Installs:
# - Go Recon Tools
# - Python Recon Tools
# - GitHub Recon Tools
# - Crawlers
# - Directory Enumeration Tools
# - Parameter Discovery Tools
#

# =========================================
# STRICT MODE
# =========================================

set -e

# =========================================
# COLORS
# =========================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# =========================================
# HELPER FUNCTIONS
# =========================================

info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =========================================
# TOOLS DIRECTORY
# =========================================

TOOLS_DIR="$HOME/vapt-tools"

mkdir -p "$TOOLS_DIR"

# =========================================
# CHECK GO
# =========================================

info "Checking Golang"

if ! command -v go &> /dev/null
then

    error "Go Not Installed"

    exit 1
fi

success "Go Detected"

# =========================================
# ADD GO BIN TO PATH
# =========================================

export PATH=$PATH:$(go env GOPATH)/bin

# =========================================
# CHECK PYTHON
# =========================================

info "Checking Python3"

if ! command -v python3 &> /dev/null
then

    error "Python3 Not Installed"

    exit 1
fi

success "Python3 Detected"

# =========================================
# UPDATE SYSTEM
# =========================================

info "Updating Package Lists"

sudo apt update -y

success "System Updated"

# =========================================
# INSTALL REQUIRED PACKAGES
# =========================================

info "Installing Required Packages"

sudo apt install -y \
    git \
    curl \
    wget \
    unzip \
    jq \
    ruby-full \
    cargo \
    rustc \
    build-essential \
    python3-pip \
    python3-dev

success "Base Packages Installed"

# =========================================
# INSTALL GO TOOLS
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING GO TOOLS${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

go_tools=(
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"

    "github.com/projectdiscovery/httpx/cmd/httpx@latest"

    "github.com/projectdiscovery/katana/cmd/katana@latest"

    "github.com/lc/gau/v2/cmd/gau@latest"

    "github.com/bp0lr/gauplus@latest"

    "github.com/tomnomnom/waybackurls@latest"

    "github.com/tomnomnom/assetfinder@latest"

    "github.com/hakluke/hakrawler@latest"

    "github.com/tomnomnom/gf@latest"

    "github.com/ffuf/ffuf/v2@latest"

    "github.com/gwen001/github-subdomains/cmd/github-subdomains@latest"
)

for tool in "${go_tools[@]}"
do

    echo ""
    echo -e "${YELLOW}[INSTALLING]${NC}"
    echo "$tool"

    go install "$tool"

    success "Installed"

done

# =========================================
# INSTALL AMASS
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING AMASS${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

go install github.com/owasp-amass/amass/v4/...@master

success "Amass Installed"

# =========================================
# INSTALL FEROXBUSTER
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING FEROXBUSTER${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

cargo install feroxbuster

success "Feroxbuster Installed"

# =========================================
# INSTALL FINDOMAIN
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING FINDOMAIN${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

sudo apt install -y findomain || true

success "Findomain Installed"

# =========================================
# INSTALL PYTHON TOOLS
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING PYTHON TOOLS${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

python_tools=(
    subscraper
    arjun
    paramspider
    uro
)

for tool in "${python_tools[@]}"
do

    echo ""
    echo -e "${YELLOW}[INSTALLING]${NC}"
    echo "$tool"

    pip3 install "$tool"

    success "Installed"

done

# =========================================
# INSTALL DIRSEARCH
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING DIRSEARCH${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

DIRSEARCH_DIR="$TOOLS_DIR/dirsearch"

if [[ ! -d "$DIRSEARCH_DIR" ]]
then

    git clone \
    https://github.com/maurosoria/dirsearch.git \
    "$DIRSEARCH_DIR"

    chmod +x "$DIRSEARCH_DIR/dirsearch.py"

    success "Dirsearch Installed"

else

    warning "Dirsearch Already Exists"

fi

# =========================================
# INSTALL SQLMAP
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING SQLMAP${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

SQLMAP_DIR="$TOOLS_DIR/sqlmap"

if [[ ! -d "$SQLMAP_DIR" ]]
then

    git clone --depth 1 \
    https://github.com/sqlmapproject/sqlmap.git \
    "$SQLMAP_DIR"

    success "SQLMap Installed"

else

    warning "SQLMap Already Exists"

fi

# =========================================
# INSTALL GF PATTERNS
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} INSTALLING GF PATTERNS${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

GF_DIR="$HOME/.gf"

if [[ ! -d "$GF_DIR" ]]
then

    git clone \
    https://github.com/1ndianl33t/Gf-Patterns.git \
    "$GF_DIR"

    success "GF Patterns Installed"

else

    warning "GF Patterns Already Exist"

fi

# =========================================
# VERIFY TOOLS
# =========================================

echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} VERIFYING TOOLS${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

verify_tools=(
    subfinder
    httpx
    katana
    gau
    gauplus
    waybackurls
    assetfinder
    hakrawler
    gf
    ffuf
    github-subdomains
    amass
    feroxbuster
    findomain
    subscraper
    arjun
    paramspider
    uro
)

for tool in "${verify_tools[@]}"
do

    if command -v "$tool" &> /dev/null
    then

        success "$tool Verified"

    else

        warning "$tool Not Found"

    fi

done

# =========================================
# VERIFY DIRSEARCH
# =========================================

DIRSEARCH_DIR="$TOOLS_DIR/dirsearch"

if [[ -d "$DIRSEARCH_DIR" ]]
then

    success "dirsearch Verified"

else

    warning "dirsearch Not Found"

fi

# =========================================
# VERIFY SQLMAP
# =========================================

SQLMAP_DIR="$TOOLS_DIR/sqlmap"

if [[ -d "$SQLMAP_DIR" ]]
then

    success "sqlmap Verified"

else

    warning "sqlmap Not Found"

fi

# =========================================
# FINAL STATUS
# =========================================

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} TOOL INSTALLATION COMPLETED${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

echo -e "${YELLOW}Installed Categories:${NC}"
echo ""
echo " - Subdomain Enumeration"
echo " - URL Enumeration"
echo " - Crawlers"
echo " - Directory Enumeration"
echo " - Parameter Discovery"
echo " - Vulnerability Scanners"
echo ""

echo -e "${YELLOW}Installed Tools:${NC}"
echo ""
echo " - subfinder"
echo " - subscraper"
echo " - findomain"
echo " - amass"
echo " - github-subdomains"
echo " - assetfinder"
echo " - httpx"
echo " - katana"
echo " - gau"
echo " - gauplus"
echo " - waybackurls"
echo " - hakrawler"
echo " - gf"
echo " - uro"
echo " - ffuf"
echo " - dirsearch"
echo " - feroxbuster"
echo " - arjun"
echo " - paramspider"
echo " - sqlmap"
echo ""

echo -e "${GREEN}Linux Recon Environment Ready${NC}"
echo ""

exit 0