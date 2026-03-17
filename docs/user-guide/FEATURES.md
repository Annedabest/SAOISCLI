# 🌟 SAOIS CLI - Feature Guide

## Core Features

### 📋 Project Management
- **List Projects**: View all registered projects in a clean table
- **Add Projects**: Register projects one at a time
- **Bulk Import**: Scan entire folders and import all subdirectories
- **Remove Projects**: Safely remove projects with confirmation

### 🐳 Docker Integration (NEW!)

Run your projects locally with one command:

```bash
saois docker myapp
```

**What it does:**
1. Checks for `docker-compose.yml` or `Dockerfile`
2. Runs `docker-compose up -d` automatically
3. Extracts the port from docker-compose.yml
4. Shows you the local URL (e.g., `http://localhost:3000`)
5. Tells you how to stop the containers

**Perfect for:**
- Quickly testing projects locally
- Starting development environments
- Running microservices
- Testing before deployment

### 🔑 API Key Extraction (NEW!)

Extract API keys and secrets from your projects:

```bash
saois keys myapp
```

**What it scans:**
- `.env`
- `.env.local`
- `.env.production`
- `config.json`
- `config.yaml`

**What it finds:**
- API_KEY patterns
- SECRET patterns
- TOKEN patterns
- DATABASE_URL
- Any environment variables

**Security:**
- Keys are masked (shows first 4 and last 4 characters)
- Never stores keys, only displays them
- Helps you quickly see what credentials a project needs

### 📊 Enhanced Status (NEW!)

Get detailed project information:

```bash
saois status myapp
```

**Shows:**
- Project location and existence
- Detected project type (Node.js, Python, Rust, Go)
- Available configuration files
- Docker support status
- Environment variable files
- README and documentation
- Quick action suggestions

**Example output:**
```
📊 Project Status - myapp

📁 Location: /Users/anne/projects/myapp
✓ Exists: Yes

Files Found:
  ✓ 📦 Node.js project
  ✓ 🐳 Docker Compose
  ✓ 🔑 Environment variables
  ✓ 📖 README

Quick Actions:
  • Start with Docker: saois docker myapp
  • View API keys: saois keys myapp
  • Open folder: saois open myapp
```

### ❓ Built-in Help

Never forget a command:

```bash
saois help
```

Shows a complete table of all commands with examples.

## Use Cases

### 🎯 For Developers
- Quickly start any project with Docker
- Find API keys needed for external integrations
- Manage multiple projects across different folders
- See project details at a glance

### 🏢 For Teams
- Share project registry across team members
- Standardize local development setup
- Document project requirements
- Quick onboarding for new developers

### 🚀 For DevOps
- Test Docker configurations locally
- Verify environment variables
- Check project structure
- Validate deployment readiness

## Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `list` | Show all projects | `saois list` |
| `add` | Add a project | `saois add myapp ~/projects/myapp` |
| `import` | Bulk import | `saois import` |
| `status` | Project details | `saois status myapp` |
| `docker` | Start with Docker | `saois docker myapp` |
| `keys` | Extract API keys | `saois keys myapp` |
| `open` | Open folder | `saois open myapp` |
| `remove` | Remove project | `saois remove myapp` |
| `help` | Show help | `saois help` |

## Tips & Tricks

### Quick Docker Testing
```bash
# Add a project
saois add webapp ~/projects/webapp

# Check if it has Docker
saois status webapp

# Start it locally
saois docker webapp

# View at http://localhost:3000
```

### API Key Management
```bash
# Extract keys from a project
saois keys myapp

# Copy them to your clipboard
# Use them for external API testing
```

### Bulk Project Setup
```bash
# Import all projects from a folder
saois import
# Enter: ~/projects

# Now all projects are registered
saois list
```
