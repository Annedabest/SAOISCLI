# ⚡ SAOIS - Installation Guide

## One-Click Install (Easiest)

### Windows
1. Double-click `INSTALL_ME.bat`
2. Follow the prompts
3. Done! SAOIS will start automatically.

### macOS
1. Double-click `INSTALL_ME.command` (or run `./scripts/install.sh`)
2. Follow the prompts
3. Run `source ~/.zshrc` then `saois start`

---

## Manual Install

### Windows (PowerShell)
```powershell
cd path\to\SAOISCLI
.\scripts\install.ps1
```

Then run `saois start` to begin.

### macOS / Linux
```bash
cd path/to/SAOISCLI
./scripts/install.sh
source ~/.zshrc
saois start
```

**That's it!** The `saois start` command will guide you through everything else.

---

## What Happens During Install

1. ✓ Checks Python is installed
2. ✓ Installs SAOIS package
3. ✓ Adds `saois` command to your terminal
4. ✓ Ready to use!

---

## After Installation

Just run:
```bash
saois start
```

This will:
- Find your projects folder
- Import your projects automatically
- Check your AI tools
- Get you ready to work!

---

## 6 Commands to Know

| Command | What it does |
|---------|--------------|
| `saois start` | Quick setup (run first!) |
| `saois work <name>` | Start working on a project |
| `saois list` | See all your projects |
| `saois add <name> <path>` | Add a new project |
| `saois tools` | Check your AI tools |
| `saois help` | Show help |

---

## Troubleshooting

**"command not found: saois"**
- Restart your terminal
- Or run: `source ~/.zshrc` (Mac/Linux)

**"No module named saois"**
- Run: `pip install rich`

**"Python not found"**
- Install Python 3.9+ from https://python.org

---

## Uninstall

```bash
pip uninstall saois
```

Then remove the SAOIS lines from your shell config file.
