# ⚡ SAOIS CLI

A modern, user-friendly CLI for managing development projects across any device.

## Features

- 🎨 **Clean Modern UI** - Simple, colorful interface anyone can use
- ⚡ **Quick Setup** - One script to install globally
- 📁 **Bulk Import** - Scan folders and import all projects at once
- 🐳 **Docker Integration** - Start projects with one command, get local URLs
- 🔑 **API Key Extraction** - Find and display API keys from .env files
- 📊 **Smart Status** - Detects project type and shows relevant info
- 🚀 **Fast & Simple** - No complex commands, just works
- 💡 **Helpful Tips** - Guides you through every action
- ✓ **Smart Validation** - Confirms before destructive actions
- ❓ **Built-in Help** - `saois help` shows all commands

## Quick Start

### Option 1: Quick Install (Recommended)
```bash
cd /path/to/SAOISCLI
./install.sh
source ~/.zshrc
```

### Option 2: Manual Install
```bash
cd /path/to/SAOISCLI
pip3 install -e .
python3 -m saois.cli install
source ~/.zshrc
```

### Option 3: Temporary Use (No Install)
```bash
cd /path/to/SAOISCLI
source activate.sh
```

Now use `saois` from anywhere!

## Usage

### � View All Projects
```bash
saois list
```
Shows a clean table with all your projects, their locations, and status.

### ➕ Add a Single Project
```bash
saois add myapp ~/projects/myapp
```
Adds one project to your registry.

### 📁 Import Multiple Projects (NEW!)
```bash
saois import
```
Scans a folder and imports all subdirectories as projects. Perfect for:
- Importing all projects from `~/projects/`
- Bulk adding from a workspace folder
- Quick setup on a new device

### 📖 View Project Status
```bash
saois status myapp
```
Shows detailed project information:
- Location and existence check
- Detected project type (Node.js, Python, Rust, Go)
- Available files (Docker, .env, README, etc.)
- Quick action suggestions

### 🐳 Start Project with Docker
```bash
saois docker myapp
```
Automatically runs `docker-compose up -d` and shows the local URL:
- Detects docker-compose.yml or Dockerfile
- Starts containers in detached mode
- Extracts and displays the local URL (e.g., http://localhost:3000)
- Shows how to stop containers

### 🔑 Extract API Keys
```bash
saois keys myapp
```
Scans project for API keys and secrets:
- Searches .env, .env.local, .env.production, config files
- Finds API_KEY, SECRET, TOKEN, DATABASE_URL patterns
- Displays masked values for security (e.g., `abcd****xyz`)
- Lists which files contain keys

### 🚀 Open a Project
```bash
saois open myapp
```
Opens the project folder in Finder.

### 🗑️ Remove a Project
```bash
saois remove myapp
```
Removes a project from the registry (asks for confirmation).

### ❓ Get Help
```bash
saois help
```
Shows all available commands with examples.

### ⚙️ System Commands

**Install globally**
```bash
saois install
```

**Uninstall**
```bash
saois uninstall
```

## Configuration

Projects are stored in `~/.saois/projects.json`

Example:
```json
{
  "saois-builder": "/Users/anne/projects/saois-builder",
  "crypto-agent": "/Users/anne/projects/crypto-agent"
}
```

## UI Features

- **Clean Header** - Simple ⚡ SAOIS CLI ⚡ branding with rounded borders
- **Readable Tables** - Clear columns with proper spacing
- **Color Coding** - Cyan for names, green for success, red for errors, yellow for warnings
- **Status Icons** - ✓ Ready / ✗ Missing for quick visual feedback
- **Helpful Tips** - Context-sensitive guidance after each command
- **Confirmation Prompts** - Asks before deleting or making changes
- **Spinner Animations** - Smooth loading indicators
- **Numbered Lists** - Easy reference for projects
- **Rounded Boxes** - Modern, friendly panel styling
- **Smart Defaults** - Sensible default choices for prompts

## Device Portability

SAOIS can be installed on any device with Python 3.7+. Simply:
1. Copy the SAOISCLI folder to the new device
2. Run `pip3 install -e .` in the folder
3. Run `python3 -m saois.cli install`
4. Source your shell config

The CLI will have access to any project on your device - just register them with `saois add`!


# COMMANDS:
saois list
saois add <name> <path>
saois status <project>
saois open <project>
saois remove <name>
saois install
saois uninstall