# SAOIS Expert Library

Collection of expert personas for AI tools. Reference them with `@` in Windsurf, Cursor, Claude, etc.

## Available Experts

| Expert | Trigger | Best For |
|--------|---------|----------|
| 🎨 UI/UX Designer | `@ui_ux_designer` | Design reviews, UI improvements |
| 👨‍💻 Code Reviewer | `@code_reviewer` | Code reviews, quality checks |
| ✏️ Language Editor | `@language_editor` | Copywriting, documentation |
| 🌍 Translator | `@translator` | Localization, i18n |
| 🌌 3D Background | `@3d_background` | WebGL, Three.js animations |
| 🎭 Graphic Designer | `@graphic_designer` | Branding, visual identity |
| 🧪 Test Engineer | `@test_engineer` | Testing strategy, unit/e2e tests |
| 🔀 Git Expert | `@git_expert` | Git workflows, commit standards |
| ⚡ Optimization | `@optimization_expert` | Performance tuning |
| 🔒 Security | `@security_expert` | Security audits, vulnerabilities |
| 🗄️ Database | `@database_expert` | Schema design, query optimization |
| ♿ Accessibility | `@accessibility_expert` | WCAG compliance, a11y |
| 🚀 DevOps | `@devops_expert` | CI/CD, infrastructure |
| 📊 Product Manager | `@product_manager` | PRDs, prioritization |

## Usage

### Install experts into a project
```bash
saois experts install <project-name>
```

### Install specific experts only
```bash
saois experts install <project-name> --only ui_ux_designer,code_reviewer
```

### List all experts
```bash
saois experts list
```

### View an expert
```bash
saois experts show ui_ux_designer
```

## How It Works

1. SAOIS copies expert MD files into your project's `.windsurf/rules/` or `.ai/experts/` folder
2. Reference them in Windsurf/Cursor with `@expert_name`
3. The AI adopts the expert persona and follows their principles

## Example Usage in AI Tool

```
@code_reviewer please review my authentication logic in src/auth.ts
```

```
@ui_ux_designer the landing page feels cluttered, suggest improvements
```

```
@security_expert audit my API endpoints for vulnerabilities
```
