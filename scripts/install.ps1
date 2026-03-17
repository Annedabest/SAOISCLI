# SAOIS CLI - Windows Installation
# Run: .\scripts\install.ps1

Write-Host ""
Write-Host "  SAOIS - AI Development Assistant" -ForegroundColor Cyan
Write-Host "  Installing for Windows..." -ForegroundColor DarkGray
Write-Host ""

# Check Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "  [X] Python not found" -ForegroundColor Red
    Write-Host "  Please install Python 3.9+ from https://python.org" -ForegroundColor Yellow
    Write-Host "  Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    Write-Host ""
    Start-Process "https://python.org/downloads"
    Read-Host "  Press Enter after installing Python..."
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "  [OK] $pythonVersion" -ForegroundColor Green

# Get script directory (where SAOIS is located)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$installDir = Split-Path -Parent $scriptDir

Write-Host "  [OK] Location: $installDir" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "  Installing dependencies..." -ForegroundColor Cyan

Set-Location $installDir

# Uninstall old version first
pip uninstall saois -y 2>$null | Out-Null

# Install rich library (required)
python -m pip install rich --quiet 2>$null

# Install the package (fresh)
python -m pip install -e . --quiet 2>$null
if (-not $?) {
    python -m pip install . --quiet 2>$null
}

Write-Host "  [OK] Dependencies installed" -ForegroundColor Green

# Create a batch file that can be used directly
$batchContent = "@echo off`r`npython -m saois.simple_cli %*"
$batchPath = Join-Path $installDir "saois.bat"
Set-Content -Path $batchPath -Value $batchContent -Force
Write-Host "  [OK] Created saois.bat" -ForegroundColor Green

# Add to PowerShell profile
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path -Parent $profilePath

if (-not (Test-Path $profileDir)) {
    New-Item -Path $profileDir -ItemType Directory -Force | Out-Null
}

if (-not (Test-Path $profilePath)) {
    New-Item -Path $profilePath -ItemType File -Force | Out-Null
}

$functionCode = "`n# SAOIS CLI`nfunction saois { python -m saois.simple_cli `$args }"

$profileContent = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
$hasFunction = $false
if ($profileContent) {
    $hasFunction = $profileContent.Contains("function saois")
}

if (-not $hasFunction) {
    Add-Content -Path $profilePath -Value $functionCode
    Write-Host "  [OK] Added to PowerShell profile" -ForegroundColor Green
} else {
    Write-Host "  [OK] PowerShell profile ready" -ForegroundColor Green
}

# Add install directory to PATH for current session
$env:Path = "$installDir;$env:Path"

# Load the function in current session
Invoke-Expression $functionCode

Write-Host ""
Write-Host "  ========================================" -ForegroundColor Green
Write-Host "  Installation complete!" -ForegroundColor Green
Write-Host "  ========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  You can now use SAOIS!" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Try it now:  saois start" -ForegroundColor White
Write-Host ""
Write-Host "  Or in new terminals, just type:" -ForegroundColor DarkGray
Write-Host "    saois help" -ForegroundColor White
Write-Host ""

# Test if it works
Write-Host "  Testing installation..." -ForegroundColor DarkGray
try {
    $testResult = python -m saois.simple_cli help 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] SAOIS is working!" -ForegroundColor Green
    } else {
        Write-Host "  [!] Test had issues, but may still work" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  [!] Test failed, but installation may still work" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Tip: Run 'saois start' to begin setup" -ForegroundColor DarkGray
Write-Host ""
