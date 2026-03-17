#!/bin/bash
# SAOIS - Simple Installation for macOS/Linux

set -e

echo ""
echo "  ⚡ SAOIS - AI Development Assistant"
echo "  One-click installation"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$(dirname "$SCRIPT_DIR")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  ❌ Python 3 not found"
    echo "  Please install Python 3.9+ first"
    exit 1
fi

echo "  ✓ $(python3 --version)"
echo "  ✓ Installing from: $INSTALL_DIR"

# Install package
echo ""
echo "  📦 Installing SAOIS..."
cd "$INSTALL_DIR"
python3 -m pip install -e . --quiet 2>/dev/null || python3 -m pip install . --quiet 2>/dev/null

# Detect shell config
SHELL_RC="$HOME/.zshrc"
if [ -f "$HOME/.bashrc" ] && [ ! -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

# Add alias
if ! grep -q "alias saois=" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# SAOIS CLI" >> "$SHELL_RC"
    echo "alias saois='python3 -m saois.simple_cli'" >> "$SHELL_RC"
    echo "  ✓ Added 'saois' command"
else
    echo "  ✓ 'saois' command ready"
fi

# Done!
echo ""
echo "  ✅ Installation complete!"
echo ""
echo "  ┌─────────────────────────────────────┐"
echo "  │  Next: Run these commands:          │"
echo "  │                                     │"
echo "  │    source $SHELL_RC"
echo "  │    saois start                      │"
echo "  │                                     │"
echo "  │  That's it! You're ready to go.    │"
echo "  └─────────────────────────────────────┘"
echo ""
