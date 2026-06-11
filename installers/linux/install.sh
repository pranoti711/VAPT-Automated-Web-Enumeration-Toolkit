#!/bin/bash
#!/bin/bash

# =========================================
# FILE: installers/linux/tools_installer.sh
# RECON / VAPT TOOLKIT INSTALLER (UPDATED)
# =========================================

set -e

echo "======================================"
echo "  VAPT RECON TOOLKIT INSTALLER"
echo "======================================"

# =========================
# SYSTEM UPDATE
# =========================
echo "[+] Updating system packages..."
sudo apt update -y && sudo apt upgrade -y

# =========================
# BASIC DEPENDENCIES
# =========================
echo "[+] Installing base dependencies..."
sudo apt install -y \
    git curl wget unzip tar build-essential \
    python3 python3-pip python3-venv \
    golang-go jq

# =========================
# GO ENV SETUP
# =========================
echo "[+] Setting up Go environment..."

GO_PATH="$HOME/go"
GO_BIN="$GO_PATH/bin"

if ! grep -q "GO_PATH" ~/.bashrc; then
    echo "export GOPATH=$GO_PATH" >> ~/.bashrc
    echo "export PATH=\$PATH:$GO_BIN" >> ~/.bashrc
fi

export GOPATH=$GO_PATH
export PATH=$PATH:$GO_BIN

mkdir -p $GO_PATH/{bin,src,pkg}

# =========================
# PYTHON SETUP
# =========================
echo "[+] Setting up Python environment..."

python3 -m pip install --upgrade pip setuptools wheel

# =========================
# GO RECON TOOLS
# =========================
echo "[+] Installing Go-based recon tools..."

GO_TOOLS=(
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    "github.com/projectdiscovery/httpx/cmd/httpx@latest"
    "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
    "github.com/tomnomnom/assetfinder@latest"
    "github.com/tomnomnom/httprobe@latest"
    "github.com/lc/gau/v2/cmd/gau@latest"
    "github.com/OJ/gobuster/v3@latest"
)

for tool in "${GO_TOOLS[@]}"; do
    echo "[+] Installing $tool"
    go install "$tool"
done

# =========================
# PYTHON RECON TOOLS
# =========================
echo "[+] Installing Python recon tools..."

PY_TOOLS=(
    "requests"
    "beautifulsoup4"
    "lxml"
    "dnspython"
    "argparse"
    "urllib3"
    "colorama"
    "tqdm"
)

pip3 install "${PY_TOOLS[@]}"

# =========================
# DIRECTORY ENUM TOOLS
# =========================
echo "[+] Installing directory brute-force tools..."

GO install github.com/OJ/gobuster/v3@latest || true

# =========================
# PARAMETER DISCOVERY TOOLS
# =========================
echo "[+] Installing parameter discovery tools..."

go install github.com/tomnomnom/qsreplace@latest || true

# =========================
# GITHUB RECON TOOLS
# =========================
echo "[+] Installing GitHub recon tools..."

go install github.com/gwen001/github-subdomains@latest || true

# =========================
# CRAWLING TOOLS
# =========================
echo "[+] Installing crawling tools..."

go install github.com/projectdiscovery/katana/cmd/katana@latest || true

# =========================
# VERIFY INSTALLATION
# =========================
echo "[+] Verifying installation..."

echo "Go Version:"
go version || true

echo "Python Version:"
python3 --version

echo "Installed Go binaries:"
ls $GO_BIN || true

# =========================
# FINAL MESSAGE
# =========================
echo "======================================"
echo " INSTALLATION COMPLETE"
echo " Add GOPATH to PATH if not already:"
echo " export PATH=\$PATH:\$HOME/go/bin"
echo "======================================"