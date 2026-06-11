# =========================================
# PRO RECON ENGINE - PYTHON SETUP (WINDOWS)
# =========================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# =========================
# CONFIG
# =========================
$PYTHON_VERSION = "3.12.10"
$PY_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-amd64.exe"

$TEMP_DIR = "$env:TEMP\vapt_python_setup"
$PY_INSTALLER = "$TEMP_DIR\python.exe"

$TOOLS_DIR = "$env:USERPROFILE\vapt-tools"

# =========================
# LOG HELPERS
# =========================
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function OK($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

# =========================
# CHECK PYTHON
# =========================
function Test-Python {
    try {
        $null = Get-Command python -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

Info "Checking Python installation..."

if (Test-Python) {
    OK "Python already installed"
    try { python --version } catch {}
} else {

    # =========================
    # CREATE TEMP DIR
    # =========================
    if (!(Test-Path $TEMP_DIR)) {
        New-Item -ItemType Directory -Path $TEMP_DIR | Out-Null
    }

    # =========================
    # DOWNLOAD PYTHON
    # =========================
    Info "Downloading Python $PYTHON_VERSION..."

    try {
        Invoke-WebRequest -Uri $PY_URL -OutFile $PY_INSTALLER
        OK "Python downloaded"
    } catch {
        Err "Download failed"
        exit 1
    }

    # =========================
    # INSTALL PYTHON
    # =========================
    Info "Installing Python..."

    try {
        Start-Process -FilePath $PY_INSTALLER -Wait -ArgumentList @(
            "/quiet",
            "InstallAllUsers=1",
            "PrependPath=1",
            "Include_pip=1"
        )

        OK "Python installed"
    } catch {
        Err "Python install failed"
        exit 1
    }
}

# =========================
# REFRESH PATH (IMPORTANT FIX)
# =========================
Info "Refreshing PATH..."

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path","User")

# =========================
# VERIFY PYTHON
# =========================
Info "Verifying Python..."

if (Test-Python) {
    OK "Python OK"
    python --version
} else {
    Err "Python not detected"
    exit 1
}

# =========================
# VERIFY PIP
# =========================
Info "Checking pip..."

try {
    python -m pip --version | Out-Null
    OK "pip available"
} catch {
    Err "pip missing"
    exit 1
}

# =========================
# UPGRADE PIP
# =========================
Info "Upgrading pip..."

python -m pip install --upgrade pip setuptools wheel | Out-Null
OK "pip upgraded"

# =========================
# CORE PACKAGES
# =========================
$core = @(
    "requests",
    "colorama",
    "urllib3",
    "beautifulsoup4",
    "lxml",
    "aiohttp",
    "tqdm"
)

Info "Installing core packages..."

foreach ($p in $core) {
    python -m pip install $p | Out-Null
    OK $p
}

# =========================
# RECON PYTHON TOOLS
# =========================
$tools = @(
    "arjun",
    "uro",
    "wafw00f",
    "paramspider"
)

Info "Installing recon tools..."

foreach ($t in $tools) {
    python -m pip install $t | Out-Null
    OK $t
}

# =========================
# CREATE TOOL DIRECTORY
# =========================
if (!(Test-Path $TOOLS_DIR)) {
    New-Item -ItemType Directory -Path $TOOLS_DIR | Out-Null
}

# =========================
# DIRSEARCH
# =========================
Info "Installing dirsearch..."

$dirsearch = "$TOOLS_DIR\dirsearch"

if (!(Test-Path $dirsearch)) {
    git clone https://github.com/maurosoria/dirsearch.git $dirsearch
    OK "dirsearch installed"
} else {
    Warn "dirsearch exists"
}

# =========================
# SQLMAP
# =========================
Info "Installing sqlmap..."

$sqlmap = "$TOOLS_DIR\sqlmap"

if (!(Test-Path $sqlmap)) {
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git $sqlmap
    OK "sqlmap installed"
} else {
    Warn "sqlmap exists"
}

# =========================
# CLEAN TEMP
# =========================
Info "Cleaning temp files..."

Remove-Item -Recurse -Force $TEMP_DIR -ErrorAction SilentlyContinue

OK "Cleanup done"

# =========================
# FINAL STATUS
# =========================
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " PYTHON ENV READY (PRO RECON ENGINE)" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Installed:"
Write-Host " - Python Core"
Write-Host " - pip packages"
Write-Host " - arjun / uro / wafw00f / paramspider"
Write-Host " - dirsearch"
Write-Host " - sqlmap"
Write-Host ""

exit 0