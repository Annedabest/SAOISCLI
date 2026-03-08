import argparse
import json
import os
import sys
import time
import subprocess
import shutil
import threading
import re
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich import box
from rich.style import Style
from rich.prompt import Prompt, Confirm

from .tool_router import (
    read_project_brain,
    get_tool_for_task,
    check_ai_rules_exists,
    get_project_brain_template,
    get_ai_rules_template,
    get_recommended_model
)
from .os_detector import (
    get_os,
    open_application,
    open_url,
    check_tool_installed,
    get_ai_projects_path
)
from .installer import (
    check_all_tools,
    offer_installation,
    verify_tool_installation
)

console = Console()

CONFIG_DIR = Path.home() / ".saois"
PROJECTS_FILE = CONFIG_DIR / "projects.json"
INSTALL_MARKER = CONFIG_DIR / ".installed"

def ensure_config():
    CONFIG_DIR.mkdir(exist_ok=True)
    if not PROJECTS_FILE.exists():
        PROJECTS_FILE.write_text("{}")

def load_projects():
    ensure_config()
    projects = json.loads(PROJECTS_FILE.read_text())
    
    # Auto-discover projects from AI_PROJECTS folder
    ai_projects_path = get_ai_projects_path()
    if ai_projects_path:
        for item in ai_projects_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Add if not already registered
                if item.name not in projects:
                    projects[item.name] = str(item)
    
    return projects

def save_projects(projects):
    ensure_config()
    PROJECTS_FILE.write_text(json.dumps(projects, indent=2))


def show_header():
    header = Panel(
        "[bold #00ffff]⚡ SAOIS CLI ⚡[/bold #00ffff]\n[#ff00ff]Smart Project Manager[/#ff00ff]",
        border_style="#00ffff",
        box=box.ROUNDED,
        padding=(0, 2)
    )
    console.print(header)
    console.print()

def scan_folder_for_projects(folder_path):
    folder = Path(folder_path).expanduser().resolve()
    if not folder.exists():
        console.print(f"[red]✗ Folder not found: {folder}[/red]")
        return []
    
    projects_found = []
    for item in folder.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            projects_found.append((item.name, str(item)))
    
    return projects_found

def show_help():
    show_header()
    
    help_table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    help_table.add_column("Command", style="#00ffff", no_wrap=True)
    help_table.add_column("Description", style="white")
    help_table.add_column("Example", style="#00ff88")
    
    help_table.add_row("list", "Show all registered projects", "saois list")
    help_table.add_row("add <name> <path>", "Add a single project", "saois add myapp ~/projects/myapp")
    help_table.add_row("import", "Bulk import projects from folder", "saois import")
    help_table.add_row("status <name>", "Show project details & info", "saois status myapp")
    help_table.add_row("run <name>", "Launch AI tool for project task", "saois run myapp")
    help_table.add_row("doctor", "Check installed AI tools", "saois doctor")
    help_table.add_row("open <name>", "Open project folder", "saois open myapp")
    help_table.add_row("remove <name>", "Remove a project", "saois remove myapp")
    help_table.add_row("docker <name>", "Start project with Docker", "saois docker myapp")
    help_table.add_row("keys <name>", "Extract API keys from project", "saois keys myapp")
    help_table.add_row("install", "Install SAOIS globally", "saois install")
    help_table.add_row("uninstall", "Uninstall SAOIS", "saois uninstall")
    help_table.add_row("help", "Show this help message", "saois help")
    
    console.print(help_table)
    console.print("\n[dim]💡 AI Dev OS - Auto-launches the right tool for each task[/dim]")

def extract_api_keys(project_path):
    keys_found = {}
    search_patterns = {
        'API_KEY': r'[A-Z_]*API[_A-Z]*KEY[A-Z_]*\s*=\s*["\']([^"\'\n]+)["\']',
        'SECRET': r'[A-Z_]*SECRET[A-Z_]*\s*=\s*["\']([^"\'\n]+)["\']',
        'TOKEN': r'[A-Z_]*TOKEN[A-Z_]*\s*=\s*["\']([^"\'\n]+)["\']',
        'DATABASE_URL': r'DATABASE_URL\s*=\s*["\']([^"\'\n]+)["\']',
    }
    
    search_files = ['.env', '.env.local', '.env.production', 'config.json', 'config.yaml']
    
    for filename in search_files:
        file_path = project_path / filename
        if file_path.exists():
            try:
                content = file_path.read_text()
                for key_type, pattern in search_patterns.items():
                    matches = re.findall(pattern, content, re.MULTILINE)
                    if matches:
                        if filename not in keys_found:
                            keys_found[filename] = []
                        for match in matches:
                            keys_found[filename].append((key_type, match))
            except:
                pass
    
    return keys_found

def show_api_keys(name):
    show_header()
    projects = load_projects()
    
    if name not in projects:
        console.print(f"[red]✗ Project '{name}' not found[/red]")
        return
    
    project_path = Path(projects[name])
    
    with console.status(f"[#00ffff]Scanning {name} for API keys...[/#00ffff]", spinner="dots"):
        keys = extract_api_keys(project_path)
    
    if not keys:
        console.print(Panel(
            "[yellow]No API keys or secrets found[/yellow]\n\n"
            "[dim]Searched in: .env, .env.local, .env.production, config.json, config.yaml[/dim]",
            title=f"[bold #ff00ff]{name}[/bold #ff00ff]",
            border_style="#ffff00",
            box=box.ROUNDED
        ))
        return
    
    console.print(f"[bold #00ffff]🔑 API Keys & Secrets - {name}[/bold #00ffff]\n")
    
    for filename, entries in keys.items():
        console.print(f"[#ff00ff]📄 {filename}[/#ff00ff]")
        for key_type, value in entries:
            masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:] if len(value) > 8 else "****"
            console.print(f"  [#00ffff]•[/#00ffff] {key_type}: [dim]{masked_value}[/dim]")
        console.print()
    
    console.print("[dim]⚠️  Keys are masked for security. Check the files directly for full values.[/dim]")

def start_docker(name):
    show_header()
    projects = load_projects()
    
    if name not in projects:
        console.print(f"[red]✗ Project '{name}' not found[/red]")
        return
    
    project_path = Path(projects[name])
    
    # Check for docker-compose.yml or Dockerfile
    docker_compose = project_path / "docker-compose.yml"
    dockerfile = project_path / "Dockerfile"
    
    if not docker_compose.exists() and not dockerfile.exists():
        console.print(Panel(
            "[yellow]No Docker configuration found[/yellow]\n\n"
            "[dim]Looking for: docker-compose.yml or Dockerfile[/dim]",
            title=f"[bold #ff00ff]{name}[/bold #ff00ff]",
            border_style="#ffff00",
            box=box.ROUNDED
        ))
        return
    
    console.print(f"[bold #00ffff]🐳 Starting Docker - {name}[/bold #00ffff]\n")
    
    try:
        if docker_compose.exists():
            with console.status("[#00ffff]Running docker-compose up...[/#00ffff]", spinner="dots"):
                result = subprocess.run(
                    ["docker-compose", "up", "-d"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0:
                console.print("[#00ff00]✓ Docker containers started![/#00ff00]\n")
                
                # Try to find the port from docker-compose.yml
                try:
                    compose_content = docker_compose.read_text()
                    port_match = re.search(r'"(\d+):\d+"', compose_content)
                    if port_match:
                        port = port_match.group(1)
                        console.print(f"[bold #00ffff]🌐 Local URL:[/bold #00ffff]")
                        console.print(f"   [#00ff88]http://localhost:{port}[/#00ff88]\n")
                    else:
                        console.print("[dim]Check docker-compose.yml for port mappings[/dim]\n")
                except:
                    console.print("[dim]Check docker-compose.yml for port mappings[/dim]\n")
                
                console.print("[dim]To stop: docker-compose down[/dim]")
            else:
                console.print(f"[red]✗ Failed to start Docker[/red]")
                console.print(f"[dim]{result.stderr}[/dim]")
        else:
            console.print("[yellow]Found Dockerfile but no docker-compose.yml[/yellow]")
            console.print("[dim]You'll need to build and run manually:[/dim]")
            console.print(f"[#00ffff]  docker build -t {name} .[/#00ffff]")
            console.print(f"[#00ffff]  docker run -p 3000:3000 {name}[/#00ffff]")
    
    except FileNotFoundError:
        console.print("[red]✗ Docker not found. Please install Docker first.[/red]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")

def import_projects():
    show_header()
    
    console.print("[bold #00ffff]📁 Bulk Project Import[/bold #00ffff]\n")
    folder_path = Prompt.ask("[#ff00ff]Enter folder path to scan[/#ff00ff]")
    
    with console.status("[#00ffff]Scanning folder...[/#00ffff]", spinner="dots"):
        found = scan_folder_for_projects(folder_path)
    
    if not found:
        console.print("[yellow]No projects found in this folder[/yellow]")
        return
    
    console.print(f"\n[#00ff00]✓ Found {len(found)} projects:[/#00ff00]\n")
    for name, path in found:
        console.print(f"  [#00ffff]▸[/#00ffff] {name}")
    
    if Confirm.ask("\n[#ff00ff]Import all these projects?[/#ff00ff]", default=True):
        projects = load_projects()
        added = 0
        for name, path in found:
            if name not in projects:
                projects[name] = path
                added += 1
        save_projects(projects)
        console.print(f"\n[#00ff00]✓ Imported {added} new projects![/#00ff00]")
    else:
        console.print("[yellow]Import cancelled[/yellow]")

def list_projects():
    show_header()
    projects = load_projects()
    
    if not projects:
        console.print(Panel(
            "[#ffff00]No projects yet![/#ffff00]\n\n"
            "[dim]Get started:[/dim]\n"
            "  [#00ffff]•[/#00ffff] Add one: [bold]saois add myapp ~/path[/bold]\n"
            "  [#00ffff]•[/#00ffff] Import many: [bold]saois import[/bold]",
            title="[bold #ff00ff]Projects[/bold #ff00ff]",
            border_style="#00ffff",
            box=box.ROUNDED
        ))
        return
    
    table = Table(
        show_header=True,
        header_style="bold #ff00ff",
        border_style="#00ffff",
        box=box.ROUNDED,
        title=f"[bold #00ffff]Your Projects[/bold #00ffff] [dim]({len(projects)} total)[/dim]",
        padding=(0, 1)
    )
    table.add_column("#", style="#ff00ff", no_wrap=True, justify="right", width=4)
    table.add_column("Name", style="bold #00ffff", no_wrap=True)
    table.add_column("Location", style="#00ff88")
    table.add_column("Status", justify="center", style="bold", width=10)
    
    for idx, (name, path) in enumerate(projects.items(), 1):
        exists = "[#00ff00]✓ Ready[/#00ff00]" if Path(path).exists() else "[#ff0000]✗ Missing[/#ff0000]"
        table.add_row(str(idx), name, path, exists)
    
    console.print(table)
    console.print("\n[dim]💡 Tip: Use [bold]saois open <name>[/bold] to open a project[/dim]")

def status_project(name):
    show_header()
    projects = load_projects()
    
    if name not in projects:
        console.print(f"[red]✗ Project '{name}' not found[/red]\n")
        if projects:
            console.print("[dim]Available projects:[/dim]")
            for p in list(projects.keys())[:5]:
                console.print(f"  [#00ffff]•[/#00ffff] {p}")
        return
    
    project_path = Path(projects[name])
    
    with console.status(f"[#00ffff]Analyzing {name}...[/#00ffff]", spinner="dots"):
        time.sleep(0.2)
    
    console.print(f"[bold #00ffff]📊 Project Status - {name}[/bold #00ffff]\n")
    
    # Basic info
    console.print(f"[#ff00ff]📁 Location:[/#ff00ff] {project_path}")
    console.print(f"[#ff00ff]✓ Exists:[/#ff00ff] {'Yes' if project_path.exists() else 'No'}\n")
    
    # Check for project brain
    brain_data = read_project_brain(project_path)
    
    if brain_data:
        console.print("[bold #00ffff]🧠 Project Brain:[/bold #00ffff]")
        if brain_data.get('next_task_type'):
            console.print(f"  [#ff00ff]Next Task Type:[/#ff00ff] {brain_data['next_task_type']}")
        if brain_data.get('next_task'):
            console.print(f"  [#ff00ff]Next Task:[/#ff00ff] {brain_data['next_task'][:100]}..." if len(brain_data.get('next_task', '')) > 100 else f"  [#ff00ff]Next Task:[/#ff00ff] {brain_data['next_task']}")
        if brain_data.get('current_status'):
            console.print(f"  [#ff00ff]Status:[/#ff00ff] {brain_data['current_status']}")
        console.print()
    else:
        console.print("[yellow]⚠️  No project brain found[/yellow]")
        console.print("[dim]To use SAOIS effectively, create:[/dim]")
        console.print(f"[#00ffff]  {project_path}/docs/project_brain.md[/#00ffff]\n")
        console.print("[dim]This helps AI tools understand your project better.[/dim]\n")
    
    # Check for AI rules
    if not check_ai_rules_exists(project_path):
        console.print("[yellow]💡 Tip: Add AI safety rules[/yellow]")
        console.print("[dim]Create:[/dim] [#00ffff].ai_rules.md[/#00ffff]")
        console.print("[dim]This keeps AI agents focused on the task.[/dim]\n")
        
        if brain_data and brain_data.get('next_task_type'):
            recommended = get_recommended_model(brain_data['next_task_type'])
            console.print(f"[#ff00ff]💰 Recommended Model:[/#ff00ff] {recommended}\n")
    
    # Check for common files
    files_to_check = {
        'package.json': '📦 Node.js project',
        'requirements.txt': '🐍 Python project',
        'Cargo.toml': '🦀 Rust project',
        'go.mod': '🔵 Go project',
        'docker-compose.yml': '🐳 Docker Compose',
        'Dockerfile': '🐳 Dockerfile',
        '.env': '🔑 Environment variables',
        'README.md': '📖 README'
    }
    
    console.print("[bold #00ffff]Files Found:[/bold #00ffff]")
    found_any = False
    for filename, description in files_to_check.items():
        if (project_path / filename).exists():
            console.print(f"  [#00ff00]✓[/#00ff00] {description}")
            found_any = True
    
    if not found_any:
        console.print("  [dim]No common project files detected[/dim]")
    
    console.print()
    
    # Quick actions
    console.print("[bold #00ffff]Quick Actions:[/bold #00ffff]")
    if brain_data and brain_data.get('next_task_type'):
        console.print(f"  [#00ffff]•[/#00ffff] Start work: [bold]saois run {name}[/bold]")
    if (project_path / "docker-compose.yml").exists():
        console.print(f"  [#00ffff]•[/#00ffff] Start with Docker: [bold]saois docker {name}[/bold]")
    if (project_path / ".env").exists():
        console.print(f"  [#00ffff]•[/#00ffff] View API keys: [bold]saois keys {name}[/bold]")
    console.print(f"  [#00ffff]•[/#00ffff] Open folder: [bold]saois open {name}[/bold]")

def open_project(name):
    show_header()
    projects = load_projects()
    
    if name not in projects:
        console.print(f"[red]✗ Project '{name}' not found[/red]")
        return
    
    project_path = projects[name]
    
    with console.status(f"[#00ffff]Opening {name}...[/#00ffff]", spinner="dots"):
        time.sleep(0.2)
    
    try:
        subprocess.run(["open", project_path], check=True)
        console.print(f"[#00ff00]✓ Opened {name}[/#00ff00]")
        console.print(f"[dim]{project_path}[/dim]")
    except Exception as e:
        console.print(f"[red]✗ Failed to open: {e}[/red]")

def add_project(name, path):
    show_header()
    projects = load_projects()
    abs_path = str(Path(path).expanduser().resolve())
    
    if not Path(abs_path).exists():
        console.print(f"[yellow]⚠ Warning: Path not found - {abs_path}[/yellow]")
        if not Confirm.ask("Add anyway?", default=False):
            console.print("[dim]Cancelled[/dim]")
            return
    
    projects[name] = abs_path
    save_projects(projects)
    
    console.print(f"\n[#00ff00]✓ Added {name}[/#00ff00]")
    console.print(f"[dim]{abs_path}[/dim]")
    console.print(f"\n[dim]Total: {len(projects)} projects[/dim]")

def remove_project(name):
    show_header()
    projects = load_projects()
    if name in projects:
        if Confirm.ask(f"[yellow]Remove {name}?[/yellow]", default=False):
            removed_path = projects[name]
            del projects[name]
            save_projects(projects)
            console.print(f"\n[#ff00ff]✓ Removed {name}[/#ff00ff]")
            console.print(f"[dim]{len(projects)} projects remaining[/dim]")
        else:
            console.print("[dim]Cancelled[/dim]")
    else:
        console.print(f"[red]✗ Project '{name}' not found[/red]")

def install_cli():
    show_header()
    
    shell_rc = Path.home() / ".zshrc"
    alias_line = "alias saois='python3 -m saois.cli'"
    
    with console.status("[#00ffff]Installing...[/#00ffff]", spinner="dots"):
        time.sleep(0.5)
        if shell_rc.exists():
            content = shell_rc.read_text()
            if alias_line not in content:
                with open(shell_rc, "a") as f:
                    f.write(f"\n# SAOIS CLI\n{alias_line}\n")
        else:
            shell_rc.write_text(f"# SAOIS CLI\n{alias_line}\n")
        
        INSTALL_MARKER.write_text("installed")
    
    console.print(f"\n[#00ff00]✓ Installation complete![/#00ff00]\n")
    console.print("[bold #ffff00]Next step:[/bold #ffff00]")
    console.print("  [#00ffff]source ~/.zshrc[/#00ffff]\n")
    console.print("[dim]Then use 'saois' from anywhere[/dim]")

def run_setup_wizard():
    """Interactive setup wizard for SAOIS."""
    show_header()
    
    console.print("[bold #00ffff]🚀 SAOIS Setup Wizard[/bold #00ffff]\n")
    console.print("[dim]Let's configure your AI Dev OS![/dim]\n")
    
    # Step 1: Check AI_PROJECTS folder
    console.print("[bold #ff00ff]Step 1: AI_PROJECTS Folder[/bold #ff00ff]")
    ai_projects = get_ai_projects_path()
    
    if ai_projects:
        console.print(f"[#00ff00]✓ Found: {ai_projects}[/#00ff00]\n")
    else:
        console.print("[yellow]AI_PROJECTS folder not found[/yellow]")
        if Confirm.ask("Create ~/Documents/AI_PROJECTS now?", default=True):
            ai_projects_path = Path.home() / "Documents" / "AI_PROJECTS"
            ai_projects_path.mkdir(parents=True, exist_ok=True)
            console.print(f"[#00ff00]✓ Created: {ai_projects_path}[/#00ff00]\n")
        else:
            console.print("[dim]Skipped. You can create it later.[/dim]\n")
    
    # Step 2: Check installed tools
    console.print("[bold #ff00ff]Step 2: AI Tools Detection[/bold #ff00ff]")
    tools_status = check_all_tools()
    installed_count = sum(tools_status.values())
    
    if installed_count > 0:
        console.print(f"[#00ff00]✓ Found {installed_count} AI tools installed[/#00ff00]")
        for tool, installed in tools_status.items():
            if installed:
                console.print(f"  [#00ff00]✓[/#00ff00] {tool}")
    else:
        console.print("[yellow]No AI tools detected yet[/yellow]")
        console.print("[dim]Don't worry! SAOIS will open browser URLs as fallback.[/dim]")
    console.print()
    
    # Step 3: Tool routing explanation
    console.print("[bold #ff00ff]Step 3: Tool Routing[/bold #ff00ff]")
    console.print("[dim]SAOIS automatically launches the right tool based on task type:[/dim]\n")
    
    routing_table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    routing_table.add_column("Task Type", style="#00ffff")
    routing_table.add_column("Tool", style="#00ff88")
    
    routing_table.add_row("coding", "Windsurf IDE")
    routing_table.add_row("debugging", "Windsurf IDE")
    routing_table.add_row("architecture", "Claude Code")
    routing_table.add_row("research", "Perplexity AI")
    routing_table.add_row("analysis", "Sourcegraph Cody")
    routing_table.add_row("planning", "Claude Code")
    
    console.print(routing_table)
    console.print()
    
    # Step 4: Next steps
    console.print("[bold #ff00ff]Step 4: Next Steps[/bold #ff00ff]")
    console.print("[#00ffff]1.[/#00ffff] Add projects: [bold]saois add myapp ~/path[/bold]")
    console.print("[#00ffff]2.[/#00ffff] Or import many: [bold]saois import[/bold]")
    console.print("[#00ffff]3.[/#00ffff] Create project brain: [bold]docs/project_brain.md[/bold]")
    console.print("[#00ffff]4.[/#00ffff] Start working: [bold]saois run PROJECT[/bold]\n")
    
    console.print("[#00ff00]✓ Setup complete! You're ready to use SAOIS.[/#00ff00]")
    console.print("[dim]Run [bold]saois help[/bold] to see all commands.[/dim]")

def run_doctor():
    """Check which AI tools are installed."""
    show_header()
    
    console.print("[bold #00ffff]🔧 SAOIS Doctor - Checking AI Tools[/bold #00ffff]\n")
    
    os_type = get_os()
    console.print(f"[#ff00ff]Operating System:[/#ff00ff] {os_type}\n")
    
    # Check AI_PROJECTS folder
    ai_projects = get_ai_projects_path()
    if ai_projects:
        console.print(f"[#00ff00]✓ AI_PROJECTS folder found[/#00ff00]")
        console.print(f"[dim]  {ai_projects}[/dim]\n")
    else:
        console.print("[yellow]⚠️  AI_PROJECTS folder not found[/yellow]")
        console.print("[dim]  Create: ~/Documents/AI_PROJECTS[/dim]\n")
    
    # Check installed tools
    tools_status = check_all_tools()
    
    console.print("[bold #00ffff]Installed Tools:[/bold #00ffff]")
    
    tool_table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    tool_table.add_column("Tool", style="#00ffff")
    tool_table.add_column("Status", justify="center")
    tool_table.add_column("Used For", style="dim")
    
    tool_usage = {
        "Windsurf": "coding, debugging",
        "Claude": "architecture, planning",
        "Perplexity": "research",
        "Cody": "codebase analysis",
        "Continue": "automation"
    }
    
    for tool, installed in tools_status.items():
        status = "[#00ff00]✓ Installed[/#00ff00]" if installed else "[red]✗ Not found[/red]"
        usage = tool_usage.get(tool, "")
        tool_table.add_row(tool, status, usage)
    
    console.print(tool_table)
    console.print()
    
    # Show summary
    installed_count = sum(tools_status.values())
    total_count = len(tools_status)
    
    if installed_count == 0:
        console.print("[yellow]No AI tools detected. SAOIS will open browser URLs for now.[/yellow]")
    elif installed_count < total_count:
        console.print(f"[#00ffff]{installed_count}/{total_count} tools installed.[/#00ffff]")
        console.print("[dim]SAOIS will use installed tools and fallback to browser for others.[/dim]")
    else:
        console.print("[#00ff00]✓ All tools installed! You're ready to go.[/#00ff00]")
    
    console.print("\n[dim]💡 Tip: Use [bold]saois run PROJECT[/bold] to auto-launch the right tool[/dim]")

def run_project(name):
    """Launch the appropriate AI tool based on project brain."""
    show_header()
    projects = load_projects()
    
    if name not in projects:
        console.print(f"[red]✗ Project '{name}' not found[/red]\n")
        if projects:
            console.print("[dim]Available projects:[/dim]")
            for p in list(projects.keys())[:5]:
                console.print(f"  [#00ffff]•[/#00ffff] {p}")
        return
    
    project_path = Path(projects[name])
    
    # Read project brain
    with console.status(f"[#00ffff]Reading project brain...[/#00ffff]", spinner="dots"):
        brain_data = read_project_brain(project_path)
    
    if not brain_data:
        console.print(f"[yellow]⚠️  No project brain found for {name}[/yellow]\n")
        console.print("[dim]To use SAOIS effectively, create:[/dim]")
        console.print(f"[#00ffff]  {project_path}/docs/project_brain.md[/#00ffff]\n")
        console.print("[dim]Template:[/dim]")
        console.print(Panel(
            get_project_brain_template(),
            border_style="#ff00ff",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        
        if Confirm.ask("\n[#ff00ff]Open project folder instead?[/#ff00ff]", default=True):
            open_project(name)
        return
    
    # Get task type
    task_type = brain_data.get('next_task_type')
    if not task_type:
        console.print(f"[yellow]⚠️  No NEXT TASK TYPE defined in project brain[/yellow]\n")
        console.print("[dim]Add to project_brain.md:[/dim]")
        console.print("[#00ffff]NEXT TASK TYPE:\ncoding[/#00ffff]\n")
        return
    
    # Get tool for task
    tool_info = get_tool_for_task(task_type)
    if not tool_info:
        console.print(f"[red]✗ Unknown task type: {task_type}[/red]\n")
        console.print("[dim]Valid types: coding, debugging, architecture, research, analysis, automation, planning[/dim]")
        return
    
    # Display project info
    console.print(f"[bold #00ffff]🚀 Launching AI Tool[/bold #00ffff]\n")
    console.print(f"[#ff00ff]Project:[/#ff00ff] {name}")
    console.print(f"[#ff00ff]Task Type:[/#ff00ff] {task_type}")
    if brain_data.get('next_task'):
        task_preview = brain_data['next_task'][:80] + "..." if len(brain_data['next_task']) > 80 else brain_data['next_task']
        console.print(f"[#ff00ff]Task:[/#ff00ff] {task_preview}")
    console.print(f"[#ff00ff]Tool:[/#ff00ff] {tool_info['name']}\n")
    
    # Check if tool is installed
    os_type = get_os()
    tool_installed = check_tool_installed(tool_info['command'])
    
    if tool_installed:
        console.print(f"[#00ffff]Opening {tool_info['name']}...[/#00ffff]")
        
        # Try to open the tool with project path
        success = False
        try:
            if tool_info['command'] == 'windsurf':
                # Open Windsurf with project path
                if os_type == "macos":
                    subprocess.run(["open", "-a", "Windsurf", str(project_path)], check=True)
                else:
                    subprocess.run([tool_info['command'], str(project_path)], check=False)
                success = True
            else:
                success = open_application(tool_info['name'], os_type)
        except:
            pass
        
        if success:
            console.print(f"[#00ff00]✓ {tool_info['name']} launched![/#00ff00]\n")
            console.print("[dim]💡 Next steps:[/dim]")
            console.print(f"[dim]  1. Read docs/project_brain.md[/dim]")
            console.print(f"[dim]  2. Work on: {task_type}[/dim]")
            if check_ai_rules_exists(project_path):
                console.print(f"[dim]  3. Follow .ai_rules.md[/dim]")
        else:
            console.print(f"[yellow]⚠️  Could not launch {tool_info['name']}[/yellow]")
            console.print(f"[#00ffff]Opening in browser instead...[/#00ffff]")
            open_url(tool_info['url'], os_type)
    else:
        # Tool not installed - offer installation
        console.print(f"[yellow]{tool_info['name']} not detected[/yellow]\n")
        offer_installation(tool_info['name'], tool_info['command'], tool_info['url'])

def uninstall_cli():
    show_header()
    
    if not Confirm.ask("[yellow]Uninstall SAOIS?[/yellow]", default=False):
        console.print("[dim]Cancelled[/dim]")
        return
    
    shell_rc = Path.home() / ".zshrc"
    alias_line = "alias saois='python3 -m saois.cli'"
    
    with console.status("[#ff00ff]Uninstalling...[/#ff00ff]", spinner="dots"):
        time.sleep(0.3)
        if shell_rc.exists():
            lines = shell_rc.read_text().split("\n")
            new_lines = [line for line in lines if alias_line not in line and "# SAOIS CLI" not in line]
            shell_rc.write_text("\n".join(new_lines))
        
        if INSTALL_MARKER.exists():
            INSTALL_MARKER.unlink()
    
    if CONFIG_DIR.exists() and Confirm.ask("[yellow]Delete all project data?[/yellow]", default=False):
        shutil.rmtree(CONFIG_DIR)
        console.print("[#ff0000]✓ Data removed[/#ff0000]")
    
    console.print(f"\n[#ff00ff]✓ Uninstalled[/#ff00ff]")
    console.print("[dim]Run: source ~/.zshrc[/dim]")

def main():
    parser = argparse.ArgumentParser(
        description="⚡ SAOIS - Futuristic CLI for managing development projects",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subparsers.add_parser("help", help="Show help and all commands")
    subparsers.add_parser("setup", help="Setup wizard for tool routing")
    subparsers.add_parser("install", help="Install SAOIS globally")
    subparsers.add_parser("uninstall", help="Uninstall SAOIS")
    subparsers.add_parser("list", help="Show all projects")
    subparsers.add_parser("import", help="Import projects from a folder")
    subparsers.add_parser("doctor", help="Check installed AI tools")
    
    status_parser = subparsers.add_parser("status", help="Show detailed project status")
    status_parser.add_argument("project", help="Project name")
    
    run_parser = subparsers.add_parser("run", help="Launch AI tool for project")
    run_parser.add_argument("project", help="Project name")
    
    docker_parser = subparsers.add_parser("docker", help="Start project with Docker")
    docker_parser.add_argument("project", help="Project name")
    
    keys_parser = subparsers.add_parser("keys", help="Extract API keys from project")
    keys_parser.add_argument("project", help="Project name")
    
    open_parser = subparsers.add_parser("open", help="Open project folder")
    open_parser.add_argument("project", help="Project name")
    
    add_parser = subparsers.add_parser("add", help="Register a new project")
    add_parser.add_argument("name", help="Project name")
    add_parser.add_argument("path", help="Project path")
    
    remove_parser = subparsers.add_parser("remove", help="Deregister a project")
    remove_parser.add_argument("name", help="Project name")
    
    args = parser.parse_args()
    
    if args.command == "help":
        show_help()
    elif args.command == "setup":
        run_setup_wizard()
    elif args.command == "install":
        install_cli()
    elif args.command == "uninstall":
        uninstall_cli()
    elif args.command == "doctor":
        run_doctor()
    elif args.command == "import":
        import_projects()
    elif args.command == "list":
        list_projects()
    elif args.command == "status":
        status_project(args.project)
    elif args.command == "run":
        run_project(args.project)
    elif args.command == "docker":
        start_docker(args.project)
    elif args.command == "keys":
        show_api_keys(args.project)
    elif args.command == "open":
        open_project(args.project)
    elif args.command == "add":
        add_project(args.name, args.path)
    elif args.command == "remove":
        remove_project(args.name)
    else:
        show_help()

if __name__ == "__main__":
    main()
