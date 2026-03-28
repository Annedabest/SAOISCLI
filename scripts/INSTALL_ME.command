#!/bin/bash
# SAOIS CLI - Double-Click Installer for macOS
# Just double-click this file to install SAOIS!

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

clear
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   ⚡ SAOIS CLI - One-Click Installer ⚡                      ║"
echo "║                                                              ║"
echo "║   Smart AI Project Manager                                   ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🔍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ Python 3 not found!"
    echo ""
    echo "Please install Python first:"
    echo "  1. Go to https://python.org/downloads"
    echo "  2. Download Python 3.9 or newer"
    echo "  3. Install it"
    echo "  4. Double-click this file again"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found: $PYTHON_VERSION"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
cd "$SCRIPT_DIR"
python3 -m pip install --user -q rich 2>/dev/null
echo "✓ Dependencies installed"
echo ""

# Install SAOIS package
echo "🚀 Installing SAOIS package..."
python3 -m pip install --user -e . 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ SAOIS package installed"
else
    echo "⚠️  Package installation had issues, continuing..."
fi
echo ""

# Create symlink for direct access
echo "� Creating command symlink..."
mkdir -p /usr/local/bin 2>/dev/null
ln -sf "$SCRIPT_DIR/saois-cli" /usr/local/bin/saois 2>/dev/null

if [ -L /usr/local/bin/saois ]; then
    echo "✓ Command symlink created"
else
    echo "⚠️  Could not create /usr/local/bin/saois (may need sudo)"
    echo "   Using alias instead..."
    echo "Add this to your shell config: alias saois='python3 -m saois.simple_cli'"
fi
echo ""

# Verify installation
echo "✅ Verifying installation..."
if command -v saois &> /dev/null; then
    echo "✓ SAOIS is ready to use!"
    echo "   Type: saois help"
else
    echo "⚠️  SAOIS not yet available"
    echo "   Try: source ~/.zshrc"
fi

# Success
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✅ INSTALLATION COMPLETE!"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "   1. Close this window"
echo ""
echo "   2. Open a NEW Terminal window"
echo "      (Press Cmd+Space, type 'Terminal', press Enter)"
echo ""
echo "   3. Type: saois quickstart"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
read -p "Press Enter to close this window..."
