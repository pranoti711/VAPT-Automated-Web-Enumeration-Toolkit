#!/bin/bash

# =========================================
# PRO RECON ENGINE - ENVIRONMENT SETUP
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
# ROOT PATHS
# =========================
GO_PATH="$HOME/go"
GO_BIN="$GO_PATH/bin"

RECON_HOME="$HOME/pro-recon-engine"
VENV_PATH="$HOME/pro-recon-env"

BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"

# =========================
# CHECK SHELL FILE
# =========================
if [ -f "$BASHRC" ]; then
    PROFILE="$BASHRC"
elif [ -f "$ZSHRC" ]; then
    PROFILE="$ZSHRC"
else
    PROFILE="$BASHRC"
fi

info "Using shell profile: $PROFILE"

# =========================
# CREATE CORE DIRECTORIES
# =========================
info "Creating core directories..."

mkdir -p "$GO_PATH"/{bin,src,pkg}
mkdir -p "$RECON_HOME"
mkdir -p "$HOME/vapt-tools"

success "Directories created"

# =========================
# GO ENV SETUP
# =========================
info "Setting Go environment variables..."

if ! grep -q "PRO RECON GO ENV" "$PROFILE"; then
    cat <<EOF >> "$PROFILE"

# =========================================
# PRO RECON ENGINE - GO ENV
# =========================================
export GOROOT=/usr/local/go
export GOPATH=$GO_PATH
export PATH=\$PATH:\$GOROOT/bin:\$GOPATH/bin
EOF
fi

export GOROOT=/usr/local/go
export GOPATH=$GO_PATH
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin

success "Go environment configured"

# =========================
# PYTHON ENV SETUP
# =========================
info "Setting Python environment..."

if ! grep -q "PRO RECON PY ENV" "$PROFILE"; then
    cat <<EOF >> "$PROFILE"

# =========================================
# PRO RECON ENGINE - PYTHON ENV
# =========================================
source $VENV_PATH/bin/activate 2>/dev/null
EOF
fi

success "Python environment configured"

# =========================
# RECON ENGINE PATH
# =========================
info "Setting Recon Engine PATH..."

if ! grep -q "PRO RECON ENGINE PATH" "$PROFILE"; then
    cat <<EOF >> "$PROFILE"

# =========================================
# PRO RECON ENGINE
# =========================================
export RECON_HOME=$RECON_HOME
export PATH=\$PATH:\$RECON_HOME
EOF
fi

export RECON_HOME="$RECON_HOME"
export PATH=$PATH:$RECON_HOME

success "Recon engine path set"

# =========================
# CREATE GLOBAL RECON COMMAND HOOK
# =========================
info "Creating recon CLI wrapper..."

sudo bash -c "cat > /usr/local/bin/recon" << 'EOF'
#!/bin/bash
python3 $HOME/pro-recon-engine/recon.py "$@"
EOF

sudo chmod +x /usr/local/bin/recon

success "Global 'recon' command created"

# =========================
# OPTIONAL: SPEED OPTIMIZATION FLAGS
# =========================
info "Adding performance environment tweaks..."

if ! grep -q "PRO RECON PERF" "$PROFILE"; then
    cat <<EOF >> "$PROFILE"

# =========================================
# PRO RECON ENGINE - PERFORMANCE
# =========================================
export PYTHONUNBUFFERED=1
export GODEBUG=netdns=go
EOF
fi

success "Performance tweaks added"

# =========================
# APPLY IMMEDIATELY
# =========================
info "Applying environment changes..."

source "$PROFILE" 2>/dev/null || true

# =========================
# FINAL CHECK
# =========================
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} ENVIRONMENT SETUP COMPLETE${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

echo "Go Path: $GOPATH"
echo "Recon Home: $RECON_HOME"
echo "Python Env: $VENV_PATH"
echo ""

echo "Test command:"
echo "  recon -d example.com"
echo ""

success "System is ready for PRO RECON ENGINE"