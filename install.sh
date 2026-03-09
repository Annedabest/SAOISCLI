#!/bin/bash
# SAOIS CLI - Universal Installation Script for macOS/Linux
# Usage: curl -sSL https://raw.githubusercontent.com/yourusername/SAOISCLI/main/install.sh | bash

set -e

echo "🚀 SAOIS CLI - Installation"
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)     OS_TYPE="Linux";;
    Darwin*)    OS_TYPE="macOS";;
    *)          OS_TYPE="Unknown";;
esac

echo "📍 Detected: $OS_TYPE"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+ first."
    echo ""
    if [ "$OS_TYPE" = "macOS" ]; then
        echo "Install with: brew install python"
    else
        echo "Install with: sudo apt install python3 python3-pip"
    fi
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found: $PYTHON_VERSION"

# Clone or update repository
INSTALL_DIR="$HOME/.saois-cli"
echo ""
echo "📦 Installing to $INSTALL_DIR..."

if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  SAOIS already exists. Updating..."
    cd "$INSTALL_DIR"
    git pull
else
    git clone https://github.com/yourusername/SAOISCLI.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
python3 -m pip install --user -r requirements.txt

# Detect shell and add alias
echo ""
echo "🔧 Setting up global command..."

SHELL_RC=""
if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_RC="$HOME/.bash_profile"
else
    SHELL_RC="$HOME/.profile"
fi

ALIAS_LINE="alias saois='python3 -m saois.cli'"

if ! grep -q "alias saois=" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# SAOIS CLI" >> "$SHELL_RC"
    echo "export PYTHONPATH=\"$INSTALL_DIR:\$PYTHONPATH\"" >> "$SHELL_RC"
    echo "alias saois='cd $INSTALL_DIR && python3 -m saois.cli'" >> "$SHELL_RC"
    echo "✓ Added 'saois' command to $SHELL_RC"
else
    echo "✓ 'saois' command already configured"
fi

# Success message
echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Reload shell: source $SHELL_RC"
echo "  2. Test: saois help"
echo "  3. Setup: saois setup"
echo ""
echo "Documentation: https://github.com/yourusername/SAOISCLI"
