#!/bin/bash

# Quick activation script for SAOIS CLI
# Run: source activate.sh

export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# Create alias for current session
alias saois='python3 -m saois.cli'

echo "✓ SAOIS activated for this session!"
echo ""
echo "To make it permanent, run:"
echo "  ./install.sh"
echo "  source ~/.zshrc"
