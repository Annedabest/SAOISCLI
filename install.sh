#!/bin/bash

echo "⚡ Installing SAOIS CLI..."

# Install the package
pip3 install -e . || { echo "❌ Failed to install package"; exit 1; }

# Add alias to shell config
SHELL_RC="$HOME/.zshrc"
ALIAS_LINE="alias saois='python3 -m saois.cli'"

if ! grep -q "$ALIAS_LINE" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# SAOIS CLI" >> "$SHELL_RC"
    echo "$ALIAS_LINE" >> "$SHELL_RC"
    echo "✓ Added alias to $SHELL_RC"
else
    echo "✓ Alias already exists"
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Next step:"
echo "  source ~/.zshrc"
echo ""
echo "Then use 'saois' from anywhere!"
