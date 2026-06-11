# =========================================
# PRO RECON ENGINE - WINDOWS INSTALLER
# =========================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# =========================
# BANNER
# =========================
Clear-Host

Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "        PRO RECON ENGINE INSTALLER (WINDOWS)" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# =========================
# LOG FILE
# =========================
$LOG_FILE = "$env:USERPROFILE\pro_recon_install.log"
Start-Transcript -Path $LOG_FILE -Append | Out-Null

# =========================
# SCRIPT PATHS
# =========================
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

$GO_SETUP_SCRIPT      = Join-Path $SCRIPT_DIR "go_setup.ps1"
$PYTHON_SETUP_SCRIPT  = Join-Path $SCRIPT_DIR "python_setup.ps1"
$ENV_SETUP_SCRIPT     = Join-Path $SCRIPT_DIR "env_setup.ps1"
$TOOLS_INSTALL_SCRIPT = Join-Path $SCRIPT_DIR "tools_installer.ps1"

# =========================
# HELPER FUNCTIONS
# =========================
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-OK { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

# =========================
# ADMIN CHECK
# =========================
Write-Info "Checking Administrator privileges..."

$isAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Err "Run PowerShell as Administrator"
    Stop-Transcript | Out-Null
    exit 1
}

Write-OK "Admin privileges confirmed"

# =========================
# VALIDATE FILES
# =========================
Write-Info "Validating installer modules..."

$files = @(
    $GO_SETUP_SCRIPT,
    $PYTHON_SETUP_SCRIPT,
    $ENV_SETUP_SCRIPT,
    $TOOLS_INSTALL_SCRIPT
)

foreach ($f in $files) {
    if (-not (Test-Path $f)) {
        Write-Err "Missing file: $f"
        Stop-Transcript | Out-Null
        exit 1
    }
}

Write-OK "All modules found"

# =========================
# EXECUTOR FUNCTION
# =========================
function Run-Step {
    param(
        [string]$Name,
        [string]$Path
    )

    Write-Host ""
    Write-Host "===================================================" -ForegroundColor Cyan
    Write-Host " $Name" -ForegroundColor Yellow
    Write-Host "===================================================" -ForegroundColor Cyan
    Write-Host ""

    try {
        powershell.exe -ExecutionPolicy Bypass -File $Path

        if ($LASTEXITCODE -eq 0) {
            Write-OK "$Name completed"
        } else {
            Write-Warn "$Name finished with exit code $LASTEXITCODE"
        }
    }
    catch {
        Write-Err "$Name failed"
        Write-Host $_.Exception.Message -ForegroundColor Red
        Stop-Transcript | Out-Null
        exit 1
    }
}

# =========================
# INSTALLATION FLOW
# =========================
Run-Step "GO SETUP" $GO_SETUP_SCRIPT
Run-Step "PYTHON SETUP" $PYTHON_SETUP_SCRIPT
Run-Step "ENVIRONMENT CONFIGURATION" $ENV_SETUP_SCRIPT
Run-Step "TOOLS INSTALLATION" $TOOLS_INSTALL_SCRIPT

# =========================
# REFRESH ENV (IMPORTANT FIX)
# =========================
Write-Info "Refreshing environment variables..."

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path","User")

Write-OK "Environment refreshed"

# =========================
# OPTIONAL CHECK (WINGET / CHOCOLATEY)
# =========================
Write-Info "Checking package managers..."

if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-OK "Winget available"
} else {
    Write-Warn "Winget not found (optional)"
}

if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-OK "Chocolatey available"
} else {
    Write-Warn "Chocolatey not found (optional)"
}

# =========================
# FINAL OUTPUT
# =========================
Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "      PRO RECON ENGINE INSTALL COMPLETE" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Installed Stack:" -ForegroundColor Yellow
Write-Host " - Go Recon Tools"
Write-Host " - Python Recon Tools"
Write-Host " - Environment Config"
Write-Host " - Recon Toolchain"

Write-Host ""
Write-Host "Next Step:" -ForegroundColor Cyan
Write-Host "  recon -d example.com"
Write-Host ""

Write-Host "Log File:"
Write-Host "  $LOG_FILE"

Stop-Transcript | Out-Null

exit 0