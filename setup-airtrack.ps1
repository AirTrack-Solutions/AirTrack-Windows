# AirTrack 1.0.0 'Wilbur'
# Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
# SPDX-License-Identifier: LicenseRef-AirTrack-Proprietary-NC
#
# Windows setup script — run as Administrator via PowerShell.
# Downloads and installs AirTrack Windows from GitHub.
#
# Usage (paste into an elevated PowerShell window):
#   irm https://raw.githubusercontent.com/Subhuti/AirTrack-Windows/main/setup-airtrack.ps1 | iex

$ErrorActionPreference = "Stop"

$repo        = "https://github.com/Subhuti/AirTrack-Windows.git"
$installDir  = Join-Path $env:USERPROFILE "docker\AirTrack-Windows"
$compose     = "docker-compose.windows.yml"

Write-Host ""
Write-Host "  ============================================"
Write-Host "   AirTrack 1.0.0 'Wilbur' — Windows Setup  "
Write-Host "  ============================================"
Write-Host ""

# ── Admin check ───────────────────────────────────────────────────────────────
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "  ERROR: Please run this script as Administrator."
    Write-Host "  Right-click PowerShell and choose 'Run as administrator'."
    Pause
    exit 1
}

# ── Git check ─────────────────────────────────────────────────────────────────
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "  ERROR: Git is not installed."
    Write-Host "  Download it from: https://git-scm.com/download/win"
    Write-Host "  After installing Git, run this script again."
    Pause
    exit 1
}

# ── Docker check ──────────────────────────────────────────────────────────────
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "  ERROR: Docker Desktop is not installed."
    Write-Host "  Download it from: https://www.docker.com/products/docker-desktop/"
    Write-Host "  After installing Docker Desktop, run this script again."
    Pause
    exit 1
}

docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Docker Desktop is not running."
    Write-Host "  Please start Docker Desktop and wait for it to finish loading,"
    Write-Host "  then run this script again."
    Pause
    exit 1
}

# ── Clone or update ───────────────────────────────────────────────────────────
if (Test-Path (Join-Path $installDir ".git")) {
    Write-Host "  Existing installation found. Updating..."
    Set-Location $installDir
    git pull
} else {
    if (Test-Path $installDir) {
        $choice = Read-Host "  Folder already exists. Delete and reinstall? (Y/N)"
        if ($choice -ne "Y") { Write-Host "  Install aborted."; exit 0 }
        Remove-Item -Recurse -Force $installDir
    }
    Write-Host "  Cloning AirTrack..."
    git clone $repo $installDir
    Set-Location $installDir
}

# ── Generate .env (first install only) ───────────────────────────────────────
$envFile = Join-Path $installDir ".env"
if (-not (Test-Path $envFile)) {
    $secret     = ([System.Guid]::NewGuid().ToString("N") + [System.Guid]::NewGuid().ToString("N")).ToUpper()
    $dbPassword = [System.Guid]::NewGuid().ToString("N").Substring(0, 16)
    $dbRootPass = [System.Guid]::NewGuid().ToString("N").Substring(0, 16)

    @"
# AirTrack Windows — generated $(Get-Date -f 'yyyy-MM-dd HH:mm:ss')
# Do NOT share or commit this file.

AIRTRACK_ROLE=client
AIRTRACK_UPDATE_MODE=remote
AIRTRACK_FORCE_PUSH=0
AIRTRACK_SYNC_USER=

SECRET_KEY=$secret

DB_HOST=airtrack-db
DB_USER=airtrack
DB_PASSWORD=$dbPassword
DB_ROOT_PASSWORD=$dbRootPass
DB_NAME=airtrack

AIRTRACK_APP_DIR=/app
AIRTRACK_STATIC_DIR=/app/static
AIRTRACK_UPDATES_DIR=/app/static/updates
AIRTRACK_LOG_FILE=/app/logs/file_sync.log
AIRTRACK_BACKUP_DIR=/app/backups
AIRTRACK_MAX_ARCHIVES=7
"@ | Out-File -FilePath $envFile -Encoding UTF8 -NoNewline
    Write-Host "  Created .env with secure credentials."
} else {
    Write-Host "  Existing .env kept."
}

# ── Build and start ───────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  Building and starting AirTrack..."
Write-Host "  This may take several minutes the first time. Please be patient."
Write-Host ""

docker compose -f $compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  ERROR: Setup failed. Check that Docker Desktop is running and try again."
    Pause
    exit 1
}

# ── Firewall ──────────────────────────────────────────────────────────────────
try {
    netsh advfirewall firewall add rule name="AirTrack" dir=in action=allow protocol=TCP localport=5000 2>&1 | Out-Null
} catch {}

# ── Done ──────────────────────────────────────────────────────────────────────
Start-Sleep -Seconds 3
Start-Process "http://localhost:5000"

Write-Host ""
Write-Host "  ============================================"
Write-Host "   AirTrack is running!"
Write-Host "   Open your browser to: http://localhost:5000"
Write-Host ""
Write-Host "   To launch AirTrack in future:"
Write-Host "   Double-click start_airtrack.bat"
Write-Host "  ============================================"
Write-Host ""
Pause
