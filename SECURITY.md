# 🔒 SAOIS CLI - Security Guidelines

## Overview

SAOIS CLI is designed with security in mind, but as a tool that manages projects and executes commands, it's important to understand its security model and best practices.

## Security Model

### What SAOIS Does

1. **File System Access**: SAOIS reads and writes to:
   - `~/.saois/` - Configuration and project registry
   - Project directories you explicitly add
   - `docs/project_brain.md` files in your projects

2. **Command Execution**: SAOIS can execute:
   - Docker commands (`docker-compose up`, etc.)
   - Package manager commands (`npm install`, `pip install`, etc.)
   - Git commands (for GitHub integration)
   - System commands to open applications

3. **Network Access**: SAOIS may:
   - Clone repositories from GitHub
   - Open URLs in your browser
   - Check if Docker daemon is running

### What SAOIS Does NOT Do

- ❌ Does not send data to external servers
- ❌ Does not modify files outside your project directories
- ❌ Does not execute commands without your permission
- ❌ Does not access your API keys (only displays masked versions)
- ❌ Does not install system packages without confirmation

## Security Best Practices

### 1. **Review Before Execution**

SAOIS shows you commands before running them. Always review:
- Docker commands
- Dependency installations
- Git clone operations

### 2. **Project Isolation**

- Keep projects in dedicated folders
- Use the `AI_PROJECTS` folder for organization
- Don't add system directories as projects

### 3. **API Key Safety**

- SAOIS masks API keys when displaying them
- Keys are never sent anywhere
- Store sensitive keys in `.env` files (gitignored)

### 4. **Dependency Management**

When SAOIS offers to install dependencies:
- Review what's being installed
- Use official package managers (npm, pip, homebrew)
- Check project `package.json` and `requirements.txt` first

### 5. **GitHub Integration**

When cloning repositories:
- Only clone from trusted sources
- Review the repository before cloning
- Clone to your `AI_PROJECTS` folder, not system directories

## Permissions & Access Control

### File Permissions

SAOIS respects your file system permissions:
- Cannot write to protected directories without sudo
- Cannot modify files you don't own
- Follows standard Unix permissions

### Command Execution

All potentially destructive commands require confirmation:
- Installing packages
- Removing projects from registry
- Archiving projects
- Running Docker containers

## Data Privacy

### What's Stored Locally

- `~/.saois/projects.json` - Project paths and names
- `~/.saois/settings.json` - Your configuration (AI_PROJECTS path)
- `~/.saois/*_errors.txt` - Error logs (opt-in only)
- `~/.saois/archived_projects/` - Archived project references

### No Telemetry

SAOIS does **not**:
- Send usage data
- Track your activity
- Phone home
- Require internet connection (except for GitHub cloning)

## Sandboxing Recommendations

For maximum security, consider:

### 1. **Use a Dedicated User Account**

```bash
# Create a dedicated user for AI development
sudo dscl . -create /Users/aidev
sudo dscl . -create /Users/aidev UserShell /bin/zsh
```

### 2. **Run in a Container** (Advanced)

```bash
# Run SAOIS in a Docker container
docker run -it -v ~/AI_PROJECTS:/projects python:3.9 bash
# Install SAOIS inside container
```

### 3. **Use macOS App Sandbox** (Future)

We're exploring macOS sandboxing for future versions.

## Vulnerability Reporting

If you discover a security issue:

1. **Do NOT** open a public issue
2. Email: security@saois.dev (if available)
3. Or create a private security advisory on GitHub

## Audit Trail

SAOIS maintains an audit trail:
- All project additions/removals
- Error logs (opt-in)
- Validation history

Review these files periodically:
```bash
ls -la ~/.saois/
cat ~/.saois/validation_log.txt
```

## Secure Configuration

### Recommended `.zshrc` Setup

```bash
# SAOIS CLI - Secure setup
alias saois='python3 -m saois.cli'

# Optional: Restrict SAOIS to specific folder
export SAOIS_PROJECTS_ROOT="/Volumes/AI-DATA/AI_PROJECTS"
```

### Environment Variables

SAOIS respects these environment variables:
- `EDITOR` - For editing templates
- `PAGER` - For viewing logs

## Third-Party Dependencies

SAOIS uses these trusted libraries:
- `rich` - Terminal UI (no network access)
- `pathlib` - File system operations (Python stdlib)
- `subprocess` - Command execution (Python stdlib)

All dependencies are pinned in `requirements.txt`.

## Regular Security Checks

Run these commands periodically:

```bash
# Check what projects are registered
saois list

# Validate all project paths
saois validate

# Review configuration
cat ~/.saois/settings.json

# Check for unexpected files
ls -la ~/.saois/
```

## Incident Response

If you suspect SAOIS has been compromised:

1. **Stop using it immediately**
2. **Review recent commands**: Check shell history
3. **Inspect configuration**: `cat ~/.saois/projects.json`
4. **Remove if needed**: `saois uninstall`
5. **Report the issue**

## Future Security Enhancements

Planned improvements:
- [ ] GPG signing of releases
- [ ] Checksum verification
- [ ] Sandboxed execution mode
- [ ] Audit log encryption
- [ ] Two-factor confirmation for destructive actions

## Compliance

SAOIS is designed to be compliant with:
- GDPR (no personal data collection)
- SOC 2 principles (if used in enterprise)
- OWASP Top 10 (secure coding practices)

## Questions?

For security questions:
- Check documentation: `saois help`
- Review code: All code is open source
- Ask the community: GitHub Discussions

---

**Remember**: SAOIS is a tool. Your security depends on how you use it. Always review commands before execution and keep your system updated.

**Last Updated**: March 2026
**Version**: 1.0.0
