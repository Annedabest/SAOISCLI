# SAOIS CLI SYSTEM RULES

## Purpose
SAOIS CLI manages multiple development projects and automatically launches the correct AI tool depending on the task type defined in `project_brain.md`.

## Supported Tools
- **Windsurf IDE** (coding, debugging)
- **Claude Code** (architecture, planning)
- **Perplexity AI** (research)
- **Sourcegraph Cody** (codebase analysis)
- **Continue.dev** (automation)

## Task Routing Rules

| Task Type | Tool |
|-----------|------|
| `coding` | Windsurf |
| `debugging` | Windsurf |
| `architecture` | Claude Code |
| `research` | Perplexity |
| `analysis` | Sourcegraph Cody |
| `automation` | Continue.dev |
| `planning` | Claude Code |

## Behavior Rules

1. CLI must read `docs/project_brain.md`
2. CLI must detect `NEXT TASK TYPE`
3. CLI must map task type to tool
4. CLI must open the correct tool

## Installation Fallback

If tool is not installed:

**Step 1:** Ask the user permission
```
"Claude Code not detected. Install now?"
```

**Step 2:** Detect operating system
- macOS
- Linux
- Windows

**Step 3:** Offer two options:
1. Run installation command
2. Open official download page

**Step 4:** Verify installation after completion

If installation fails: Open browser download page automatically.

## Security Rules

- Never run install commands without confirmation
- Always show the command before executing
- Always detect OS before suggesting install command

## Cross Platform Rules

### macOS
- Launch: `open -a AppName`
- Browser: `open https://site`

### Linux
- Launch: `xdg-open` or direct command
- Browser: `xdg-open https://site`

### Windows
- Launch: `start AppName`
- Browser: `start https://site`

## Project Brain Template

Every project must contain:
```
docs/project_brain.md
```

Template:
```markdown
PROJECT NAME:
[Your project name]

MISSION:
[What this project does]

CURRENT STATUS:
[Current development state]

ARCHITECTURE SUMMARY:
[High-level architecture]

KNOWN ISSUES:
[List of known problems]

NEXT TASK TYPE:
[coding | research | architecture | debugging | analysis | planning | automation]

NEXT TASK:
[Describe the next development action]
```

## AI Safety Rules

Each project should contain:
```
.ai_rules.md
```

Template:
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
```

## CLI Commands

| Command | Purpose |
|---------|---------|
| `saois list` | List all projects |
| `saois status PROJECT` | Show project brain |
| `saois run PROJECT` | Launch correct tool for project |
| `saois doctor` | Check installed tools |
| `saois add NAME PATH` | Register a project |
| `saois import` | Bulk import from folder |

## Project Discovery

SAOIS looks for projects in two places:
1. `~/Documents/AI_PROJECTS/` (auto-discovered)
2. Manually registered projects (via `saois add`)

## Tool Installation Commands

### macOS
```bash
brew install windsurf
brew install claude-code
```

### Linux
```bash
pip install windsurf
pip install claude-code
```

### Windows
```bash
winget install windsurf
winget install claude-code
```

## Tool URLs

- Windsurf: https://codeium.com/windsurf
- Claude Code: https://claude.ai/code
- Perplexity: https://perplexity.ai
- Sourcegraph Cody: https://sourcegraph.com/cody
- Continue.dev: https://continue.dev

## Workflow Example

```bash
# Check projects
saois list

# View project brain
saois status SAOIS

# Start work (auto-opens correct tool)
saois run SAOIS
```

Output:
```
Project: SAOIS
Next Task Type: research
Opening Perplexity AI…
```

## ADHD-Friendly Design

- Clear, simple output
- Automatic tool launching
- Guided workflow
- Minimal decisions needed
- One command to start work
