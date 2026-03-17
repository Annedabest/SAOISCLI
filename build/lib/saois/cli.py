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
    get_ai_projects_path,
    set_ai_projects_path,
    load_settings
)
from .installer import (
    check_all_tools,
    offer_installation,
    verify_tool_installation
)
from .helpers import (
    detect_project_type,
    run_command_with_output,
    simplify_error,
    get_fix_prompt,
    log_error_to_file
)
from .dependency_checker import check_dependencies_for_project
from .github_helper import auto_commit_and_push
from .ai_tool_installer import install_all_ai_tools

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
        return {}
    
    projects = {}
    for item in folder.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            projects[item.name] = str(item)
    
    return projects

def show_help():
    show_header()
    
    help_table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    help_table.add_column("Command", style="#00ffff", no_wrap=True)
    help_table.add_column("Description", style="white")
    help_table.add_column("Example", style="#00ff88")
    
    help_table.add_row("quickstart", "Interactive setup guide", "saois quickstart")
    help_table.add_row("setup", "Configure AI projects folder", "saois setup")
    help_table.add_row("list", "Show all registered projects", "saois list")
    help_table.add_row("add <name> <path>", "Add a single project", "saois add myapp ~/projects/myapp")
    help_table.add_row("import", "Bulk import projects from folder", "saois import")
    help_table.add_row("validate", "Validate & fix project paths", "saois validate")
    help_table.add_row("init-brains", "Create project brains for all", "saois init-brains")
    help_table.add_row("status <name>", "Show project details & info", "saois status myapp")
    help_table.add_row("run <name>", "Launch AI tool for project task", "saois run myapp")
    help_table.add_row("docker <name>", "Start project locally", "saois docker myapp")
    help_table.add_row("keys <name>", "Extract API keys from project", "saois keys myapp")
    help_table.add_row("doctor", "Check installed AI tools", "saois doctor")
    help_table.add_row("setup-tools", "Install AI tools", "saois setup-tools")
    help_table.add_row("config-tools", "Configure your AI tools", "saois config-tools")
    help_table.add_row("menu", "Interactive menu (easy mode)", "saois menu")
    help_table.add_row("prompts [name]", "Browse AI prompt templates", "saois prompts browse")
    help_table.add_row("open <name>", "Open project folder", "saois open myapp")
    help_table.add_row("remove <name>", "Remove a project", "saois remove myapp")
    help_table.add_row("git-push <name>", "Commit & push to GitHub", "saois git-push myapp")
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
    
    console.print(f"[bold #00ffff]🚀 Starting Project - {name}[/bold #00ffff]\n")
    
    # Check for custom run commands
    from .tool_router import read_project_brain
    brain_data = read_project_brain(project_path)
    
    # Check if brain is still template (not customized)
    brain_file = project_path / "docs" / "project_brain.md"
    if brain_file.exists():
        content = brain_file.read_text()
        is_template = "[Your project name]" in content or "Leave empty if not applicable" in content
        
        if is_template:
            console.print("[yellow]⚠️  Project brain is still using template[/yellow]")
            console.print("[dim]You should customize it with your project details[/dim]\n")
            
            if Confirm.ask("[#ff00ff]Show AI prompt to customize it?[/#ff00ff]", default=True):
                console.print("\n" + "="*60)
                console.print("[bold #00ffff]📋 COPY THIS PROMPT TO YOUR AI TOOL:[/bold #00ffff]")
                console.print("="*60 + "\n")
                
                prompt = f"""Please help me customize the project_brain.md file for my project.

Project: {name}
Location: {project_path}

The file is at: {brain_file}

Please:
1. Read the current project_brain.md file
2. Analyze the project structure and code
3. Fill in all the template sections with actual project information:
   - PROJECT NAME
   - MISSION (what does this project do?)
   - CURRENT STATUS (what stage is it in?)
   - ARCHITECTURE SUMMARY (tech stack, key components)
   - KNOWN ISSUES (any bugs or problems)
   - RUN COMMANDS (how to start/test the project)
   - NEXT TASK (what needs to be done next)

4. Save the updated project_brain.md file

Make it detailed and accurate so AI tools can understand the project context."""
                
                console.print(prompt)
                console.print("\n" + "="*60)
                console.print("[dim]Copy the text above and paste it into Windsurf, Claude, or your AI tool[/dim]")
                console.print("="*60 + "\n")
                
                if Confirm.ask("[#ff00ff]Open project in AI tool now?[/#ff00ff]", default=True):
                    pass  # Continue with normal flow
                else:
                    return
    
    custom_command = None
    
    if brain_data and brain_data.get("run_commands"):
        run_commands = brain_data["run_commands"].strip()
        # Remove example markers and brackets
        run_commands = re.sub(r'\[.*?\]', '', run_commands)
        run_commands = run_commands.replace('Examples:', '').strip()
        # Get first non-empty line as the command
        for line in run_commands.split('\n'):
            line = line.strip().lstrip('-').strip()
            if line and not line.startswith('[') and not line.startswith('Leave empty'):
                custom_command = line
                break
    
    if custom_command:
        console.print(f"[#00ffff]📋 Custom command from project brain:[/#00ffff]")
        console.print(f"  [bold]{custom_command}[/bold]\n")
        
        if Confirm.ask("Run this command?", default=True):
            with console.status(f"[#00ffff]Running {custom_command}...[/#00ffff]", spinner="dots"):
                result = run_command_with_output(custom_command, project_path)
            
            if result["success"]:
                console.print("[#00ff00]✓ Command executed successfully![/#00ff00]\n")
                console.print(result["stdout"])
            else:
                console.print(f"[red]✗ Command failed[/red]\n")
                console.print(f"[yellow]Error:[/yellow] {result['stderr'][:200]}\n")
                console.print("[dim]Tip: Update RUN COMMANDS in docs/project_brain.md[/dim]")
        return
    
    # Detect project type and requirements
    project_info = detect_project_type(project_path)
    
    # Check and offer to install dependencies
    if not check_dependencies_for_project(project_info):
        console.print("\n[dim]Install dependencies and try again[/dim]")
        return
    
    # Check for docker-compose.yml or Dockerfile
    docker_compose = project_path / "docker-compose.yml"
    dockerfile = project_path / "Dockerfile"
    
    if docker_compose.exists() or dockerfile.exists():
        console.print("[#00ffff]🐳 Docker configuration found[/#00ffff]")
        
        try:
            if docker_compose.exists():
                with console.status("[#00ffff]Running docker-compose up...[/#00ffff]", spinner="dots"):
                    result = run_command_with_output("docker-compose up -d", project_path)
                
                if result["success"]:
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
                    console.print(f"[red]✗ Failed to start Docker[/red]\n")
                    
                    # Simplify error
                    simplified = simplify_error(result["stderr"], "docker")
                    console.print(f"[yellow]Error:[/yellow] {simplified}\n")
                    
                    # Generate AI fix prompt
                    fix_prompt = get_fix_prompt(simplified, "docker", project_info)
                    
                    # Log error (opt-in)
                    log_file = log_error_to_file(name, {
                        "project_type": "docker",
                        "command": "docker-compose up -d",
                        "simplified": simplified,
                        "full_error": result["stderr"],
                        "recommendation": "Check Docker is running and ports are available",
                        "ai_prompt": fix_prompt
                    }, CONFIG_DIR)
                    
                    if log_file:
                        console.print(f"[dim]Error log saved to: {log_file}[/dim]\n")
                    
                    # Recommend AI tool
                    console.print("[#ff00ff]💡 Recommended action:[/#ff00ff]")
                    console.print("  Use [bold]Windsurf[/bold] or [bold]Claude[/bold] to fix this")
                    console.print(f"  Run: [bold]saois run {name}[/bold]\n")
                    
                    console.print("[dim]AI Prompt (copy this):[/dim]")
                    console.print(Panel(fix_prompt, border_style="#ff00ff", box=box.ROUNDED))
            else:
                console.print("[yellow]Found Dockerfile but no docker-compose.yml[/yellow]")
                console.print("[dim]You'll need to build and run manually:[/dim]")
                console.print(f"[#00ffff]  docker build -t {name} .[/#00ffff]")
                console.print(f"[#00ffff]  docker run -p 3000:3000 {name}[/#00ffff]")
        
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
    
    # No Docker - try running with dependencies
    elif project_info["type"]:
        console.print(f"[#00ffff]📦 {project_info['type'].title()} project detected[/#00ffff]")
        console.print(f"[dim]Package manager: {project_info['package_manager'] or 'N/A'}[/dim]\n")
        
        if project_info["start_command"]:
            console.print("[#ff00ff]Recommended command:[/#ff00ff]")
            console.print(f"  [#00ffff]{project_info['start_command']}[/#00ffff]\n")
            
            if Confirm.ask("Run this command now?", default=False):
                console.print()
                with console.status(f"[#00ffff]Running {project_info['start_command']}...[/#00ffff]", spinner="dots"):
                    result = run_command_with_output(project_info["start_command"], project_path)
                
                if result["success"]:
                    console.print("[#00ff00]✓ Project started successfully![/#00ff00]\n")
                    console.print(result["stdout"])
                else:
                    console.print(f"[red]✗ Failed to start project[/red]\n")
                    
                    # Simplify error
                    simplified = simplify_error(result["stderr"], project_info["type"])
                    console.print(f"[yellow]Error:[/yellow] {simplified}\n")
                    
                    # Generate AI fix prompt
                    fix_prompt = get_fix_prompt(simplified, project_info["type"], project_info)
                    
                    # Log error (opt-in)
                    log_file = log_error_to_file(name, {
                        "project_type": project_info["type"],
                        "command": project_info["start_command"],
                        "simplified": simplified,
                        "full_error": result["stderr"],
                        "recommendation": f"Install dependencies and check configuration",
                        "ai_prompt": fix_prompt
                    }, CONFIG_DIR)
                    
                    if log_file:
                        console.print(f"[dim]Error log saved to: {log_file}[/dim]\n")
                    
                    # Recommend AI tool
                    console.print("[#ff00ff]💡 Recommended action:[/#ff00ff]")
                    console.print("  Use [bold]Windsurf[/bold] to debug and fix this")
                    console.print(f"  Run: [bold]saois run {name}[/bold]\n")
                    
                    console.print("[dim]AI Prompt (copy this):[/dim]")
                    console.print(Panel(fix_prompt, border_style="#ff00ff", box=box.ROUNDED))
        else:
            console.print("[yellow]Could not determine start command[/yellow]")
            console.print("[dim]Check the project documentation for setup instructions[/dim]")
    else:
        console.print("[yellow]No Docker or standard project structure found[/yellow]")
        console.print("[dim]Looking for: docker-compose.yml, Dockerfile, package.json, requirements.txt, etc.[/dim]")
        console.print("\n[#ff00ff]💡 Tip:[/#ff00ff] Add a docker-compose.yml or check project documentation")

def import_from_github():
    """Import a project by cloning from GitHub."""
    from .github_integration import is_git_installed, install_git_prompt, clone_github_repo, parse_github_url
    
    if not is_git_installed():
        if not install_git_prompt():
            return
    
    console.print("[bold #00ffff]🐙 GitHub Import[/bold #00ffff]\n")
    
    repo_url = Prompt.ask("[#ff00ff]GitHub repository URL[/#ff00ff]")
    
    # Parse repo name
    repo_name = parse_github_url(repo_url)
    if not repo_name:
        console.print("[red]✗ Invalid GitHub URL[/red]")
        return
    
    # Ask for destination
    ai_projects = get_ai_projects_path(allow_missing=True)
    default_dest = str(ai_projects / repo_name) if ai_projects else str(Path.home() / repo_name)
    
    destination = Prompt.ask(
        "[#ff00ff]Clone to[/#ff00ff]",
        default=default_dest
    )
    destination = Path(destination).expanduser()
    
    if destination.exists():
        console.print(f"[yellow]⚠️  {destination} already exists[/yellow]")
        if not Confirm.ask("Overwrite?", default=False):
            return
    
    # Clone repository
    console.print(f"\n[dim]Cloning {repo_url}...[/dim]")
    with console.status("[#00ffff]Cloning repository...[/#00ffff]", spinner="dots"):
        success, error = clone_github_repo(repo_url, destination)
    
    if success:
        console.print(f"[#00ff00]✓ Cloned successfully![/#00ff00]\n")
        
        # Add to registry
        projects = load_projects()
        projects[repo_name] = str(destination)
        save_projects(projects)
        
        console.print(f"[#00ff00]✓ Added {repo_name} to registry[/#00ff00]")
        console.print(f"[dim]Run [bold]saois init-brains[/bold] to create project brain[/dim]")
    else:
        console.print(f"[red]✗ Clone failed: {error}[/red]")

def import_projects():
    show_header()
    
    console.print("[bold #00ffff]📁 Bulk Project Import[/bold #00ffff]\n")
    
    # Ask for source type
    source_type = Prompt.ask(
        "[#ff00ff]Import from?[/#ff00ff]",
        choices=["folder", "github"],
        default="folder"
    )
    
    if source_type == "github":
        import_from_github()
        return
    
    # Folder import
    folder_path = Prompt.ask("[#ff00ff]Enter folder path to scan[/#ff00ff]")
    
    with console.status("[#00ffff]Scanning folder...[/#00ffff]", spinner="dots"):
        found = scan_folder_for_projects(folder_path)
    
    if not found:
        console.print("[yellow]No projects found[/yellow]")
        return
    
    # Exclude AI_PROJECTS folder itself
    ai_projects_path = get_ai_projects_path(allow_missing=True)
    if ai_projects_path:
        ai_projects_name = ai_projects_path.name
        if ai_projects_name in found:
            del found[ai_projects_name]
            console.print(f"[dim]Excluding {ai_projects_name} folder from import[/dim]\n")
    
    if not found:
        console.print("[yellow]No projects found after filtering[/yellow]")
        return
    
    console.print(f"\n[#00ff00]✓ Found {len(found)} projects:[/#00ff00]\n")
    
    # Show projects with numbers for selection
    project_list = list(found.items())
    for i, (name, _) in enumerate(project_list, 1):
        console.print(f"  [dim]{i:2}.[/dim] [#00ffff]{name}[/#00ffff]")
    
    console.print()
    
    # Ask for import mode
    import_mode = Prompt.ask(
        "[#ff00ff]Import mode?[/#ff00ff]",
        choices=["all", "select", "cancel"],
        default="all"
    )
    
    if import_mode == "cancel":
        console.print("[dim]Cancelled[/dim]")
        return
    
    projects = load_projects()
    to_import = {}
    
    if import_mode == "all":
        to_import = found
    else:
        # Selective import
        console.print("\n[dim]Enter project numbers to import (comma-separated, or 'all'):[/dim]")
        console.print("[dim]Example: 1,3,5-8,12[/dim]")
        selection = Prompt.ask("[#ff00ff]Projects[/#ff00ff]")
        
        if selection.lower() == "all":
            to_import = found
        else:
            # Parse selection
            selected_indices = set()
            for part in selection.split(","):
                part = part.strip()
                if "-" in part:
                    start, end = part.split("-")
                    selected_indices.update(range(int(start), int(end) + 1))
                elif part.isdigit():
                    selected_indices.add(int(part))
            
            for idx in selected_indices:
                if 1 <= idx <= len(project_list):
                    name, path = project_list[idx - 1]
                    to_import[name] = path
    
    if not to_import:
        console.print("[yellow]No projects selected[/yellow]")
        return
    
    # Import selected projects
    new_count = 0
    for name, path in to_import.items():
        if name not in projects:
            projects[name] = path
            new_count += 1
    
    save_projects(projects)
    console.print(f"\n[#00ff00]✓ Imported {new_count} new projects![/#00ff00]")
    
    if new_count > 0:
        console.print(f"[dim]Run [bold]saois init-brains[/bold] to create project brains[/dim]")

def list_projects():
    show_header()
    projects = load_projects()
    
    if not projects:
        console.print(Panel(
            "[yellow]No projects yet![/yellow]\n\n"
            "[dim]Get started:[/dim]\n"
            "  [#00ffff]1.[/#00ffff] Import projects: [bold]saois import[/bold]\n"
            "  [#00ffff]2.[/#00ffff] Or add one: [bold]saois add myapp ~/path[/bold]\n\n"
            "[dim]💡 Tip: Run 'saois menu' for an easy interactive guide[/dim]",
            title="[bold #ff00ff]Projects[/bold #ff00ff]",
            border_style="#ffff00",
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
    
    # Ensure config directory exists FIRST
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
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
    
    # Step 1: Configure AI_PROJECTS folder
    console.print("[bold #ff00ff]Step 1: Projects Home Folder[/bold #ff00ff]")
    current_path = get_ai_projects_path(allow_missing=True)
    console.print(f"[#00ffff]Current setting:[/#00ffff] {current_path if current_path else 'Not configured'}")
    
    if Confirm.ask("Do you want to change this folder?", default=False):
        new_path = Prompt.ask("[#ff00ff]Enter full path for your AI projects[/#ff00ff]", default=str(current_path) if current_path else str(Path.home() / "Documents" / "AI_PROJECTS"))
        new_path = Path(new_path).expanduser()
        set_ai_projects_path(new_path)
        if not new_path.exists() and Confirm.ask("Folder does not exist. Create it now?", default=True):
            new_path.mkdir(parents=True, exist_ok=True)
            console.print(f"[#00ff00]✓ Created {new_path}[/#00ff00]")
        console.print(f"[#00ff00]✓ Projects folder set to {new_path}[/#00ff00]\n")
    else:
        if current_path and not current_path.exists():
            if Confirm.ask(f"Folder {current_path} is missing. Create it now?", default=True):
                current_path.mkdir(parents=True, exist_ok=True)
                console.print(f"[#00ff00]✓ Created {current_path}[/#00ff00]\n")
            else:
                console.print("[yellow]Skipping creation. SAOIS will remind you later.[/yellow]\n")
        elif current_path:
            console.print(f"[#00ff00]✓ Using {current_path}[/#00ff00]\n")
        else:
            console.print("[yellow]No folder configured yet. You can set it later.[/yellow]\n")
    
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
    
    # Get user's configured tools
    from .tool_config import load_tools_config, AVAILABLE_TOOLS
    config = load_tools_config()
    
    for task, tool_id in config["task_mapping"].items():
        tool_name = AVAILABLE_TOOLS.get(tool_id, {}).get("name", tool_id)
        routing_table.add_row(task, tool_name)
    
    console.print(routing_table)
    console.print()
    
    # Step 4: Next steps
    console.print("[bold #ff00ff]Step 4: Next Steps[/bold #ff00ff]")
    console.print("[#00ffff]1.[/#00ffff] Add projects: [bold]saois add myapp ~/path[/bold]")
    console.print("[#00ffff]2.[/#00ffff] Or import many: [bold]saois import[/bold]")
    console.print("[#00ffff]3.[/#00ffff] Create project brain: [bold]docs/project_brain.md[/bold]")
    console.print("[#00ffff]4.[/#00ffff] Start working: [bold]saois run PROJECT[/bold]\n")
    
    console.print("[#00ff00] Setup complete! You're ready to use SAOIS.[/#00ff00]")
    console.print("[dim]Run [bold]saois help[/bold] to see all commands.[/dim]")

def run_doctor():
    """Check system health and installed AI tools."""
    show_header()
    
    console.print("[bold #00ffff] SAOIS Doctor - Checking AI Tools[/bold #00ffff]\n")
    
    os_type = get_os()
    console.print(f"[dim]Operating System: {os_type}[/dim]\n")
    
    # Check AI_PROJECTS folder
    ai_projects = get_ai_projects_path()
    if ai_projects:
        console.print(f"[#00ff00] AI_PROJECTS folder found[/#00ff00]")
        console.print(f"  {ai_projects}\n")
    else:
        console.print(f"[yellow]  AI_PROJECTS folder not found[/yellow]")
        console.print(f"  [dim]Create: ~/Documents/AI_PROJECTS[/dim]\n")
    
    # Check installed tools
    console.print("[bold]Installed Tools:[/bold]")
    tools_status = check_all_tools()
    
    tool_table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    tool_table.add_column("Tool", style="#00ffff")
    tool_table.add_column("Status", justify="center")
    tool_table.add_column("Used For", style="dim")
    
    task_mapping = {
        "Windsurf": "coding, debugging",
        "Claude": "architecture, planning",
        "Cursor": "coding, AI-first editing",
        "VS Code": "coding with extensions",
        "ChatGPT": "general AI assistance"
    }
    
    missing_tools = []
    for tool, installed in tools_status.items():
        status = "[#00ff00]✓ Installed[/#00ff00]" if installed else "[yellow]Not installed[/yellow]"
        tool_table.add_row(tool, status, task_mapping.get(tool, ""))
        if not installed:
            missing_tools.append(tool)
    
    console.print(tool_table)
    
    installed_count = sum(tools_status.values())
    console.print(f"\n[#00ffff]Desktop Tools:[/#00ffff] {installed_count}/{len(tools_status)} installed")
    
    if installed_count == 0:
        console.print("[yellow]⚠️  No desktop AI tools detected[/yellow]")
        console.print("[dim]Run 'saois setup-tools' to install tools[/dim]")
    elif installed_count < len(tools_status):
        console.print(f"[dim]Run 'saois setup-tools' to install more tools[/dim]")
    else:
        console.print(f"[#00ff00]✓ All desktop tools installed![/#00ff00]")
    
    # Offer to install missing tools
    if missing_tools:
        console.print("\n[#ff00ff]Missing Tools:[/#ff00ff]")
        from .installer import TOOL_DETAILS
        
        for tool_name in missing_tools:
            tool_info = TOOL_DETAILS.get(tool_name)
            if not tool_info:
                continue
            
            console.print(f"  • [#00ffff]{tool_name}[/#00ffff] - {task_mapping.get(tool_name, 'AI assistant')}")
            console.print(f"    Download: {tool_info['url']}")
        
        if Confirm.ask("\n[#ff00ff]Run installation wizard?[/#ff00ff]", default=True):
            from .ai_tool_installer import install_all_ai_tools
            install_all_ai_tools()
            return
        
        console.print("\n[dim]💡 Tip: Run 'saois setup-tools' anytime to install tools[/dim]")

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
            console.print(f"\n[dim]💡 Tip: Run 'saois list' to see all projects[/dim]")
        else:
            console.print("[dim]No projects registered yet[/dim]")
            console.print(f"\n[dim]💡 Tip: Run 'saois import' to add projects[/dim]")
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

def show_interactive_menu():
    """Show a simple numbered menu for non-tech users."""
    show_header()
    
    console.print("[bold #00ffff]🌟 Welcome to SAOIS![/bold #00ffff]\n")
    console.print("[dim]What would you like to do?[/dim]\n")
    
    menu_items = [
        ("1", "Get Started (First Time Setup)", "quickstart"),
        ("2", "Import My Projects", "import"),
        ("3", "View My Projects", "list"),
        ("4", "Install AI Tools", "setup-tools"),
        ("5", "Configure My Tools", "config-tools"),
        ("6", "Check System Health", "doctor"),
        ("7", "Help & Commands", "help"),
        ("0", "Exit", "exit")
    ]
    
    for num, label, _ in menu_items:
        if num == "0":
            console.print(f"\n  [dim]{num}.[/dim] {label}")
        else:
            console.print(f"  [#00ffff]{num}.[/#00ffff] {label}")
    
    console.print()
    choice = Prompt.ask("[#ff00ff]Enter number[/#ff00ff]", default="1")
    
    # Map choice to command
    for num, _, cmd in menu_items:
        if choice == num:
            if cmd == "exit":
                console.print("[dim]Goodbye! 👋[/dim]")
                return None
            return cmd
    
    return "help"

def run_quickstart():
    """Interactive quickstart guide for new users - beginner friendly!"""
    show_header()
    
    console.print("[bold #00ffff]🚀 Welcome to SAOIS![/bold #00ffff]\n")
    console.print("[dim]Let's set you up in just a few easy steps.[/dim]\n"
                  "[dim]Don't worry - we'll guide you through everything![/dim]\n")
    
    # Step 1: Installation check
    console.print("[bold #ff00ff]Step 1: Installation[/bold #ff00ff]")
    if INSTALL_MARKER.exists():
        console.print("[#00ff00]✓ SAOIS is installed globally[/#00ff00]\n")
    else:
        console.print("[yellow]SAOIS not installed globally yet[/yellow]")
        if Confirm.ask("Install now?", default=True):
            install_cli()
        console.print()
    
    # Step 2: Projects folder
    console.print("[bold #ff00ff]Step 2: Projects Folder[/bold #ff00ff]")
    ai_projects = get_ai_projects_path(allow_missing=True)
    if ai_projects and ai_projects.exists():
        console.print(f"[#00ff00]✓ Projects folder: {ai_projects}[/#00ff00]\n")
    else:
        console.print("[yellow]No projects folder configured[/yellow]")
        if Confirm.ask("Run setup wizard to configure?", default=True):
            run_setup_wizard()
            return
        console.print()
    
    # Step 3: Check for projects
    console.print("[bold #ff00ff]Step 3: Your Projects[/bold #ff00ff]")
    projects = load_projects()
    if projects:
        console.print(f"[#00ff00]✓ You have {len(projects)} projects registered[/#00ff00]\n")
    else:
        console.print("[yellow]No projects registered yet[/yellow]")
        choice = Prompt.ask(
            "[#ff00ff]What would you like to do?[/#ff00ff]",
            choices=["add", "import", "skip"],
            default="import"
        )
        if choice == "add":
            name = Prompt.ask("Project name")
            path = Prompt.ask("Project path")
            add_project(name, path)
        elif choice == "import":
            import_projects()
        console.print()
    
    # Step 4: AI Tools
    console.print("[bold #ff00ff]Step 4: AI Tools[/bold #ff00ff]")
    tools_status = check_all_tools()
    installed = sum(tools_status.values())
    if installed > 0:
        console.print(f"[#00ff00]✓ {installed}/5 AI tools detected[/#00ff00]\n")
    else:
        console.print("[yellow]No AI tools detected[/yellow]")
        console.print("[dim]SAOIS will open browser URLs as fallback[/dim]\n")
    
    # Step 5: Next actions
    console.print("[bold #ff00ff]Step 5: Next Steps[/bold #ff00ff]")
    console.print("[#00ffff]1.[/#00ffff] Validate projects: [bold]saois validate[/bold]")
    console.print("[#00ffff]2.[/#00ffff] Create project brains: [bold]saois init-brains[/bold]")
    console.print("[#00ffff]3.[/#00ffff] Check system health: [bold]saois doctor[/bold]")
    console.print("[#00ffff]4.[/#00ffff] Start working: [bold]saois run PROJECT[/bold]\n")
    
    console.print("[#00ff00]✓ Quickstart complete! You're ready to use SAOIS.[/#00ff00]")
    console.print("[dim]Run [bold]saois help[/bold] to see all commands.[/dim]")

def validate_projects():
    """Validate all project paths and offer to fix issues."""
    show_header()
    
    console.print("[bold #00ffff]🔍 Project Validation[/bold #00ffff]\n")
    
    projects = load_projects()
    if not projects:
        console.print("[yellow]No projects to validate[/yellow]")
        console.print("[dim]Add projects with: [bold]saois add[/bold] or [bold]saois import[/bold][/dim]")
        return
    
    console.print(f"[dim]Checking {len(projects)} projects...[/dim]\n")
    
    valid = []
    missing = []
    
    for name, path in projects.items():
        if Path(path).exists():
            valid.append((name, path))
        else:
            missing.append((name, path))
    
    # Show valid projects
    if valid:
        console.print(f"[#00ff00]✓ {len(valid)} projects are valid[/#00ff00]")
        for name, _ in valid[:3]:
            console.print(f"  [#00ff00]✓[/#00ff00] {name}")
        if len(valid) > 3:
            console.print(f"  [dim]... and {len(valid) - 3} more[/dim]")
        console.print()
    
    # Handle missing projects
    if missing:
        console.print(f"[yellow]⚠️  {len(missing)} projects have missing paths:[/yellow]\n")
        
        # Offer bulk actions
        if len(missing) > 5:
            bulk_action = Prompt.ask(
                f"[#ff00ff]Handle {len(missing)} missing projects?[/#ff00ff]",
                choices=["one-by-one", "archive-all", "remove-all", "skip-all"],
                default="one-by-one"
            )
            
            if bulk_action == "archive-all":
                archive_dir = CONFIG_DIR / "archived_projects"
                archive_dir.mkdir(exist_ok=True)
                archived = archive_dir / "projects.json"
                archived_data = json.loads(archived.read_text()) if archived.exists() else {}
                
                for name, path in missing:
                    archived_data[name] = path
                    del projects[name]
                
                archived.write_text(json.dumps(archived_data, indent=2))
                save_projects(projects)
                console.print(f"\n[#ff00ff]✓ Archived {len(missing)} projects[/#ff00ff]")
                console.print(f"[dim]Location: {archived}[/dim]")
                return
            
            elif bulk_action == "remove-all":
                if Confirm.ask(f"[red]Really remove all {len(missing)} projects?[/red]", default=False):
                    for name, _ in missing:
                        del projects[name]
                    save_projects(projects)
                    console.print(f"\n[red]✓ Removed {len(missing)} projects[/red]")
                return
            
            elif bulk_action == "skip-all":
                console.print("[dim]Skipped validation[/dim]")
                return
        
        archive_dir = CONFIG_DIR / "archived_projects"
        log_file = CONFIG_DIR / "validation_log.txt"
        
        for name, path in missing:
            console.print(f"[bold #ff00ff]{name}[/bold #ff00ff]")
            console.print(f"[dim]  Missing: {path}[/dim]")
            
            choice = Prompt.ask(
                "  [#ff00ff]Action?[/#ff00ff]",
                choices=["fix", "skip", "archive", "remove", "later"],
                default="skip"
            )
            
            if choice == "fix":
                new_path = Prompt.ask("  Enter correct path")
                new_path = str(Path(new_path).expanduser().resolve())
                if Path(new_path).exists():
                    projects[name] = new_path
                    save_projects(projects)
                    console.print(f"  [#00ff00]✓ Updated path for {name}[/#00ff00]\n")
                else:
                    console.print(f"  [red]✗ Path still doesn't exist[/red]\n")
            
            elif choice == "archive":
                archive_dir.mkdir(exist_ok=True)
                archived = archive_dir / "projects.json"
                
                archived_data = {}
                if archived.exists():
                    archived_data = json.loads(archived.read_text())
                
                archived_data[name] = path
                archived.write_text(json.dumps(archived_data, indent=2))
                
                del projects[name]
                save_projects(projects)
                console.print(f"  [#ff00ff]✓ Archived {name}[/#ff00ff]\n")
            
            elif choice == "remove":
                del projects[name]
                save_projects(projects)
                console.print(f"  [red]✓ Removed {name}[/red]\n")
            
            elif choice == "later":
                console.print(f"  [dim]Skipped for now[/dim]\n")
                # Log for future reference
                log_error_to_file(name, {
                    "project_type": "validation",
                    "command": "validate",
                    "simplified": f"Project path missing: {path}",
                    "full_error": f"Path does not exist: {path}",
                    "recommendation": "Update path or remove project",
                    "ai_prompt": "N/A"
                }, CONFIG_DIR)
                break
            
            else:  # skip
                console.print(f"  [dim]Skipped[/dim]\n")
        
        if choice != "later":
            console.print(f"\n[#00ff00]✓ Validation complete![/#00ff00]")
            valid_count = len([n for n, p in projects.items() if Path(p).exists()])
            archived_path = str(archive_dir / 'projects.json') if archive_dir.exists() else 'None'
            console.print(f"[dim]Valid: {valid_count} | Archived: {archived_path}[/dim]")
    else:
        console.print("[#00ff00]✓ All projects are valid![/#00ff00]")

def init_all_brains():
    """Create project_brain.md for all projects that don't have one."""
    show_header()
    
    console.print("[bold #00ffff]🧠 Initialize Project Brains[/bold #00ffff]\n")
    
    projects = load_projects()
    if not projects:
        console.print("[yellow]No projects to initialize[/yellow]")
        return
    
    # Check which projects need brains
    needs_brain = []
    has_brain = []
    
    for name, path in projects.items():
        project_path = Path(path)
        if not project_path.exists():
            continue
        
        brain_file = project_path / "docs" / "project_brain.md"
        if brain_file.exists():
            has_brain.append(name)
        else:
            needs_brain.append((name, project_path))
    
    if has_brain:
        console.print(f"[#00ff00]✓ {len(has_brain)} projects already have brains[/#00ff00]\n")
    
    if not needs_brain:
        console.print("[#00ff00]✓ All projects have project brains![/#00ff00]")
        return
    
    console.print(f"[yellow]{len(needs_brain)} projects need project brains[/yellow]\n")
    
    # Ask if user wants to customize template
    use_custom = Confirm.ask("Do you want to customize the template?", default=False)
    
    template = get_project_brain_template()
    
    if use_custom:
        console.print("\n[dim]Current template:[/dim]")
        console.print(Panel(template, border_style="#ff00ff", box=box.ROUNDED))
        console.print()
        
        if Confirm.ask("Edit this template?", default=False):
            console.print("[dim]Opening template in editor... (save and close when done)[/dim]")
            temp_file = CONFIG_DIR / "temp_template.md"
            temp_file.write_text(template)
            
            import os
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.run([editor, str(temp_file)])
            
            if temp_file.exists():
                template = temp_file.read_text()
                temp_file.unlink()
                console.print("[#00ff00]✓ Template updated[/#00ff00]\n")
    
    # Create brains
    created = 0
    skipped = 0
    
    for name, project_path in needs_brain:
        console.print(f"[bold #ff00ff]{name}[/bold #ff00ff]")
        console.print(f"[dim]  {project_path}[/dim]")
        
        choice = Prompt.ask(
            "  [#ff00ff]Action?[/#ff00ff]",
            choices=["create", "skip", "later"],
            default="create"
        )
        
        if choice == "create":
            docs_dir = project_path / "docs"
            docs_dir.mkdir(exist_ok=True)
            
            brain_file = docs_dir / "project_brain.md"
            
            # Customize template with project name
            customized = template.replace("[Your project name]", name)
            customized = customized.replace("[Your project name here]", name)
            
            brain_file.write_text(customized)
            console.print(f"  [#00ff00]✓ Created project brain[/#00ff00]\n")
            created += 1
        
        elif choice == "later":
            console.print(f"  [dim]Stopping here. Run again to continue.[/dim]\n")
            break
        
        else:
            console.print(f"  [dim]Skipped[/dim]\n")
            skipped += 1
    
    console.print(f"\n[#00ff00]✓ Initialization complete![/#00ff00]")
    console.print(f"[dim]Created: {created} | Skipped: {skipped}[/dim]")
    
    if created > 0:
        console.print("\n[#00ffff]💡 Next steps:[/#00ffff]")
        console.print("  1. Edit each project_brain.md with your project details")
        console.print("  2. Set the NEXT TASK TYPE (coding, research, etc.)")
        console.print("  3. Run [bold]saois run PROJECT[/bold] to start working")

def configure_tools():
    """Configure which AI tools to use for each task."""
    show_header()
    from .tool_config import show_tool_selection_menu, configure_task_mapping, show_current_config
    
    console.print("[bold #00ffff]⚙️  AI Tools Configuration[/bold #00ffff]\n")
    console.print("[dim]Configure which tools SAOIS uses for different tasks.[/dim]\n")
    
    menu_choice = Prompt.ask(
        "[#ff00ff]What would you like to do?[/#ff00ff]",
        choices=["view", "configure", "back"],
        default="view"
    )
    
    if menu_choice == "view":
        show_current_config()
    elif menu_choice == "configure":
        configure_task_mapping()
    else:
        console.print("[dim]Cancelled[/dim]")

def setup_all_tools():
    """Complete AI tools installation wizard."""
    show_header()
    install_all_ai_tools()

def git_push_project(name):
    """Automated git commit and push for a project."""
    show_header()
    projects = load_projects()
    
    if name not in projects:
        console.print(f"[red]✗ Project '{name}' not found[/red]")
        return
    
    project_path = Path(projects[name])
    auto_commit_and_push(project_path)

def uninstall_cli():
    show_header()
    
    console.print("[bold #ff00ff]🗑️  SAOIS Complete Uninstaller[/bold #ff00ff]\n")
    console.print("[red]⚠️  WARNING: This will completely remove SAOIS from your system[/red]\n")
    console.print("[dim]This will delete:[/dim]")
    console.print("  • SAOIS command alias from ALL shell configs")
    console.print("  • ~/.saois/ directory (all projects, settings, logs)")
    console.print("  • ~/.saois-cli/ directory (if exists)")
    console.print("  • Installation markers and cache")
    console.print("  • Python package installation\n")
    
    if not Confirm.ask("[yellow]Are you SURE you want to completely remove SAOIS?[/yellow]", default=False):
        console.print("[dim]Cancelled[/dim]")
        return
    
    import shutil
    removed_items = []
    
    # 1. Remove from ALL shell configs
    console.print("\n[#00ffff]Step 1: Removing from shell configurations...[/#00ffff]")
    shell_configs = [
        Path.home() / ".zshrc",
        Path.home() / ".bashrc",
        Path.home() / ".bash_profile",
        Path.home() / ".profile"
    ]
    
    for shell_rc in shell_configs:
        if not shell_rc.exists():
            continue
        
        try:
            content = shell_rc.read_text()
            lines = content.split("\n")
            
            # Remove ALL SAOIS-related lines
            new_lines = []
            for line in lines:
                # Skip any line containing saois
                if "saois" in line.lower() or "# SAOIS" in line:
                    continue
                new_lines.append(line)
            
            new_content = "\n".join(new_lines)
            if new_content != content:
                shell_rc.write_text(new_content)
                removed_items.append(f"✓ Cleaned {shell_rc.name}")
        except Exception as e:
            console.print(f"[yellow]  ⚠️  Could not modify {shell_rc.name}: {e}[/yellow]")
    
    # 2. Remove ~/.saois directory
    console.print("\n[#00ffff]Step 2: Removing configuration directory...[/#00ffff]")
    if CONFIG_DIR.exists():
        try:
            shutil.rmtree(CONFIG_DIR)
            removed_items.append(f"✓ Deleted {CONFIG_DIR}")
        except Exception as e:
            console.print(f"[yellow]  ⚠️  Could not remove {CONFIG_DIR}: {e}[/yellow]")
    
    # 3. Remove ~/.saois-cli directory (if installed there)
    console.print("\n[#00ffff]Step 3: Removing installation directory...[/#00ffff]")
    saois_cli_dir = Path.home() / ".saois-cli"
    if saois_cli_dir.exists():
        try:
            shutil.rmtree(saois_cli_dir)
            removed_items.append(f"✓ Deleted {saois_cli_dir}")
        except Exception as e:
            console.print(f"[yellow]  ⚠️  Could not remove {saois_cli_dir}: {e}[/yellow]")
    
    # 4. Remove Python package
    console.print("\n[#00ffff]Step 4: Uninstalling Python package...[/#00ffff]")
    try:
        result = subprocess.run(
            ["pip3", "uninstall", "-y", "saois"],
            capture_output=True,
            text=True
        )
        if "Successfully uninstalled" in result.stdout or "not installed" in result.stderr:
            removed_items.append("✓ Uninstalled Python package")
    except Exception as e:
        console.print(f"[yellow]  ⚠️  Could not uninstall package: {e}[/yellow]")
    
    # 5. Remove .egg-info and build artifacts
    console.print("\n[#00ffff]Step 5: Cleaning build artifacts...[/#00ffff]")
    current_dir = Path.cwd()
    artifacts = [
        current_dir / "saois.egg-info",
        current_dir / "build",
        current_dir / "dist",
        current_dir / "__pycache__"
    ]
    
    for artifact in artifacts:
        if artifact.exists():
            try:
                if artifact.is_dir():
                    shutil.rmtree(artifact)
                else:
                    artifact.unlink()
                removed_items.append(f"✓ Deleted {artifact.name}")
            except:
                pass
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold #00ff00]✓ SAOIS Completely Uninstalled![/bold #00ff00]")
    console.print("="*60 + "\n")
    
    if removed_items:
        console.print("[#00ffff]Removed:[/#00ffff]")
        for item in removed_items:
            console.print(f"  {item}")
    
    console.print("\n[dim]Final steps:[/dim]")
    console.print("  1. Reload shell: [bold]source ~/.zshrc[/bold] (or ~/.bashrc)")
    console.print("  2. Verify removal: [bold]saois help[/bold] (should show 'command not found')")
    console.print("\n[#00ffff]To reinstall:[/#00ffff]")
    console.print("  cd /path/to/SAOISCLI && ./install.sh")
    console.print("\n[green]✓ System is clean - no SAOIS traces remaining[/green]")

def main():
    parser = argparse.ArgumentParser(
        description="⚡ SAOIS - Futuristic CLI for managing development projects",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subparsers.add_parser("help", help="Show help and all commands")
    subparsers.add_parser("quickstart", help="Interactive quickstart guide")
    subparsers.add_parser("setup", help="Setup wizard for tool routing")
    subparsers.add_parser("install", help="Install SAOIS globally")
    subparsers.add_parser("uninstall", help="Uninstall SAOIS")
    subparsers.add_parser("list", help="Show all projects")
    subparsers.add_parser("import", help="Import projects from a folder")
    subparsers.add_parser("validate", help="Validate and fix project paths")
    subparsers.add_parser("init-brains", help="Create project brains for all projects")
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
    
    git_push_parser = subparsers.add_parser("git-push", help="Commit and push to GitHub")
    git_push_parser.add_argument("name", help="Project name")
    
    setup_tools_parser = subparsers.add_parser("setup-tools", help="Install AI tools")
    config_tools_parser = subparsers.add_parser("config-tools", help="Configure which AI tools to use")
    menu_parser = subparsers.add_parser("menu", help="Interactive menu (beginner-friendly)")
    prompts_parser = subparsers.add_parser("prompts", help="Browse AI prompt templates")
    prompts_parser.add_argument("template", nargs="?", help="Template name or 'browse'")
    
    args = parser.parse_args()
    
    if args.command == "help":
        show_help()
    elif args.command == "quickstart":
        run_quickstart()
    elif args.command == "setup":
        run_setup_wizard()
    elif args.command == "validate":
        validate_projects()
    elif args.command == "init-brains":
        init_all_brains()
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
    elif args.command == "git-push":
        git_push_project(args.name)
    elif args.command == "setup-tools":
        setup_all_tools()
    elif args.command == "config-tools":
        configure_tools()
    elif args.command == "menu":
        cmd = show_interactive_menu()
        if cmd:
            # Re-run with the selected command
            import sys
            sys.argv = ['saois', cmd]
            main()
    elif args.command == "prompts":
        from .prompt_library import list_prompt_templates, browse_prompts, show_prompt_template
        if args.template:
            if args.template == "browse":
                browse_prompts()
            else:
                show_prompt_template(args.template)
        else:
            list_prompt_templates()
    else:
        show_help()

if __name__ == "__main__":
    main()
