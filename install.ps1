# SAOIS CLI - Windows PowerShell Installation Script
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "🚀 SAOIS CLI - Installation for Windows" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Python not found. Please install Python 3.9+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green

# Clone repository
Write-Host ""
Write-Host "📦 Cloning SAOIS CLI..." -ForegroundColor Cyan
$installDir = "$env:USERPROFILE\SAOIS"

if (Test-Path $installDir) {
    Write-Host "⚠️  SAOIS already exists at $installDir" -ForegroundColor Yellow
    $overwrite = Read-Host "Overwrite? (y/n)"
    if ($overwrite -ne "y") {
        Write-Host "Installation cancelled" -ForegroundColor Yellow
        exit 0
    }
    Remove-Item -Recurse -Force $installDir
}

git clone https://github.com/yourusername/SAOISCLI.git $installDir
if (-not $?) {
    Write-Host "❌ Failed to clone repository" -ForegroundColor Red
    exit 1
}

Set-Location $installDir

# Install dependencies
Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (-not $?) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create alias in PowerShell profile
Write-Host ""
Write-Host "🔧 Setting up global command..." -ForegroundColor Cyan

$profilePath = $PROFILE.CurrentUserAllHosts
if (-not (Test-Path $profilePath)) {
    New-Item -Path $profilePath -Type File -Force | Out-Null
}

$aliasLine = "function saois { python `"$installDir\saois\cli.py`" @args }"

# Check if alias already exists
$profileContent = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
if ($profileContent -notlike "*function saois*") {
    Add-Content -Path $profilePath -Value "`n# SAOIS CLI`n$aliasLine"
    Write-Host "✓ Added 'saois' command to PowerShell profile" -ForegroundColor Green
} else {
    Write-Host "✓ 'saois' command already in profile" -ForegroundColor Green
}

# Success message
Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Restart PowerShell or run: . $profilePath" -ForegroundColor White
Write-Host "  2. Test: saois help" -ForegroundColor White
Write-Host "  3. Setup: saois setup" -ForegroundColor White
Write-Host ""
Write-Host "Documentation: https://github.com/yourusername/SAOISCLI" -ForegroundColor Cyan
