# 🚀 SAOIS CLI - Complete Setup Guide

## What is SAOIS?

SAOIS is an **AI Development Operating System** - a CLI that automatically launches the right AI tool based on your project's current task.

Instead of manually opening tools, SAOIS reads your project's "brain" and opens:
- **Windsurf** for coding/debugging
- **Claude Code** for architecture/planning
- **Perplexity** for research
- **Sourcegraph Cody** for analysis
- **Continue.dev** for automation

## Quick Setup (5 Minutes)

### Step 1: Install SAOIS CLI

```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
./install.sh
source ~/.zshrc
```

### Step 2: Create AI_PROJECTS Folder

```bash
mkdir -p ~/Documents/AI_PROJECTS
```

This folder will contain all your AI projects.

### Step 3: Move Your Projects

Move or create projects inside `AI_PROJECTS`:

```bash
mv ~/projects/myapp ~/Documents/AI_PROJECTS/
```

SAOIS will auto-discover them!

### Step 4: Add Project Brain

For each project, create:

```bash
mkdir -p ~/Documents/AI_PROJECTS/myapp/docs
```

Create `docs/project_brain.md`:

```markdown
PROJECT NAME:
My Awesome App

MISSION:
Build a revolutionary AI-powered application

CURRENT STATUS:
Initial setup complete, starting core features

ARCHITECTURE SUMMARY:
React frontend + Node.js backend + PostgreSQL

KNOWN ISSUES:
- Authentication needs improvement
- API rate limiting not implemented

NEXT TASK TYPE:
coding

NEXT TASK:
Implement user authentication with JWT tokens
```

### Step 5: (Optional) Add AI Safety Rules

Create `.ai_rules.md` in project root:

```markdown
# AI RULES

Before coding:
1. Read docs/project_brain.md
2. Understand NEXT TASK

Rules:
- Only modify files related to the task
- Do not refactor the whole project
- Prefer small changes
- Maintain compatibility

Recommended Models:
- Simple tasks: GPT-4o-mini, Claude 3.5 Haiku
- Complex tasks: Claude 3.5 Sonnet, GPT-4o
- Debugging: Claude 3.5 Sonnet
```

## Daily Workflow

### 1. Check Your Projects

```bash
saois list
```

Shows all projects (from AI_PROJECTS + manually registered).

### 2. View Project Status

```bash
saois status myapp
```

Shows:
- Project brain summary
- Next task type
- Files detected
- Quick actions

### 3. Start Working

```bash
saois run myapp
```

SAOIS will:
1. Read `docs/project_brain.md`
2. See `NEXT TASK TYPE: coding`
3. Open **Windsurf IDE** automatically
4. You start coding immediately!

## Task Types & Tools

| Task Type | Tool | When to Use |
|-----------|------|-------------|
| `coding` | Windsurf | Writing new code |
| `debugging` | Windsurf | Fixing bugs |
| `architecture` | Claude Code | Designing systems |
| `research` | Perplexity | Finding information |
| `analysis` | Sourcegraph Cody | Understanding codebases |
| `automation` | Continue.dev | Automating workflows |
| `planning` | Claude Code | Project planning |

## Advanced Features

### Check Installed Tools

```bash
saois doctor
```

Shows which AI tools are installed and working.

### Docker Integration

```bash
saois docker myapp
```

Starts project with Docker and shows local URL.

### API Key Extraction

```bash
saois keys myapp
```

Finds and displays API keys from `.env` files (masked for security).

### Bulk Import

```bash
saois import
```

Scan a folder and import all projects at once.

## Project Structure Example

```
~/Documents/AI_PROJECTS/
├── myapp/
│   ├── .ai_rules.md          # AI safety rules
│   ├── docs/
│   │   └── project_brain.md  # Project brain
│   ├── src/
│   ├── package.json
│   └── README.md
├── another-project/
│   ├── .ai_rules.md
│   ├── docs/
│   │   └── project_brain.md
│   └── ...
```

## Tips for ADHD-Friendly Workflow

### 1. One Command to Start
```bash
saois run myapp
```
No decisions needed - SAOIS knows what to open.

### 2. Clear Next Steps
Project brain tells you exactly what to work on next.

### 3. Context Switching
```bash
saois run project1  # Work on project 1
saois run project2  # Switch to project 2
```

### 4. Visual Status
```bash
saois status myapp
```
See everything at a glance.

## Troubleshooting

### Command not found?
```bash
source ~/.zshrc
```

### Tool not opening?
```bash
saois doctor
```
Check which tools are installed.

### No project brain?
```bash
saois status myapp
```
SAOIS will show you the template to create one.

### Want to use browser instead?
SAOIS automatically falls back to browser if tools aren't installed.

## Model Recommendations (Save Credits!)

### Simple Tasks
- **GPT-4o-mini** - Fast, cheap, great for simple code
- **Claude 3.5 Haiku** - Excellent for quick fixes

### Complex Tasks
- **Claude 3.5 Sonnet** - Best for architecture and debugging
- **GPT-4o** - Great for complex logic

### Research
- **Perplexity Pro** - Latest information with sources

## Next Steps

1. ✅ Install SAOIS
2. ✅ Create AI_PROJECTS folder
3. ✅ Add your first project
4. ✅ Create project brain
5. ✅ Run `saois run PROJECT`
6. 🎉 Start coding!

## Support

- Check `saois help` for all commands
- Read `docs/SAOIS_SYSTEM_RULES.md` for system design
- Run `saois doctor` to diagnose issues

---

**You now have a personal AI Dev OS!** 🚀
