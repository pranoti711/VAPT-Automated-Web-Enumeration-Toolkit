# =========================================
# PRO RECON ENGINE - GO SETUP (WINDOWS)
# =========================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# =========================
# CONFIG
# =========================
$GO_VERSION = "1.24.5"

$GO_URL = "https://go.dev/dl/go$GO_VERSION.windows-amd64.msi"

$TEMP_DIR = "$env:TEMP\vapt_go_setup"
$MSI_PATH = "$TEMP_DIR\go.msi"

$GO_INSTALL_PATH = "C:\Program Files\Go"
$GO_BIN = "$GO_INSTALL_PATH\bin"

$USER_GOPATH = "$env:USERPROFILE\go"
$USER_GO_BIN = "$USER_GOPATH\bin"

# =========================
# LOG HELPERS
# =========================
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function OK($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

# =========================
# CHECK IF GO EXISTS
# =========================
Info "Checking existing Go installation..."

function Test-Go {
    try {
        $null = Get-Command go -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

if (Test-Go) {
    OK "Go already installed"
    try { go version } catch {}
    exit 0
}

# =========================
# CREATE TEMP DIR
# =========================
if (!(Test-Path $TEMP_DIR)) {
    New-Item -ItemType Directory -Path $TEMP_DIR | Out-Null
}

# =========================
# DOWNLOAD INSTALLER
# =========================
Info "Downloading Go $GO_VERSION..."

try {
    Invoke-WebRequest -Uri $GO_URL -OutFile $MSI_PATH
    OK "Downloaded Go installer"
}
catch {
    Err "Download failed"
    exit 1
}

# =========================
# INSTALL GO SILENTLY
# =========================
Info "Installing Go..."

try {
    $proc = Start-Process msiexec.exe -Wait -PassThru -ArgumentList "/i `"$MSI_PATH`" /qn /norestart"

    if ($proc.ExitCode -ne 0) {
        Err "MSI install failed with code $($proc.ExitCode)"
        exit 1
    }

    OK "Go installed successfully"
}
catch {
    Err "Installation error"
    exit 1
}

# =========================
# WAIT FOR SYSTEM REG UPDATE
# =========================
Start-Sleep -Seconds 3

# =========================
# CONFIGURE GOPATH
# =========================
Info "Setting GOPATH..."

if (!(Test-Path $USER_GOPATH)) {
    New-Item -ItemType Directory -Path $USER_GOPATH | Out-Null
}

if (!(Test-Path $USER_GO_BIN)) {
    New-Item -ItemType Directory -Path $USER_GO_BIN | Out-Null
}

[Environment]::SetEnvironmentVariable("GOPATH", $USER_GOPATH, "User")
OK "GOPATH set"

# =========================
# FIX MACHINE PATH
# =========================
Info "Configuring PATH..."

$machinePath = [Environment]::GetEnvironmentVariable("Path","Machine")
$userPath = [Environment]::GetEnvironmentVariable("Path","User")

# Add Go system bin
if ($machinePath -notlike "*$GO_BIN*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$machinePath;$GO_BIN",
        "Machine"
    )
    OK "Added Go to Machine PATH"
}

# Add user GOPATH bin
if ($userPath -notlike "*$USER_GO_BIN*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$userPath;$USER_GO_BIN",
        "User"
    )
    OK "Added GOPATH to User PATH"
}

# =========================
# REFRESH CURRENT SESSION
# =========================
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path","User")

# =========================
# VERIFY GO
# =========================
Info "Verifying Go installation..."

$goPath = Get-Command go -ErrorAction SilentlyContinue

if ($goPath) {
    OK "Go is working"
    try { go version } catch {}
}
else {
    Err "Go not found in PATH"
    exit 1
}

# =========================
# CLEANUP
# =========================
Info "Cleaning temp files..."

Remove-Item -Recurse -Force $TEMP_DIR -ErrorAction SilentlyContinue

OK "Cleanup done"

# =========================
# FINAL OUTPUT
# =========================
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " GO SETUP COMPLETE (PRO READY)" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Go Version:"
try { go version } catch {}

Write-Host ""
Write-Host "Paths:"
Write-Host "  GOPATH: $USER_GOPATH"
Write-Host "  GO BIN: $GO_BIN"
Write-Host "  USER BIN: $USER_GO_BIN"
Write-Host ""

Write-Host "Ready for:"
Write-Host "  subfinder, httpx, nuclei, katana, gau"
Write-Host ""

exit 0