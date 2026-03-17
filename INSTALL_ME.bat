@echo off
title SAOIS - One-Click Installer
color 0B

echo.
echo   ========================================
echo   SAOIS - AI Development Assistant
echo   ========================================
echo   One-Click Installation
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Python not found!
    echo.
    echo   Please install Python 3.9+ from:
    echo   https://python.org/downloads
    echo.
    echo   IMPORTANT: Check "Add Python to PATH" during install!
    echo.
    start https://python.org/downloads
    pause
    exit /b 1
)

echo   [OK] Python found
echo.

:: Get the directory where this script is located
cd /d "%~dp0"

echo   Installing SAOIS...
echo.

:: Uninstall old version first
pip uninstall saois -y >nul 2>&1

:: Install rich library
python -m pip install rich --quiet 2>nul

:: Install the package (fresh install)
python -m pip install -e . --quiet 2>nul

echo   [OK] Installation complete!
echo.

:: Add to PATH for this session
set PATH=%~dp0;%PATH%

echo   ========================================
echo   SAOIS is ready!
echo   ========================================
echo.
echo   Starting SAOIS setup...
echo.

:: Run the setup
python -m saois.simple_cli start

echo.
echo   ========================================
echo   To use SAOIS anywhere:
echo   ========================================
echo.
echo   Just type: saois [command]
echo.
echo   Commands: start, work, list, add, tools, help
echo.
echo   Example: saois work myproject
echo.
pause
