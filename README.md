# ⚡ SAOIS

**Your AI Development Assistant** - Work on any project with the right AI tool, automatically.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Annedabest/SAOISCLI/releases)
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

## 6 Commands You Need

| Command | What it does |
|---------|--------------|
| `saois start` | Quick setup (run this first!) |
| `saois work myapp` | Start working on a project |
| `saois list` | See all your projects |
| `saois add myapp ~/path` | Add a new project |
| `saois tools` | Check your AI tools |
| `saois help` | Show help |

**That's it.** Just 6 commands to remember.

## How It Works

1. **You run:** `saois work myproject`
2. **SAOIS:** Reads your project, figures out what you're working on
3. **SAOIS:** Launches the best AI tool (Windsurf for coding, Claude for planning, etc.)
4. **You:** Start working with full AI assistance

## Example Workflow

```bash
# First time setup (only once)
saois start

# Start working on a project
saois work my-website

# SAOIS opens Windsurf with your project ready!
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

**"No AI tools found"**
- SAOIS will open browser versions instead
- Install Windsurf or Cursor for best experience

## License

MIT License - Use freely!