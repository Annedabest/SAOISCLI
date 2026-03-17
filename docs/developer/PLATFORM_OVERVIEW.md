# SAOIS CLI - COMPREHENSIVE PLATFORM OVERVIEW

**Last Updated:** 2026-03-16  
**Status:** MVP / Early Production  
**Maintainer:** Anne (@Annedabest)

---

## EXECUTIVE SUMMARY

**SAOIS CLI** (Smart AI-Optimized Intelligence System) is an intelligent command-line interface that acts as an "AI Development Operating System" - automatically routing development tasks to the appropriate AI tools (Windsurf, Claude, Perplexity, etc.) while managing multi-project workflows across devices.

**Core Value Proposition:** "One command to launch the right AI tool with full project context - no thinking required."

**The Problem:**
- Developers waste mental energy choosing AI tools for each task
- Managing 10-100+ projects creates organizational chaos
- Context switching overhead slows development
- Missing dependencies break workflows

**The Solution:**
- Single command (`saois run myproject`) reads project metadata
- Automatically routes to optimal AI tool based on task type
- Centralized project registry with validation
- Dependency detection and automated installation

---

## 1. CORE CAPABILITIES

### 1.1 Intelligent AI Tool Routing
**Purpose:** Automatically select and launch the right AI tool based on task type  
**How:** Parses `docs/project_brain.md` → Extracts task type → Routes to appropriate tool  
**Supported Tools:** Windsurf (coding), Claude (architecture), Perplexity (research), Cursor, VS Code, ChatGPT

### 1.2 Project Registry Management
**Purpose:** Centralized tracking of all development projects  
**Storage:** `~/.saois/projects.json`  
**Features:** Bulk import, selective import, GitHub cloning, validation, archiving

### 1.3 Project Brain System
**Purpose:** Structured project metadata for AI context  
**Format:** `docs/project_brain.md` (markdown with YAML-like fields)  
**Contents:** Project status, next tasks, architecture summary, dependencies

### 1.4 Smart Project Execution
**Purpose:** One-command project startup with dependency checking  
**Detects:** Node.js, Python, Rust, Go, Docker projects  
**Actions:** Validates dependencies, runs appropriate commands

### 1.5 Dependency Detection & Installation
**Purpose:** Automated environment setup  
**Checks:** Docker, Node.js, Python, package managers  
**Installs:** Via Homebrew (macOS), apt/yum (Linux), manual guidance (Windows)

### 1.6 Project Validation & Repair
**Purpose:** Maintain registry integrity  
**Features:** Path validation, broken project detection, bulk archive/remove/fix

### 1.7 GitHub Integration
**Purpose:** Streamlined project onboarding  
**Features:** Clone repos, auto-register cloned projects

### 1.8 API Key Extraction
**Purpose:** Security-conscious credential viewing  
**Features:** Scans `.env` files, displays masked values (first 4 + last 4 chars)

### 1.9 Error Simplification & AI Prompts
**Purpose:** Accelerate debugging  
**Features:** Translates cryptic errors to plain English, generates ready-to-use AI prompts

### 1.10 AI Prompt Template Library
**Purpose:** Structured AI prompts for common scenarios  
**Templates:** 20+ curated prompts (performance audit, security review, dark mode, etc.)

### 1.11 Git Automation
**Purpose:** Streamlined version control  
**Features:** Automated commit/push workflows with interactive prompts

### 1.12 AI Tool Installation Wizard
**Purpose:** Guided setup for new users  
**Features:** Detects installed tools, guides installation, configures task routing

---

## 2. SYSTEM ARCHITECTURE

### 2.1 Technology Stack
- **Language:** Python 3.9+
- **UI Library:** Rich (terminal formatting)
- **Storage:** JSON files (no database)
- **Platform:** Cross-platform (macOS, Linux, Windows)

### 2.2 Module Structure
```
saois/
├── cli.py                    # Main command router (1661 lines) ⚠️
├── tool_router.py            # AI tool selection logic
├── tool_config.py            # Tool configuration management
├── ai_tool_installer.py      # Installation automation
├── os_detector.py            # Cross-platform OS detection
├── helpers.py                # Project type detection, error handling
├── dependency_checker.py     # Dependency validation
├── github_helper.py          # Git automation
├── github_integration.py     # GitHub cloning
├── installer.py              # Tool installation management
└── prompt_library.py         # AI prompt templates
```

### 2.3 Data Storage
```
~/.saois/
├── projects.json             # Project registry
├── settings.json             # User settings
├── tools_config.json         # AI tool configuration
├── archived_projects/
│   └── projects.json         # Archived projects
└── {project}_errors.txt      # Error logs (opt-in)
```

### 2.4 Component Interaction Flow
```
User Command → CLI Parser → Command Handler
    ↓
Project Registry (JSON) → Project Brain Parser
    ↓
Tool Router → OS Detector → Launch AI Tool
    ↓
Dependency Checker → System Package Managers
```

---

## 3. USER WORKFLOWS

### 3.1 Onboarding Flow
1. Install SAOIS (`./install.sh` or `pip install -e .`)
2. Run `saois quickstart` or `saois setup`
3. Configure AI_PROJECTS folder (default: `~/Documents/AI_PROJECTS`)
4. Import projects (`saois import`)
5. Create project brains (`saois init-brains`)
6. Check system health (`saois doctor`)
7. Start working (`saois run PROJECT`)

### 3.2 Primary Workflow (AI-Assisted Development)
1. Developer runs `saois run myproject`
2. SAOIS reads `docs/project_brain.md`
3. Extracts `NEXT TASK TYPE` (e.g., "coding")
4. Routes to appropriate tool (e.g., Windsurf)
5. Launches tool with project path
6. Developer works with full context
7. Updates project brain when complete

### 3.3 Project Management Workflow
1. Import projects (`saois import`)
2. Validate registry (`saois validate`)
3. Archive/remove broken projects
4. View all projects (`saois list`)
5. Search projects (`saois search TERM`)

---

## 4. COMMAND REFERENCE

### Core Commands
- `saois run PROJECT` - Launch AI tool for project
- `saois list` - Show all registered projects
- `saois import` - Import projects (folder/GitHub)
- `saois validate` - Validate project registry
- `saois doctor` - System health check

### Setup Commands
- `saois quickstart` - Interactive setup wizard
- `saois setup` - Configure AI_PROJECTS folder
- `saois setup-tools` - Install AI tools
- `saois config-tools` - Configure tool routing

### Project Commands
- `saois init-brains` - Create project brain files
- `saois archive PROJECT` - Archive project
- `saois remove PROJECT` - Remove from registry
- `saois search TERM` - Search projects

### Utility Commands
- `saois prompts` - View AI prompt library
- `saois simplify-error` - Translate error messages
- `saois extract-keys PROJECT` - View API keys
- `saois git-commit PROJECT` - Automated git workflow

---

## 5. STRENGTHS

### Technical Strengths
1. **Clean Abstraction** - Separated concerns (routing, detection, installation)
2. **Cross-Platform** - Works on macOS, Linux, Windows
3. **Minimal Dependencies** - Only Rich library required
4. **Rich UI** - Beautiful terminal output with colors, tables, panels
5. **Comprehensive Features** - 20+ commands covering full workflow
6. **Error Handling** - Simplifies errors, generates AI prompts

### Product Strengths
1. **Solves Real Problem** - Context switching is genuine developer pain
2. **Novel Approach** - AI tool routing is innovative
3. **User-Friendly** - Interactive menus, helpful prompts
4. **Privacy-Focused** - No telemetry, local-only operation
5. **Extensible** - Easy to add new AI tools or project types
6. **Well-Documented** - Comprehensive README, multiple guides

### Market Strengths
1. **First-Mover** - No direct competitors in AI tool routing
2. **Growing Market** - AI-assisted development expanding rapidly
3. **Open Source** - Community can contribute, fork, extend

---

## 6. WEAKNESSES & RISKS

### Technical Weaknesses
1. ⚠️ **No Tests** - Zero test coverage, high regression risk
2. ⚠️ **Monolithic Code** - `cli.py` is 1661 lines, difficult to maintain
3. ⚠️ **Fragile Parsing** - Regex-based brain parsing breaks easily
4. ⚠️ **No Backup** - JSON corruption could lose all projects
5. ⚠️ **Hard-Coded Assumptions** - macOS-centric paths
6. ⚠️ **Command Injection Risk** - `shell=True` in subprocess calls
7. ⚠️ **No Async** - Blocking operations, no concurrent handling

### Product Weaknesses
1. **Requires Manual Setup** - Project brains must be created manually
2. **Learning Curve** - Users must understand task types, brain format
3. **Limited AI Integration** - Only launches tools, no API integration
4. **No Cloud Sync** - Projects don't sync across devices
5. **No Team Features** - Single-user only
6. **No Analytics** - Cannot measure impact or usage

### Operational Risks
1. **Bus Factor: 1** - Solo-developed, project would stall if developer unavailable
2. **No Monitoring** - Cannot track usage, errors, or adoption
3. **No Monetization** - Unsustainable without revenue model
4. **Dependency on External Tools** - Value diminishes if AI tools change

---

## 7. TARGET USERS

### Primary Users
- Solo developers managing 10+ projects simultaneously
- AI-assisted developers using multiple AI tools
- Developers with ADHD or executive function challenges
- Power users wanting streamlined workflows

### Use Cases
1. **Multi-Project Management** - Developers juggling many projects
2. **AI Tool Optimization** - Users wanting automatic tool selection
3. **Context Preservation** - Developers needing project state tracking
4. **Dependency Management** - Users wanting automated environment setup

---

## 8. FUTURE OPPORTUNITIES

### Near-Term (0-3 months)
1. Add automated testing (unit, integration, E2E)
2. Refactor monolithic `cli.py` into smaller modules
3. Implement JSON backup/recovery mechanism
4. Improve Windows compatibility
5. Add configuration validation

### Mid-Term (3-6 months)
1. Cloud sync (opt-in, encrypted)
2. Team collaboration features
3. AI tool API integration (not just launching)
4. Analytics dashboard (opt-in)
5. Plugin system for extensibility

### Long-Term (6-12 months)
1. Web UI for project management
2. Mobile companion app
3. Team licensing and monetization
4. Enterprise features (SSO, audit logs)
5. AI-powered project insights

---

## 9. COMPETITIVE LANDSCAPE

### Direct Competitors
- **None identified** - No other tools do AI tool routing

### Indirect Competitors
- **Project Managers:** tmux, tmuxinator, i3, etc. (no AI integration)
- **AI Tools:** Windsurf, Cursor, GitHub Copilot (single-tool focus)
- **Launchers:** Alfred, Raycast (no project context)

### Competitive Advantages
1. **AI Tool Routing** - Unique capability
2. **Project Brain System** - Structured context for AI
3. **Privacy-First** - No telemetry, local-only
4. **Cross-Platform** - Works everywhere

---

## 10. BUSINESS MODEL (POTENTIAL)

### Current State
- **Free and open source**
- **No revenue**
- **Unsustainable commercially**

### Potential Models
1. **Freemium**
   - Free: Basic features, local-only
   - Premium: Cloud sync, analytics, team features ($10-20/month)

2. **Team Licensing**
   - Per-user pricing ($10-50/user/month)
   - Team features (shared registries, collaboration)

3. **Enterprise**
   - Custom pricing
   - SSO, audit logs, support contracts

---

## 11. KEY METRICS (IF IMPLEMENTED)

### User Metrics
- Active users (DAU/MAU)
- Projects per user
- Commands per session
- Retention rate

### Product Metrics
- Tool routing accuracy
- Time saved per task
- Error reduction rate
- Dependency installation success rate

### Business Metrics
- Conversion rate (free → paid)
- Churn rate
- Customer lifetime value
- Net Promoter Score

---

## 12. TECHNICAL DEBT

### High Priority
1. **Add automated testing** - Critical for reliability
2. **Refactor cli.py** - Too large, difficult to maintain
3. **Implement backup system** - Prevent data loss
4. **Security audit** - Address command injection risks

### Medium Priority
1. **Improve error handling** - Consistent patterns
2. **Add logging framework** - Better debugging
3. **Configuration validation** - Prevent invalid states
4. **Documentation** - API docs, architecture diagrams

### Low Priority
1. **Performance optimization** - Handle 1000+ projects
2. **Internationalization** - Multi-language support
3. **Accessibility** - Screen reader support
4. **CI/CD pipeline** - Automated testing and releases

---

## 13. DEPENDENCIES

### Python Dependencies
- **Rich** (terminal UI) - Only external dependency
- **Standard Library:** pathlib, subprocess, json, re, argparse, platform

### System Dependencies
- **Python 3.9+** - Core runtime
- **Git** - Version control operations
- **Package Managers:** Homebrew (macOS), apt/yum (Linux)

### External Tools (Optional)
- **AI Tools:** Windsurf, Claude Desktop, Cursor, VS Code, ChatGPT, Perplexity
- **Development Tools:** Docker, npm, pip, yarn, pnpm, cargo, go

---

## 14. SECURITY CONSIDERATIONS

### Current Security Posture
- **No Authentication** - Local-only tool
- **No Encryption** - JSON files in plaintext
- **Masked Display** - API keys shown with masking
- **Opt-In Logging** - Error logs require confirmation
- **No Telemetry** - Zero data collection

### Security Risks
1. **Command Injection** - `shell=True` in subprocess
2. **Path Traversal** - Limited validation on paths
3. **Credential Exposure** - `.env` files unencrypted (standard)
4. **JSON Corruption** - No integrity checks

### Mitigation Strategies
1. Use `shell=False` with argument lists
2. Validate and sanitize all user-provided paths
3. Implement JSON schema validation
4. Add backup/recovery mechanisms

---

## 15. CONCLUSION

**SAOIS CLI** is an innovative MVP that solves a real problem (AI tool fragmentation + project chaos) with a novel approach (intelligent routing). It demonstrates strong product-market fit for power users managing multiple AI-assisted development projects.

**Key Achievements:**
- ✅ Comprehensive feature set (20+ commands)
- ✅ Beautiful, user-friendly CLI
- ✅ Cross-platform compatibility
- ✅ Privacy-focused design
- ✅ Minimal dependencies

**Critical Needs:**
- ⚠️ Automated testing
- ⚠️ Code refactoring (cli.py)
- ⚠️ Backup/recovery system
- ⚠️ Monetization strategy
- ⚠️ Team expansion (reduce bus factor)

**Recommendation:** SAOIS has strong potential as both an open-source community tool and a commercial product. Priority should be on technical debt reduction (testing, refactoring) and establishing a sustainable business model (freemium or team licensing).

---

**Document Version:** 1.0  
**Next Review:** 2026-06-16  
**Maintainer:** Anne (@Annedabest)
