#!/bin/bash

# =========================================
# PRO RECON ENGINE - macOS GO SETUP
# =========================================

set -euo pipefail

echo "======================================"
echo "[GO SETUP] macOS Golang Installer"
echo "======================================"
echo ""

# =========================
# CHECK EXISTING GO
# =========================
if command -v go >/dev/null 2>&1; then
    echo "[OK] Go already installed"
    go version
    exit 0
fi

# =========================
# CHECK HOMEBREW
# =========================
if ! command -v brew >/dev/null 2>&1; then
    echo "[ERROR] Homebrew not found"
    echo "Install it first: https://brew.sh"
    exit 1
fi

# =========================
# INSTALL GO
# =========================
echo "[INFO] Installing Go via Homebrew..."
brew install go

# =========================
# GOPATH SETUP
# =========================
GO_PATH="$HOME/go"
GO_BIN="$GO_PATH/bin"

mkdir -p "$GO_BIN"

# =========================
# SHELL DETECTION (zsh default on macOS)
# =========================
SHELL_RC="$HOME/.zshrc"

if [ ! -f "$SHELL_RC" ]; then
    touch "$SHELL_RC"
fi

echo "[INFO] Configuring Go environment..."

# Add GOPATH
grep -qxF "export GOPATH=$GO_PATH" "$SHELL_RC" || \
echo "export GOPATH=$GO_PATH" >> "$SHELL_RC"

# Add Go bin to PATH
grep -qxF "export PATH=\$PATH:$GO_BIN" "$SHELL_RC" || \
echo "export PATH=\$PATH:$GO_BIN" >> "$SHELL_RC"

# =========================
# APPLY CURRENT SESSION
# =========================
export GOPATH="$GO_PATH"
export PATH="$PATH:$GO_BIN"

# =========================
# VERIFY INSTALLATION
# =========================
echo "[INFO] Verifying Go installation..."
sleep 2

if command -v go >/dev/null 2>&1; then
    echo "[OK] Go installed successfully"
    go version
else
    echo "[ERROR] Go installation failed"
    exit 1
fi

# =========================
# FINAL OUTPUT
# =========================
echo ""
echo "======================================"
echo "[GO SETUP COMPLETE]"
echo "======================================"
echo ""
echo "GOPATH: $GO_PATH"
echo "GOBIN : $GO_BIN"
echo ""
echo "IMPORTANT:"
echo "Run: source ~/.zshrc"
echo ""