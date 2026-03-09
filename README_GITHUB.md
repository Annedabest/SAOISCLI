# ⚡ SAOIS CLI - Smart AI-Optimized Intelligence System

> **Your AI Development Operating System** - Automatically routes tasks to the right AI tool, manages projects across devices, and streamlines your entire development workflow.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/yourusername/SAOISCLI)

---

## 🎯 What is SAOIS?

SAOIS CLI is an intelligent project management system that:
- 🤖 **Auto-launches the right AI tool** based on your task (coding → Windsurf, research → Perplexity, etc.)
- 📁 **Manages all your projects** in one place across any device
- 🚀 **Runs projects with one command** - handles Docker, npm, pip, and more
- 🔍 **Validates and fixes** broken project paths
- 🐙 **Clones from GitHub** and adds to your registry automatically
- 🔒 **Secure by design** - no telemetry, no data collection

**Perfect for**: Developers juggling multiple projects, AI-assisted development, teams working across devices, ADHD-friendly workflows.

---

## ✨ Key Features

### 🤖 AI Tool Routing
```bash
saois run myproject
# Reads docs/project_brain.md
# Detects task type: "coding"
# Launches: Windsurf IDE automatically
```

### 📦 Smart Project Management
- **Selective Import**: Choose exactly which projects to import (no more all-or-nothing)
- **GitHub Integration**: Clone repos directly into your registry
- **Bulk Validation**: Fix 35 missing paths in one action
- **Custom Run Commands**: Define project-specific commands in project brain

### 🐳 Intelligent Execution
- **Dependency Detection**: Checks for Docker, npm, pip, etc. before running
- **Auto-Installation**: Offers to install missing tools via Homebrew
- **Error Simplification**: Translates cryptic errors into plain English
- **AI Fix Prompts**: Generates ready-to-use prompts for debugging

### 🔒 Security First
- ✅ No telemetry or data collection
- ✅ All commands require confirmation
- ✅ Opt-in error logging
- ✅ Open source and auditable
- ✅ Comprehensive security documentation

---

## 🚀 Installation

### macOS / Linux (One-Line Install)

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/SAOISCLI/main/install.sh | bash
```

Or manually:
```bash
git clone https://github.com/yourusername/SAOISCLI.git ~/.saois-cli
cd ~/.saois-cli
pip3 install -r requirements.txt
./install.sh
source ~/.zshrc  # or ~/.bashrc
```

### Windows (PowerShell)

```powershell
# Run as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
Invoke-WebRequest -Uri https://raw.githubusercontent.com/yourusername/SAOISCLI/main/install.ps1 -OutFile install.ps1
.\install.ps1
```

Or manually:
```powershell
git clone https://github.com/yourusername/SAOISCLI.git $env:USERPROFILE\SAOIS
cd $env:USERPROFILE\SAOIS
python -m pip install -r requirements.txt
# Add to PowerShell profile (see install.ps1)
```

### Verify Installation

```bash
saois help
saois doctor  # Check system health
saois setup   # Interactive setup wizard
```

---

## 📖 Quick Start Guide

### 1. First-Time Setup

```bash
# Run the setup wizard
saois setup

# This will:
# - Configure your AI_PROJECTS folder
# - Detect installed AI tools
# - Show you how task routing works
```

### 2. Import Your Projects

**Option A: From a folder (selective)**
```bash
saois import
# Choose: folder
# Enter path: /Volumes/AI-DATA/
# Import mode: select
# Projects: 1,3,5-8,12  ← Pick exactly what you want
```

**Option B: Clone from GitHub**
```bash
saois import
# Choose: github
# Enter URL: https://github.com/facebook/react
# Auto-clones to AI_PROJECTS and registers
```

### 3. Create Project Brains

```bash
# Bulk create for all projects
saois init-brains

# Or manually create docs/project_brain.md in each project
# Template: docs/project_brain_template.md
```

### 4. Start Working

```bash
# Auto-launch the right AI tool
saois run myproject

# Or run the project locally
saois docker myproject
```

---

## 📋 All Commands

| Command | Description | Example |
|---------|-------------|---------|
| `quickstart` | Interactive setup guide | `saois quickstart` |
| `setup` | Configure AI projects folder | `saois setup` |
| `list` | Show all registered projects | `saois list` |
| `add <name> <path>` | Add a single project | `saois add myapp ~/projects/myapp` |
| `import` | Bulk import (folder or GitHub) | `saois import` |
| `validate` | Validate & fix project paths | `saois validate` |
| `init-brains` | Create project brains for all | `saois init-brains` |
| `status <name>` | Show project details | `saois status myapp` |
| `run <name>` | Launch AI tool for project | `saois run myapp` |
| `docker <name>` | Start project locally | `saois docker myapp` |
| `keys <name>` | Extract API keys | `saois keys myapp` |
| `doctor` | Check installed AI tools | `saois doctor` |
| `open <name>` | Open project folder | `saois open myapp` |
| `remove <name>` | Remove a project | `saois remove myapp` |
| `install` | Install SAOIS globally | `saois install` |
| `uninstall` | Uninstall SAOIS | `saois uninstall` |
| `help` | Show this help | `saois help` |

---

## 🧠 Project Brain System

The **project brain** (`docs/project_brain.md`) is the heart of SAOIS. It tells the CLI:
- What your project does
- What task you're working on
- Which AI tool to launch
- **Custom run commands** (new!)

### Example Project Brain

```markdown
PROJECT NAME:
MyAwesomeApp

MISSION:
A React-based dashboard for analytics

CURRENT STATUS:
MVP complete, adding authentication

ARCHITECTURE SUMMARY:
React + TypeScript, Node.js backend, PostgreSQL

KNOWN ISSUES:
- Login redirect broken
- API rate limiting needed

RUN COMMANDS:
npm run dev

NEXT TASK TYPE:
coding

NEXT TASK:
1. Implement JWT authentication in backend
2. Add login/logout endpoints
3. Create protected route middleware
4. Write unit tests for auth flow
5. Update frontend to use auth tokens
6. Test end-to-end login flow
```

**Why detailed tasks?** AI tools can complete the entire task in one session, saving you tokens and time!

---

## 🎨 Usage Examples

### Selective Import
```bash
$ saois import
Import from? [folder/github]: folder
Enter folder path: /Volumes/AI-DATA/
✓ Found 34 projects (AI_PROJECTS excluded)

  1. PastoralCoaching
  2. FairFinance
  3. PhotoEditorV2
  ...
  34. Pics Keys

Import mode? [all/select/cancel]: select
Projects: 1-5,12,20
✓ Imported 7 new projects!
```

### Bulk Validation
```bash
$ saois validate
Checking 35 projects...
⚠️  10 projects have missing paths

Handle 10 missing projects? [one-by-one/archive-all/remove-all/skip-all]: archive-all
✓ Archived 10 projects
Location: ~/.saois/archived_projects/projects.json
```

### Custom Run Commands
```bash
$ saois docker SAOISCLI
🚀 Starting Project - SAOISCLI
📋 Custom command from project brain:
  python3 -m saois.cli help

Run this command? [y/n]: y
✓ Command executed successfully!
```

### AI Tool Installation
```bash
$ saois doctor
🔧 SAOIS Doctor - Checking AI Tools

Installed Tools:
┌────────────┬─────────────┬────────────────────────┐
│ Tool       │   Status    │ Used For               │
├────────────┼─────────────┼────────────────────────┤
│ Windsurf   │ ✓ Installed │ coding, debugging      │
│ Claude     │ ✗ Not found │ architecture, planning │
└────────────┴─────────────┴────────────────────────┘

Would you like help installing missing tools? [y/n]: y

Claude
  architecture, planning
  Install method? [browser/skip]: browser
  Opening https://claude.ai/code...
```

---

## 🔧 Configuration

### AI Projects Folder

Default: `~/Documents/AI_PROJECTS`

Change it:
```bash
saois setup
# Choose to change folder
# Enter new path: /Volumes/AI-DATA/AI_PROJECTS
```

Stored in: `~/.saois/settings.json`

### Project Registry

All registered projects: `~/.saois/projects.json`

```json
{
  "myproject": "/path/to/myproject",
  "another": "/path/to/another"
}
```

### Archived Projects

Missing projects can be archived: `~/.saois/archived_projects/projects.json`

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**: `saois help`, `saois doctor`, etc.
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/yourusername/SAOISCLI.git
cd SAOISCLI
pip3 install -r requirements.txt
python3 -m saois.cli help  # Test it works
```

---

## 🐛 Troubleshooting

### Command not found: saois

**macOS/Linux:**
```bash
source ~/.zshrc  # or ~/.bashrc
```

**Windows:**
```powershell
. $PROFILE
```

### Python not found

**macOS:**
```bash
brew install python
```

**Linux:**
```bash
sudo apt install python3 python3-pip
```

**Windows:**
Download from [python.org](https://python.org)

### Doctor says tools not installed, but they are

Make sure apps are in `/Applications` (macOS) or system PATH. Re-run:
```bash
saois doctor
```

### Import fails with "No projects found"

Check the folder path and ensure it contains subdirectories with projects.

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[SECURITY.md](SECURITY.md)** - Security model and best practices
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Changelog and new features
- **[FEATURES.md](FEATURES.md)** - Detailed feature documentation

---

## 🔒 Security

SAOIS is designed with security in mind:

- ✅ **No telemetry** - Zero data collection
- ✅ **No external requests** - Except GitHub cloning (opt-in)
- ✅ **Opt-in error logging** - You control what's saved
- ✅ **Command confirmation** - All destructive actions require approval
- ✅ **Open source** - Fully auditable code

Read our full [Security Policy](SECURITY.md).

---

## 📊 System Requirements

- **Python**: 3.9 or higher
- **OS**: macOS, Linux, or Windows
- **Dependencies**: Listed in `requirements.txt`
  - `rich` - Terminal UI
  - Standard library only (pathlib, subprocess, json, etc.)

---

## 🎯 Roadmap

- [ ] Multi-select with checkboxes (TUI)
- [ ] Project templates
- [ ] Automated project brain generation via AI
- [ ] Integration with more AI tools (Cursor, Copilot, etc.)
- [ ] Team collaboration features
- [ ] Cloud sync (opt-in)
- [ ] VS Code extension

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- Python standard library
- Love for developer productivity

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/SAOISCLI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/SAOISCLI/discussions)
- **Email**: support@saois.dev (if available)

---

## ⭐ Star History

If SAOIS helps you, consider giving it a star! ⭐

---

**Made with ❤️ for developers who want to focus on building, not managing.**
