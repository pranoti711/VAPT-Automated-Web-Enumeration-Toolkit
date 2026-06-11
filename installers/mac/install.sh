#!/bin/bash

# =========================================
# PRO RECON ENGINE - macOS INSTALLER
# ENTRYPOINT
# =========================================

set -euo pipefail

echo "======================================"
echo "   PRO RECON ENGINE - macOS SETUP"
echo "======================================"
echo ""

# =========================
# SCRIPT DIRECTORY
# =========================
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# =========================
# CHECKS
# =========================

echo "[INFO] Checking system requirements..."

if ! command -v brew >/dev/null 2>&1; then
    echo "[ERROR] Homebrew not installed"
    echo "Install it from: https://brew.sh"
    exit 1
fi

if ! command -v git >/dev/null 2>&1; then
    echo "[INFO] Installing git..."
    brew install git
fi

if ! command -v curl >/dev/null 2>&1; then
    echo "[INFO] curl missing (rare), installing..."
    brew install curl
fi

echo "[OK] Base requirements satisfied"
echo ""

# =========================
# RUN MODULES
# =========================

echo "======================================"
echo "[STEP 1] GO SETUP"
echo "======================================"
bash "$SCRIPT_DIR/go_setup.sh"

echo ""
echo "======================================"
echo "[STEP 2] PYTHON SETUP"
echo "======================================"
bash "$SCRIPT_DIR/python_setup.sh"

echo ""
echo "======================================"
echo "[STEP 3] ENVIRONMENT SETUP"
echo "======================================"
bash "$SCRIPT_DIR/env_setup.sh"

echo ""
echo "======================================"
echo "[STEP 4] RECON TOOLS INSTALLATION"
echo "======================================"
bash "$SCRIPT_DIR/tools_installer.sh"

# =========================
# FINAL STATUS
# =========================

echo ""
echo "======================================"
echo "   INSTALLATION COMPLETE (macOS)"
echo "======================================"
echo ""
echo "[OK] Go installed & configured"
echo "[OK] Python environment ready"
echo "[OK] Recon tools installed"
echo "[OK] Environment variables set"
echo ""

echo "IMPORTANT:"
echo " - Restart terminal (zsh recommended)"
echo " - Run: source ~/.zshrc"
echo ""

echo "PRO RECON ENGINE READY 🚀"
echo ""