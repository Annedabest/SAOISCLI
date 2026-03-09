# 🚀 SAOIS CLI - Quick Start Guide

## Installation (Choose One)

### ⚡ Fastest Way
```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
./install.sh
source ~/.zshrc
saois list
```

### 🔧 Manual Way
```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
pip3 install -e .
python3 -m saois.cli install
source ~/.zshrc
saois list
```

### 🧪 Try Without Installing
```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
source activate.sh
saois list
```

## First-Time Setup (Required)

1. **Create the AI projects home**
```bash
mkdir -p ~/Documents/AI_PROJECTS
```

2. **Run the guided setup**
```bash
saois setup
```
This wizard will:
- Verify the `AI_PROJECTS` folder (creates it if missing)
- Detect installed AI tools (Windsurf, Claude, Perplexity, etc.)
- Show you how task routing works
- Remind you to add project brains

3. **Add or import projects**
```bash
saois add myproject ~/Documents/AI_PROJECTS/myproject
# or
saois import
```

4. **Create docs/project_brain.md** in every project (template available in `docs/project_brain_template.md`).

5. **(Optional) Add .ai_rules.md** for AI safety guardrails (see `docs/ai_rules_template.md`).

## Common Tasks

### Add Your First Project
```bash
saois add myproject ~/path/to/project
```

### Import All Projects from a Folder
```bash
saois import
# Then enter: ~/projects
```

### View All Projects
```bash
saois list
```

### Launch the Right AI Tool Automatically
```bash
saois run myproject
```
Reads `docs/project_brain.md`, detects `NEXT TASK TYPE`, and opens Windsurf/Claude/Perplexity/etc. automatically.

### Open a Project
```bash
saois open myproject
```

### Remove a Project
```bash
saois remove myproject
```

## Features

✅ **AI Dev OS** - SAOIS routes tasks to the right AI tool
✅ **Setup Wizard** - `saois setup` guides new installs
✅ **Project Brain** - Keep `docs/project_brain.md` updated
✅ **AI Safety Rules** - `.ai_rules.md` reminders for agents
✅ **Bulk Import** - Add entire folders in one command
✅ **Clean UI** - Easy to read, colorful output
✅ **Smart Prompts** - Confirms before changes
✅ **Helpful Tips** - Guides you along the way

## Troubleshooting

**Command not found?**
```bash
source ~/.zshrc
```

**Still not working?**
```bash
python3 -m saois.cli list
```

**Doctor says tools not installed, but they are?**
- Make sure the apps live in `/Applications` (e.g., `/Applications/Windsurf.app`).
- Re-run `saois doctor` after installing.
- Use `saois setup` to confirm routing is configured.

**Want to start fresh?**
```bash
saois uninstall
./install.sh
source ~/.zshrc
```
