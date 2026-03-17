#!/usr/bin/env python3
"""
SAOIS CLI - Simple Entry Point
The new simplified CLI with only 6 essential commands.
"""
import sys

def main():
    """Main entry point for SAOIS CLI."""
    from .commands.main import run_command
    run_command(sys.argv)

if __name__ == "__main__":
    main()
