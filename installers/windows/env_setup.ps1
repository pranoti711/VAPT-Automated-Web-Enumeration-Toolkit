# =========================================
# PRO RECON ENGINE - ENV SETUP (WINDOWS)
# =========================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# =========================
# HELPERS
# =========================
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function OK($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

# =========================
# PATHS
# =========================
$USER_HOME = $env:USERPROFILE

$GO_PATH = Join-Path $USER_HOME "go"
$GO_BIN  = Join-Path $GO_PATH "bin"

$VAPT_HOME = Join-Path $USER_HOME "vapt-tools"
$OUTPUTS   = Join-Path $USER_HOME "vapt-outputs"
$WORDLISTS = Join-Path $USER_HOME "wordlists"

# AUTO-DETECT PYTHON SCRIPTS (FIX)
$PY_SCRIPTS = Join-Path $env:LOCALAPPDATA "Programs\Python"
$PY_BIN = ""

if (Test-Path $PY_SCRIPTS) {
    $latestPython = Get-ChildItem $PY_SCRIPTS -Directory |
        Where-Object { $_.Name -like "Python*" } |
        Sort-Object Name -Descending |
        Select-Object -First 1

    if ($latestPython) {
        $PY_BIN = Join-Path $latestPython.FullName "Scripts"
    }
}

# =========================
# CREATE DIRECTORIES
# =========================
Info "Creating core directories..."

$dirs = @(
    $GO_PATH,
    $GO_BIN,
    $VAPT_HOME,
    $OUTPUTS,
    $WORDLISTS,

    "$OUTPUTS\scans",
    "$OUTPUTS\reports",
    "$OUTPUTS\logs",

    "$VAPT_HOME\subdomains",
    "$VAPT_HOME\urls",
    "$VAPT_HOME\dirs",
    "$VAPT_HOME\params"
)

foreach ($d in $dirs) {
    if (!(Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
        OK "Created: $d"
    } else {
        Warn "Exists: $d"
    }
}

# =========================
# USER PATH HANDLING (FIXED)
# =========================
Info "Updating PATH safely..."

$currentPath = [Environment]::GetEnvironmentVariable("Path","User")

$addPaths = @(
    $GO_BIN,
    $VAPT_HOME,
    $PY_BIN
) | Where-Object { $_ -and $_ -ne "" }

foreach ($p in $addPaths) {
    if ($currentPath -notlike "*$p*") {
        $currentPath = "$currentPath;$p"
        OK "Added PATH: $p"
    } else {
        Warn "Already in PATH: $p"
    }
}

[Environment]::SetEnvironmentVariable(
    "Path",
    $currentPath,
    "User"
)

# =========================
# ENV VARIABLES
# =========================
Info "Setting environment variables..."

$envVars = @{
    "GOPATH"         = $GO_PATH
    "VAPT_HOME"      = $VAPT_HOME
    "VAPT_OUTPUTS"   = $OUTPUTS
    "WORDLISTS_PATH" = $WORDLISTS
}

foreach ($k in $envVars.Keys) {
    [Environment]::SetEnvironmentVariable(
        $k,
        $envVars[$k],
        "User"
    )
    OK "$k set"
}

# =========================
# SESSION REFRESH (IMPORTANT FIX)
# =========================
Info "Refreshing session PATH..."

$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [Environment]::GetEnvironmentVariable("Path","User")

# =========================
# WORDLIST STRUCTURE
# =========================
Info "Creating wordlist structure..."

$wordlists = @(
    "subdomains.txt",
    "dirs.txt",
    "params.txt",
    "api.txt"
)

foreach ($w in $wordlists) {
    $file = Join-Path $WORDLISTS $w
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file -Force | Out-Null
        OK "Created wordlist: $w"
    }
}

# =========================
# CATEGORY STRUCTURE
# =========================
Info "Creating tool categories..."

$categories = @(
    "subdomain_enum",
    "url_enum",
    "directory_enum",
    "parameter_enum",
    "crawler",
    "scanner",
    "reports"
)

foreach ($c in $categories) {
    $path = Join-Path $VAPT_HOME $c
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        OK "Created category: $c"
    }
}

# =========================
# FINAL OUTPUT
# =========================
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " PRO RECON ENV READY (WINDOWS)" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Core Paths:"
Write-Host " - GOPATH: $GO_PATH"
Write-Host " - VAPT_HOME: $VAPT_HOME"
Write-Host " - OUTPUTS: $OUTPUTS"
Write-Host " - WORDLISTS: $WORDLISTS"
Write-Host ""

Write-Host "Status:"
Write-Host " - PATH configured safely"
Write-Host " - Directories ready"
Write-Host " - Environment variables set"
Write-Host ""

Write-Host "Recommended:"
Write-Host " Restart PowerShell before running recon"
Write-Host ""

exit 0