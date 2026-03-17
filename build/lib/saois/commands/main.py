"""
SAOIS Main Commands
Simplified command handlers - only 6 essential commands.
"""
import sys
from pathlib import Path
from typing import Optional

from ..core.config import config
from ..core.registry import registry
from ..core.brain import Brain
from ..core.router import router
from ..core.ui import ui, console


def cmd_start():
    """
    Quick setup command - gets user started in 30 seconds.
    Combines: setup, import, init-brains, setup-tools into ONE command.
    """
    ui.header()
    console.print(f"[bold {ui.PRIMARY}]🚀 Let's get you started![/bold {ui.PRIMARY}]\n")
    
    # Step 1: Check/create AI_PROJECTS folder
    console.print(f"[bold]Step 1: Projects Folder[/bold]")
    ai_path = config.get_ai_projects_path()
    
    if ai_path:
        ui.success(f"Found: {ai_path}")
    else:
        # Create default folder
        default_path = Path.home() / "Documents" / "AI_PROJECTS"
        if ui.confirm(f"Create projects folder at {default_path}?"):
            default_path.mkdir(parents=True, exist_ok=True)
            config.set_ai_projects_path(default_path)
            ui.success(f"Created: {default_path}")
            ai_path = default_path
        else:
            # Ask for custom path
            custom = ui.ask("Enter your projects folder path")
            custom_path = Path(custom).expanduser()
            custom_path.mkdir(parents=True, exist_ok=True)
            config.set_ai_projects_path(custom_path)
            ui.success(f"Set: {custom_path}")
            ai_path = custom_path
    
    console.print()
    
    # Step 2: Auto-import projects
    console.print(f"[bold]Step 2: Finding Projects[/bold]")
    
    if ai_path:
        found = registry.scan_folder(ai_path)
        if found:
            count = registry.import_projects(found)
            ui.success(f"Found {len(found)} projects, imported {count} new")
        else:
            ui.dim("No projects found yet - add them with 'saois add NAME PATH'")
    
    console.print()
    
    # Step 3: Check AI tools
    console.print(f"[bold]Step 3: AI Tools[/bold]")
    tools = config.get_installed_tools()
    installed = sum(tools.values())
    
    if installed > 0:
        ui.success(f"{installed} AI tools ready")
        for tool, is_installed in tools.items():
            if is_installed:
                console.print(f"  [green]✓[/green] {tool.title()}")
    else:
        ui.warning("No AI tools detected - SAOIS will open browser versions")
        ui.dim("Install Windsurf, Cursor, or VS Code for best experience")
    
    console.print()
    
    # Done!
    console.print(f"[bold {ui.SUCCESS}]✓ Setup complete![/bold {ui.SUCCESS}]\n")
    
    # Show next steps
    projects = registry.get_all()
    if projects:
        first_project = list(projects.keys())[0]
        console.print(f"[bold]Next:[/bold] Run [cyan]saois work {first_project}[/cyan] to start working!")
    else:
        console.print(f"[bold]Next:[/bold] Add a project with [cyan]saois add myapp ~/path/to/project[/cyan]")


def cmd_work(project_name: str):
    """
    Start working on a project - the main command.
    Auto-creates brain if needed, launches best AI tool.
    """
    ui.header()
    
    # Find project
    project_path = registry.get(project_name)
    
    if not project_path:
        ui.error(f"Project '{project_name}' not found")
        
        # Suggest similar projects
        projects = registry.get_all()
        if projects:
            matches = registry.search(project_name)
            if matches:
                ui.dim(f"Did you mean: {', '.join(matches[:3])}")
            else:
                ui.dim(f"Available: {', '.join(list(projects.keys())[:5])}")
        else:
            ui.tip("Run 'saois start' to set up your projects")
        return
    
    if not project_path.exists():
        ui.error(f"Project folder not found: {project_path}")
        ui.tip("Run 'saois list' to check your projects")
        return
    
    # Check/create brain
    brain = Brain(project_path)
    
    if not brain.exists() or brain.is_template():
        console.print(f"[{ui.WARNING}]Setting up project for first use...[/{ui.WARNING}]")
        
        # Ask what they're working on
        task_type = ui.ask(
            "What are you working on?",
            choices=["code", "research", "plan"],
            default="code"
        )
        
        # Create brain
        brain.create(task_type)
        ui.success("Project configured!")
        console.print()
    
    # Get task info
    task_type = brain.get_task_type()
    current_task = brain.get_current_task()
    
    # Show project info
    console.print(f"[bold {ui.PRIMARY}]🚀 Starting Work[/bold {ui.PRIMARY}]\n")
    console.print(f"[{ui.SECONDARY}]Project:[/{ui.SECONDARY}] {project_name}")
    console.print(f"[{ui.SECONDARY}]Task:[/{ui.SECONDARY}] {task_type}")
    if current_task and "[" not in current_task:  # Not a template placeholder
        console.print(f"[{ui.SECONDARY}]Working on:[/{ui.SECONDARY}] {current_task[:60]}...")
    console.print()
    
    # Launch tool
    success, message, tool_name, _ = router.launch_for_project(project_path)
    
    if success:
        ui.success(f"{tool_name} is ready!")
        ui.tip(f"Your project is open in {tool_name}")
    else:
        ui.error(message)


def cmd_list():
    """Show all projects."""
    ui.header()
    
    # Auto-validate and show warnings
    valid, missing = registry.validate()
    
    if missing:
        ui.warning(f"{len(missing)} projects have missing paths")
        if ui.confirm("Archive missing projects?"):
            count = registry.archive_missing()
            ui.success(f"Archived {count} projects")
            console.print()
    
    # Show projects
    projects = registry.get_all()
    ui.project_list(projects)
    
    if projects:
        ui.tip("Run 'saois work <name>' to start working on a project")


def cmd_add(name: str, path: str):
    """Add a new project."""
    ui.header()
    
    project_path = Path(path).expanduser().resolve()
    
    if not project_path.exists():
        ui.warning(f"Path not found: {project_path}")
        if not ui.confirm("Add anyway?", default=False):
            ui.dim("Cancelled")
            return
    
    registry.add(name, project_path)
    ui.success(f"Added '{name}'")
    ui.dim(str(project_path))
    
    # Offer to start working
    if project_path.exists():
        if ui.confirm("Start working on it now?"):
            cmd_work(name)


def cmd_tools():
    """Show AI tools status."""
    ui.header()
    
    tools = config.get_installed_tools()
    ui.tool_status(tools)
    
    installed = sum(tools.values())
    if installed == 0:
        console.print(f"\n[{ui.WARNING}]No desktop AI tools found[/{ui.WARNING}]")
        console.print(f"[{ui.DIM}]SAOIS will open browser versions instead[/{ui.DIM}]")
        console.print(f"\n[bold]Recommended tools:[/bold]")
        console.print(f"  • [cyan]Windsurf[/cyan] - https://windsurf.ai")
        console.print(f"  • [cyan]Cursor[/cyan] - https://cursor.sh")
        console.print(f"  • [cyan]VS Code[/cyan] - https://code.visualstudio.com")


def cmd_help():
    """Show help."""
    ui.help_commands()


def cmd_remove(name: str):
    """Remove a project from registry."""
    ui.header()
    
    if not registry.exists(name):
        ui.error(f"Project '{name}' not found")
        return
    
    if ui.confirm(f"Remove '{name}' from SAOIS?", default=False):
        registry.remove(name)
        ui.success(f"Removed '{name}'")
        ui.dim("(Project files were not deleted)")


def cmd_open(name: str):
    """Open project folder."""
    import subprocess
    
    project_path = registry.get(name)
    
    if not project_path:
        ui.error(f"Project '{name}' not found")
        return
    
    os_type = config.get_os()
    
    try:
        if os_type == "windows":
            subprocess.run(["explorer", str(project_path)], check=True)
        elif os_type == "macos":
            subprocess.run(["open", str(project_path)], check=True)
        else:
            subprocess.run(["xdg-open", str(project_path)], check=True)
        ui.success(f"Opened {name}")
    except Exception as e:
        ui.error(f"Could not open folder: {e}")


def cmd_import():
    """Import projects from a folder."""
    ui.header()
    
    console.print(f"[bold {ui.PRIMARY}]Import Projects[/bold {ui.PRIMARY}]\n")
    
    # Get folder path
    default_path = config.get_ai_projects_path()
    folder = ui.ask("Folder to scan", default=str(default_path) if default_path else "")
    
    folder_path = Path(folder).expanduser()
    
    if not folder_path.exists():
        ui.error(f"Folder not found: {folder_path}")
        return
    
    # Scan for projects
    found = registry.scan_folder(folder_path)
    
    if not found:
        ui.warning("No projects found in that folder")
        return
    
    console.print(f"\n[{ui.SUCCESS}]Found {len(found)} projects:[/{ui.SUCCESS}]\n")
    
    for i, name in enumerate(found.keys(), 1):
        console.print(f"  [{ui.DIM}]{i}.[/{ui.DIM}] [{ui.PRIMARY}]{name}[/{ui.PRIMARY}]")
    
    console.print()
    
    # Import all or select
    choice = ui.ask("Import which?", choices=["all", "none"], default="all")
    
    if choice == "all":
        count = registry.import_projects(found)
        ui.success(f"Imported {count} new projects")
    else:
        ui.dim("Cancelled")


# Legacy command aliases for backward compatibility
def cmd_run(name: str):
    """Alias for 'work' command."""
    cmd_work(name)


def cmd_doctor():
    """Alias for 'tools' command."""
    cmd_tools()


def cmd_quickstart():
    """Alias for 'start' command."""
    cmd_start()


def cmd_setup():
    """Alias for 'start' command."""
    cmd_start()


def run_command(args):
    """Main command dispatcher."""
    if len(args) < 2:
        # No command - show welcome or help
        projects = registry.get_all()
        if not projects:
            ui.welcome()
        else:
            cmd_help()
        return
    
    command = args[1].lower()
    
    # Main commands (simplified)
    if command in ["start", "setup", "quickstart", "init"]:
        cmd_start()
    
    elif command in ["work", "run", "go"]:
        if len(args) < 3:
            ui.error("Please specify a project name")
            ui.dim("Usage: saois work <project-name>")
            return
        cmd_work(args[2])
    
    elif command in ["list", "ls", "projects"]:
        cmd_list()
    
    elif command == "add":
        if len(args) < 4:
            ui.error("Please specify name and path")
            ui.dim("Usage: saois add <name> <path>")
            return
        cmd_add(args[2], args[3])
    
    elif command in ["tools", "doctor", "check"]:
        cmd_tools()
    
    elif command in ["help", "-h", "--help", "?"]:
        cmd_help()
    
    elif command in ["remove", "rm", "delete"]:
        if len(args) < 3:
            ui.error("Please specify a project name")
            return
        cmd_remove(args[2])
    
    elif command == "open":
        if len(args) < 3:
            ui.error("Please specify a project name")
            return
        cmd_open(args[2])
    
    elif command == "import":
        cmd_import()
    
    else:
        # Unknown command - maybe it's a project name?
        if registry.exists(command):
            cmd_work(command)
        else:
            ui.error(f"Unknown command: {command}")
            ui.tip("Run 'saois help' to see available commands")
