# ⚡ SAOIS

**Your AI Development Assistant** - Work on any project with the right AI tool, automatically.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Annedabest/SAOISCLI)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Website](https://img.shields.io/badge/website-saois.cli.victorconsultancy.cloud-cyan.svg)](https://saois.cli.victorconsultancy.cloud)

🌐 **Website:** [saois.cli.victorconsultancy.cloud](https://saois.cli.victorconsultancy.cloud)

## What is SAOIS?

SAOIS helps you work on projects with AI assistance. It automatically picks the best AI tool (Windsurf, Cursor, Claude, etc.) for your task and launches it with your project ready to go.

**No complex setup. No manual configuration. Just works.**

## Install (30 seconds)

### One-Click Install
- **Windows:** Double-click `INSTALL_ME.bat`
- **macOS:** Double-click `INSTALL_ME.command`

### Manual Install

**Windows (PowerShell):**
```powershell
cd path\to\SAOISCLI
.\scripts\install.ps1
saois start
```

**macOS / Linux:**
```bash
cd path/to/SAOISCLI
./scripts/install.sh
source ~/.zshrc
saois start
```

## Commands (start here, then shortcuts)

| Command | What it does |
|---------|--------------|
| `saois start` | Quick setup (run this first!) |
| `saois work myapp` | Open the best tool for your task (desktop app if detected, otherwise the tool’s website—see message) |
| `saois list` | See all your projects |
| `saois add myapp ~/path` | Add a new project |
| `saois tools` | Check your AI tools (`saois tools --verbose` shows what matched) |
| `saois prompts` | List or show built-in AI prompt templates |
| `saois suggest myapp` | Show brain-based next steps without launching a tool |
| `saois help` | Show this help |

The essentials are still **start → work → list**; the rest are optional power-user commands.

## How It Works

1. **You run:** `saois work myproject`
2. **SAOIS:** Reads your project, figures out what you're working on
3. **SAOIS:** Launches the best desktop AI tool when it can detect one; otherwise it opens the vendor site in your browser and says so explicitly.
4. **You:** Continue in the IDE or open the project folder from the path SAOIS prints.

## Example Workflow

```bash
# First time setup (only once)
saois start

# Start working on a project
saois work my-website

# If Windsurf (or Cursor/VS Code) is installed, SAOIS opens it with the folder; otherwise check the on-screen note (browser fallback).
```

## Verify install (developers)

Use the same Python you develop with (including **Xcode’s** `/usr/bin/python3` on macOS):

```bash
cd /path/to/SAOISCLI
python3 -m pip install -e ".[dev]"
python3 -m pytest tests/ -v
python3 -m pip wheel . -w /tmp/saois_wheel --no-deps   # wheel should contain saois/ and templates/, not tests/
```

## Features

- ✅ **Zero Config** - Works out of the box
- ✅ **Smart Routing** - Picks the right AI tool automatically
- ✅ **Auto-Discovery** - Finds your projects automatically
- ✅ **Cross-Platform** - Windows, macOS, Linux
- ✅ **Privacy First** - No data collection, everything local

## Supported AI Tools

| Tool | Best For |
|------|----------|
| **Windsurf** | Coding with AI |
| **Cursor** | AI-first editing |
| **VS Code** | General coding |
| **Claude** | Planning & architecture |
| **ChatGPT** | General AI help |
| **Perplexity** | Research & learning |

SAOIS automatically uses whatever you have installed.

## Documentation

- [Installation Guide](docs/user-guide/INSTALL.md)
- [Quick Start](docs/user-guide/QUICKSTART.md)
- [All Features](docs/user-guide/FEATURES.md)

## Troubleshooting

**"command not found: saois"**
- Restart your terminal
- Or run: `source ~/.zshrc`

**"No AI tools found" / `saois tools` shows 0/6**
- Run `saois tools --verbose` to see why each tool was skipped (path vs `PATH`)
- Install Windsurf, Cursor, or VS Code for desktop launches; without them, `saois work` still runs but may open vendor sites instead of an IDE

## License

MIT License - Use freely!