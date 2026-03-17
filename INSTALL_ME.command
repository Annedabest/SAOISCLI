#!/bin/bash
# SAOIS - One-Click Installer for macOS
# Double-click this file to install SAOIS

cd "$(dirname "$0")"

echo ""
echo "  ⚡ SAOIS - AI Development Assistant"
echo "  One-Click Installation"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  ❌ Python 3 not found"
    echo "  Please install Python 3.9+ first"
    echo ""
    echo "  Opening python.org..."
    open "https://python.org/downloads"
    read -p "  Press Enter after installing Python..."
    exit 1
fi

echo "  ✓ $(python3 --version)"
echo "  ✓ Location: $(pwd)"

# Install
echo ""
echo "  📦 Installing SAOIS..."

python3 -m pip install rich --quiet 2>/dev/null
python3 -m pip install -e . --quiet 2>/dev/null || python3 -m pip install . --quiet 2>/dev/null

echo "  ✓ Dependencies installed"

# Add to shell config
SHELL_RC="$HOME/.zshrc"
if [ -f "$HOME/.bashrc" ] && [ ! -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if ! grep -q "alias saois=" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# SAOIS CLI" >> "$SHELL_RC"
    echo "alias saois='python3 -m saois.simple_cli'" >> "$SHELL_RC"
    echo "  ✓ Added 'saois' command to $SHELL_RC"
else
    echo "  ✓ 'saois' command ready"
fi

# Load for current session
alias saois='python3 -m saois.simple_cli'

echo ""
echo "  ========================================"
echo "  ✅ Installation complete!"
echo "  ========================================"
echo ""
echo "  Starting SAOIS setup..."
echo ""

# Run setup
python3 -m saois.simple_cli start

echo ""
echo "  ========================================"
echo "  To use SAOIS in new terminals:"
echo "  ========================================"
echo ""
echo "  1. Close and reopen Terminal"
echo "  2. Or run: source $SHELL_RC"
echo "  3. Then type: saois help"
echo ""
read -p "  Press Enter to close..."
