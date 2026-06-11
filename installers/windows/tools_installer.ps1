# =========================================
# PRO RECON ENGINE - WINDOWS TOOLS INSTALLER
# =========================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# =========================
# HELPERS
# =========================
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function OK($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }

function ToolExists($t){
    return $null -ne (Get-Command $t -ErrorAction SilentlyContinue)
}

# =========================
# DIRECTORIES
# =========================
$TOOLS_DIR = Join-Path $env:USERPROFILE "vapt-tools"
if (!(Test-Path $TOOLS_DIR)) {
    New-Item -ItemType Directory -Path $TOOLS_DIR | Out-Null
}

# =========================
# GO TOOLS (FULL LIST)
# =========================
Info "Installing Go tools..."

$goTools = @(
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
    "github.com/projectdiscovery/httpx/cmd/httpx@latest",
    "github.com/projectdiscovery/katana/cmd/katana@latest",
    "github.com/lc/gau/v2/cmd/gau@latest",
    "github.com/tomnomnom/waybackurls@latest",
    "github.com/tomnomnom/assetfinder@latest",
    "github.com/hakluke/hakrawler@latest",
    "github.com/tomnomnom/gf@latest",
    "github.com/ffuf/ffuf/v2@latest",
    "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
    "github.com/tomnomnom/qsreplace@latest"
)

foreach ($tool in $goTools) {

    $name = ($tool -split "/")[-1]

    if (ToolExists $name) {
        Warn "$name already installed"
        continue
    }

    try {
        go install $tool
        OK "$name installed"
    }
    catch {
        Warn "$name failed"
    }
}

# =========================
# AMASS (FIXED - WINDOWS SAFE)
# =========================
Info "Installing Amass..."

if (!(ToolExists "amass")) {
    try {
        go install github.com/owasp-amass/amass/v4/...@master
        OK "Amass installed"
    }
    catch {
        Warn "Amass install failed"
    }
} else {
    Warn "Amass already installed"
}

# =========================
# PYTHON TOOLS (FULL SET)
# =========================
Info "Installing Python tools..."

$pythonTools = @(
    "arjun",
    "uro",
    "wafw00f",
    "paramspider",
    "subscraper"
)

foreach ($p in $pythonTools) {
    try {
        python -m pip install $p
        OK "$p installed"
    }
    catch {
        Warn "$p failed"
    }
}

# =========================
# FERoxBUSTER (CARGO CHECK)
# =========================
Info "Installing Feroxbuster..."

if (!(ToolExists "feroxbuster")) {
    if (Get-Command cargo -ErrorAction SilentlyContinue) {
        cargo install feroxbuster
        OK "Feroxbuster installed"
    } else {
        Warn "Cargo not installed (skip feroxbuster)"
    }
} else {
    Warn "Feroxbuster already installed"
}

# =========================
# FINDOMAIN (OPTIONAL)
# =========================
Info "Installing Findomain..."

if (!(ToolExists "findomain")) {
    try {
        winget install --id=Findomain.Findomain -e
        OK "Findomain installed"
    }
    catch {
        Warn "Findomain not available via winget"
    }
} else {
    Warn "Findomain already installed"
}

# =========================
# DIRSEARCH
# =========================
Info "Installing Dirsearch..."

if (!(Test-Path "$TOOLS_DIR\dirsearch")) {
    git clone https://github.com/maurosoria/dirsearch.git "$TOOLS_DIR\dirsearch"
    OK "Dirsearch installed"
} else {
    Warn "Dirsearch exists"
}

# =========================
# SQLMAP
# =========================
Info "Installing SQLMap..."

if (!(Test-Path "$TOOLS_DIR\sqlmap")) {
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git "$TOOLS_DIR\sqlmap"
    OK "SQLMap installed"
} else {
    Warn "SQLMap exists"
}

# =========================
# GF PATTERNS (FIXED REPO)
# =========================
Info "Installing GF patterns..."

$gfDir = Join-Path $env:USERPROFILE ".gf"

if (!(Test-Path $gfDir)) {
    git clone https://github.com/1ndianl33t/Gf-Patterns.git $gfDir
    OK "GF patterns installed"
} else {
    Warn "GF exists"
}

# =========================
# VERIFICATION (FULL LIST)
# =========================
Info "Verifying tools..."

$verify_tools = @(
    "subfinder",
    "httpx",
    "katana",
    "gau",
    "waybackurls",
    "assetfinder",
    "hakrawler",
    "gf",
    "ffuf",
    "amass",
    "feroxbuster",
    "arjun",
    "paramspider",
    "uro",
    "nuclei",
    "qsreplace"
)

foreach ($t in $verify_tools) {

    if (ToolExists $t) {
        OK "$t OK"
    } else {
        Warn "$t missing"
    }
}

# =========================
# FINAL STATUS
# =========================
Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host " PRO RECON ENGINE READY (WINDOWS)" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

Write-Host "Categories Installed:"
Write-Host " - Subdomain Enumeration"
Write-Host " - URL Enumeration"
Write-Host " - Crawling Engine"
Write-Host " - Directory Bruteforce"
Write-Host " - Parameter Discovery"
Write-Host " - Vulnerability Scanning"
Write-Host ""

exit 0