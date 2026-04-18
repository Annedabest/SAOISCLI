"""
SAOIS Experts CLI
Install expert MD files into projects for @ referencing in AI tools
"""
import shutil
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box

console = Console()

EXPERTS_DIR = Path(__file__).parent / "experts"

EXPERT_METADATA = {
    "ui_ux_designer": {"emoji": "🎨", "name": "UI/UX Designer", "desc": "Design reviews, UI improvements"},
    "code_reviewer": {"emoji": "👨‍💻", "name": "Code Reviewer", "desc": "Code reviews, quality checks"},
    "language_editor": {"emoji": "✏️", "name": "Language Editor", "desc": "Copywriting, documentation"},
    "translator": {"emoji": "🌍", "name": "Translator", "desc": "Localization, i18n"},
    "3d_background": {"emoji": "🌌", "name": "3D Background", "desc": "WebGL, Three.js animations"},
    "graphic_designer": {"emoji": "🎭", "name": "Graphic Designer", "desc": "Branding, visual identity"},
    "test_engineer": {"emoji": "🧪", "name": "Test Engineer", "desc": "Testing strategy, unit/e2e tests"},
    "git_expert": {"emoji": "🔀", "name": "Git Expert", "desc": "Git workflows, commit standards"},
    "optimization_expert": {"emoji": "⚡", "name": "Optimization", "desc": "Performance tuning"},
    "security_expert": {"emoji": "🔒", "name": "Security", "desc": "Security audits, vulnerabilities"},
    "database_expert": {"emoji": "🗄️", "name": "Database", "desc": "Schema design, query optimization"},
    "accessibility_expert": {"emoji": "♿", "name": "Accessibility", "desc": "WCAG compliance, a11y"},
    "devops_expert": {"emoji": "🚀", "name": "DevOps", "desc": "CI/CD, infrastructure"},
    "product_manager": {"emoji": "📊", "name": "Product Manager", "desc": "PRDs, prioritization"},
}


def list_experts():
    """List all available experts."""
    console.print("\n[bold #00ffff]🎓 SAOIS Expert Library[/bold #00ffff]\n")
    console.print("[dim]Expert personas for AI tools (Windsurf, Cursor, Claude)[/dim]\n")
    
    table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    table.add_column("Trigger", style="#00ffff")
    table.add_column("Expert", style="bold")
    table.add_column("Best For", style="dim")
    
    for trigger, meta in EXPERT_METADATA.items():
        table.add_row(f"@{trigger}", f"{meta['emoji']} {meta['name']}", meta['desc'])
    
    console.print(table)
    console.print(f"\n[dim]💡 Install into a project: [bold]saois experts install <project>[/bold][/dim]")
    console.print(f"[dim]💡 View an expert: [bold]saois experts show <trigger>[/bold][/dim]")


def show_expert(trigger):
    """Display an expert's full content."""
    expert_file = EXPERTS_DIR / f"{trigger}.md"
    
    if not expert_file.exists():
        console.print(f"[red]Expert '{trigger}' not found[/red]")
        list_experts()
        return
    
    content = expert_file.read_text()
    console.print(content)


def install_experts(project_name=None, specific_experts=None):
    """Install expert MD files into a project."""
    from .core.registry import registry
    
    projects = {name: str(path) for name, path in registry.get_all().items()}
    
    if not projects:
        console.print("[yellow]No projects registered. Run 'saois import' first.[/yellow]")
        return
    
    # Select project
    if not project_name:
        console.print("[bold #00ffff]Select project to install experts into:[/bold #00ffff]\n")
        project_list = list(projects.items())
        for i, (name, _) in enumerate(project_list[:20], 1):
            console.print(f"  [#00ffff]{i}.[/#00ffff] {name}")
        
        choice = Prompt.ask("\n[#ff00ff]Project number[/#ff00ff]")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(project_list):
                project_name, project_path = project_list[idx]
            else:
                console.print("[red]Invalid selection[/red]")
                return
        except ValueError:
            console.print("[red]Invalid input[/red]")
            return
    else:
        if project_name not in projects:
            console.print(f"[red]Project '{project_name}' not found[/red]")
            return
        project_path = projects[project_name]
    
    project_dir = Path(project_path)
    if not project_dir.exists():
        console.print(f"[red]Project path doesn't exist: {project_path}[/red]")
        return
    
    # Select experts
    if not specific_experts:
        console.print(f"\n[bold #00ffff]Select experts to install:[/bold #00ffff]\n")
        
        expert_list = list(EXPERT_METADATA.items())
        for i, (trigger, meta) in enumerate(expert_list, 1):
            console.print(f"  [#00ffff]{i}.[/#00ffff] {meta['emoji']} {meta['name']} [dim]({meta['desc']})[/dim]")
        
        console.print(f"\n[dim]Enter numbers comma-separated (e.g., 1,3,5) or 'all'[/dim]")
        choice = Prompt.ask("[#ff00ff]Your choice[/#ff00ff]", default="all")
        
        if choice.lower() == "all":
            specific_experts = list(EXPERT_METADATA.keys())
        else:
            specific_experts = []
            try:
                for num in choice.split(","):
                    idx = int(num.strip()) - 1
                    if 0 <= idx < len(expert_list):
                        specific_experts.append(expert_list[idx][0])
            except ValueError:
                console.print("[red]Invalid input[/red]")
                return
    
    if not specific_experts:
        console.print("[yellow]No experts selected[/yellow]")
        return
    
    # Determine destination
    # Priority: .windsurf/rules > .cursor/rules > .ai/experts
    destinations = []
    if (project_dir / ".windsurf").exists() or Confirm.ask(
        "[#ff00ff]Install for Windsurf? (.windsurf/rules/)[/#ff00ff]", default=True
    ):
        destinations.append(project_dir / ".windsurf" / "rules")
    
    if (project_dir / ".cursor").exists():
        if Confirm.ask("[#ff00ff]Also install for Cursor? (.cursor/rules/)[/#ff00ff]", default=True):
            destinations.append(project_dir / ".cursor" / "rules")
    
    if not destinations:
        destinations.append(project_dir / ".ai" / "experts")
    
    # Install
    console.print(f"\n[bold #00ffff]Installing {len(specific_experts)} experts...[/bold #00ffff]\n")
    
    installed = 0
    for dest_dir in destinations:
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for trigger in specific_experts:
            source = EXPERTS_DIR / f"{trigger}.md"
            if not source.exists():
                console.print(f"  [yellow]⚠️  {trigger}.md not found in library[/yellow]")
                continue
            
            dest = dest_dir / f"{trigger}.md"
            shutil.copy(source, dest)
            meta = EXPERT_METADATA.get(trigger, {})
            console.print(f"  [#00ff00]✓[/#00ff00] {meta.get('emoji', '')} {meta.get('name', trigger)} → {dest.relative_to(project_dir)}")
            installed += 1
    
    console.print(f"\n[bold #00ff00]✅ Installed {installed} experts into {project_name}[/bold #00ff00]")
    console.print(f"\n[bold #ffff00]How to use:[/bold #ffff00]")
    console.print(f"  Open the project in Windsurf/Cursor")
    console.print(f"  Reference an expert with [bold]@expert_name[/bold]")
    console.print(f"\n[dim]Examples:[/dim]")
    console.print(f"  [dim]@code_reviewer review my auth logic[/dim]")
    console.print(f"  [dim]@ui_ux_designer improve this landing page[/dim]")
    console.print(f"  [dim]@security_expert audit API endpoints[/dim]")


def browse_experts():
    """Interactive expert browser."""
    list_experts()
    console.print()
    
    choice = Prompt.ask("[#ff00ff]Enter trigger to view (or 'q' to quit)[/#ff00ff]")
    
    if choice.lower() == 'q':
        return
    
    # Strip @ if provided
    choice = choice.lstrip('@')
    
    if choice in EXPERT_METADATA:
        show_expert(choice)
    else:
        console.print(f"[red]Expert '{choice}' not found[/red]")
