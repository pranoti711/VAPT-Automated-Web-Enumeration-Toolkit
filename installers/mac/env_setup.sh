#!/bin/bash

# =========================================
# PRO RECON ENGINE - macOS ENV SETUP
# =========================================

set -euo pipefail

echo "======================================"
echo "[ENV SETUP] macOS Environment Config"
echo "======================================"
echo ""

# =========================
# BASE PATHS
# =========================
USER_HOME="$HOME"

GO_PATH="$USER_HOME/go"
GO_BIN="$GO_PATH/bin"

VAPT_HOME="$USER_HOME/vapt-tools"
VAPT_OUTPUTS="$USER_HOME/vapt-outputs"
WORDLISTS="$USER_HOME/wordlists"

# =========================
# CREATE DIRECTORIES
# =========================
echo "[INFO] Creating framework directories..."

mkdir -p \
"$GO_PATH" \
"$GO_BIN" \
"$VAPT_HOME" \
"$VAPT_OUTPUTS" \
"$WORDLISTS" \
"$VAPT_OUTPUTS/scans" \
"$VAPT_OUTPUTS/reports" \
"$VAPT_OUTPUTS/logs" \
"$VAPT_HOME/subdomains" \
"$VAPT_HOME/urls" \
"$VAPT_HOME/dirs" \
"$VAPT_HOME/params"

echo "[OK] Directories ready"

# =========================
# DETECT SHELL (macOS uses zsh default)
# =========================
SHELL_RC="$HOME/.zshrc"

if [ ! -f "$SHELL_RC" ]; then
    touch "$SHELL_RC"
fi

# =========================
# SAFE PATH ADD FUNCTION
# =========================
add_path() {
    if ! grep -q "$1" "$SHELL_RC"; then
        echo "export PATH=\$PATH:$1" >> "$SHELL_RC"
        echo "[OK] PATH added: $1"
    else
        echo "[WARN] PATH exists: $1"
    fi
}

# =========================
# ENV VARIABLES FUNCTION
# =========================
set_env() {
    if ! grep -q "$1=" "$SHELL_RC"; then
        echo "export $1=$2" >> "$SHELL_RC"
        echo "[OK] $1 set"
    else
        echo "[WARN] $1 already set"
    fi
}

# =========================
# ADD PATHS
# =========================
echo ""
echo "[INFO] Configuring PATH..."

add_path "$GO_BIN"
add_path "$VAPT_HOME"

# Python Scripts (macOS Homebrew detection safe)
PY_SCRIPTS="/opt/homebrew/bin"
if [ -d "$PY_SCRIPTS" ]; then
    add_path "$PY_SCRIPTS"
fi

# =========================
# SET ENV VARIABLES
# =========================
echo ""
echo "[INFO] Setting environment variables..."

set_env "GOPATH" "$GO_PATH"
set_env "VAPT_HOME" "$VAPT_HOME"
set_env "VAPT_OUTPUTS" "$VAPT_OUTPUTS"
set_env "WORDLISTS_PATH" "$WORDLISTS"

# =========================
# APPLY TO CURRENT SESSION
# =========================
export GOPATH="$GO_PATH"
export PATH="$PATH:$GO_BIN:$VAPT_HOME"

# =========================
# WORDLIST STRUCTURE
# =========================
echo ""
echo "[INFO] Creating wordlist structure..."

touch "$WORDLISTS/subdomains.txt"
touch "$WORDLISTS/dirs.txt"
touch "$WORDLISTS/params.txt"
touch "$WORDLISTS/api.txt"

# =========================
# TOOL CATEGORIES
# =========================
echo ""
echo "[INFO] Creating tool categories..."

mkdir -p \
"$VAPT_HOME/subdomain_enum" \
"$VAPT_HOME/url_enum" \
"$VAPT_HOME/directory_enum" \
"$VAPT_HOME/parameter_enum" \
"$VAPT_HOME/crawler" \
"$VAPT_HOME/scanner" \
"$VAPT_HOME/reports"

# =========================
# FINAL OUTPUT
# =========================
echo ""
echo "======================================"
echo "[ENV SETUP COMPLETE]"
echo "======================================"
echo ""

echo "Configured:"
echo " - GOPATH"
echo " - VAPT_HOME"
echo " - VAPT_OUTPUTS"
echo " - WORDLISTS_PATH"
echo ""

echo "Created:"
echo " - Tool directories"
echo " - Output structure"
echo " - Wordlist templates"
echo ""

echo "IMPORTANT:"
echo "Run: source ~/.zshrc"
echo ""