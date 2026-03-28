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

If a desktop IDE is installed, SAOIS launches it with your project folder. If not, it opens the tool’s website in your browser and tells you so—install the app for full one-click opens.

---

## All Commands

| Command | What it does |
|---------|--------------|
| `saois start` | Quick setup |
| `saois work <name>` | Start working (IDE or browser fallback) |
| `saois list` | See projects |
| `saois add <name> <path>` | Add project |
| `saois tools` | Check AI tools (`--verbose` shows detection) |
| `saois prompts` | List / show AI prompt templates |
| `saois suggest <name>` | Brain-based next steps only |
| `saois help` | Show help |

---

## Example Workflow

```bash
# First time only
saois start

# Every day
saois work my-website    # e.g. Windsurf / Cursor when installed
saois work research      # Perplexity / ChatGPT chain
saois work planning      # Claude / ChatGPT chain
```

---

## Troubleshooting

**"command not found"**
- Restart your terminal
- Or: `source ~/.zshrc`

**"No projects found"**
- Run: `saois add myapp ~/path/to/project`

**"AI tool not opening"**
- CLI will say if it opened the website instead of the app; use `saois tools --verbose` to see detection
- Install Windsurf/Cursor/VS Code for desktop launches
