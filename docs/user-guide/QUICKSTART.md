# 🚀 SAOIS - Quick Start

Get up and running in 60 seconds.

## Step 1: Install

**Windows:**
```powershell
cd path\to\SAOISCLI
.\scripts\install.ps1
# Restart PowerShell
```

**Mac/Linux:**
```bash
cd path/to/SAOISCLI
./scripts/install.sh
source ~/.zshrc
```

## Step 2: Setup

```bash
saois start
```

This does everything automatically:
- ✓ Finds your projects folder
- ✓ Imports your projects
- ✓ Checks your AI tools
- ✓ You're ready!

## Step 3: Work

```bash
saois work myproject
```

SAOIS opens the right AI tool for your task. That's it!

---

## All Commands

| Command | What it does |
|---------|--------------|
| `saois start` | Quick setup |
| `saois work <name>` | Start working |
| `saois list` | See projects |
| `saois add <name> <path>` | Add project |
| `saois tools` | Check AI tools |
| `saois help` | Show help |

---

## Example Workflow

```bash
# First time only
saois start

# Every day
saois work my-website    # Opens Windsurf
saois work research      # Opens Perplexity
saois work planning      # Opens Claude
```

---

## Troubleshooting

**"command not found"**
- Restart your terminal
- Or: `source ~/.zshrc`

**"No projects found"**
- Run: `saois add myapp ~/path/to/project`

**"AI tool not opening"**
- SAOIS will open browser version instead
- Install Windsurf/Cursor for best experience
