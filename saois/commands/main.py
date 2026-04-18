"""
SAOIS Main Commands
Simplified command handlers - only 6 essential commands.
"""
from pathlib import Path
from typing import Optional

from ..core.config import LAUNCH_BROWSER, LAUNCH_DESKTOP, config
from ..core.registry import registry
from ..core.brain import Brain
from ..core.router import router
from ..core.ui import ui, console


def _maybe_confirm_projects_root(path: Path) -> Path:
    """Warn on volume roots or very large scan directories; return possibly updated path."""
    need, reason = config.projects_folder_needs_confirmation(path)
    if not need:
        return path
    ui.warning(f"Projects folder: {reason}")
    if ui.confirm("Use this folder anyway?", default=True):
        return path
    alt = ui.ask("Enter a narrower projects folder path", default=str(path))
    new_path = Path(alt).expanduser().resolve()
    if not new_path.exists():
        new_path.mkdir(parents=True, exist_ok=True)
    config.set_ai_projects_path(new_path)
    return new_path


def cmd_start():
    """Quick setup: folder, import, tool check."""
    ui.header()
    console.print(f"[bold {ui.PRIMARY}]🚀 Let's get you started![/bold {ui.PRIMARY}]\n")

    console.print("[bold]Step 1: Projects Folder[/bold]")
    ai_path = config.get_ai_projects_path()

    if ai_path:
        ui.success(f"Found: {ai_path}")
        ai_path = _maybe_confirm_projects_root(ai_path)
    else:
        default_path = Path.home() / "Documents" / "AI_PROJECTS"
        if ui.confirm(f"Create projects folder at {default_path}?"):
            default_path.mkdir(parents=True, exist_ok=True)
            config.set_ai_projects_path(default_path)
            ui.success(f"Created: {default_path}")
            ai_path = default_path
        else:
            custom = ui.ask("Enter your projects folder path")
            custom_path = Path(custom).expanduser()
            custom_path.mkdir(parents=True, exist_ok=True)
            config.set_ai_projects_path(custom_path)
            ui.success(f"Set: {custom_path}")
            ai_path = custom_path
        ai_path = _maybe_confirm_projects_root(ai_path)

    console.print()
    console.print("[bold]Step 2: Finding Projects[/bold]")

    if ai_path:
        found = registry.scan_folder(ai_path)
        if found:
            new_ct, already_ct = registry.import_projects(found)
            parts = [
                f"Scanned [bold]{len(found)}[/bold] project folders in this directory."
            ]
            if new_ct:
                parts.append(f"[green]{new_ct} newly added[/green] to your SAOIS registry.")
            if already_ct:
                parts.append(f"[dim]{already_ct} were already registered.[/dim]")
            console.print(" ".join(parts))
        else:
            ui.dim("No projects found yet - add them with 'saois add NAME PATH'")

    console.print()
    console.print("[bold]Step 3: AI Tools[/bold]")
    tools = config.get_installed_tools()
    installed = sum(tools.values())

    if installed > 0:
        ui.success(f"{installed} AI tool(s) detected")
        for tool_id, is_on in tools.items():
            if is_on:
                console.print(f"  [green]✓[/green] {config.TOOL_NAMES.get(tool_id, tool_id)}")
    else:
        ui.warning("No desktop AI tools detected — `saois work` will open vendor sites in your browser.")
        ui.dim("Install Windsurf, Cursor, or VS Code for full IDE launches.")

    console.print()
    console.print(f"[bold {ui.SUCCESS}]✓ Setup complete![/bold {ui.SUCCESS}]\n")

    projects = registry.get_all()
    if projects:
        first_project = list(projects.keys())[0]
        console.print(
            f"[bold]Next:[/bold] Run [cyan]saois work {first_project}[/cyan] to start working!"
        )
    else:
        console.print(
            f"[bold]Next:[/bold] Add a project with [cyan]saois add myapp ~/path/to/project[/cyan]"
        )


def _print_brain_next_steps(brain: Brain, project_path: Path):
    run_cmd = brain.get_run_command()
    if run_cmd and "[" not in run_cmd:
        ui.dim(f"Next (from brain): [cyan]cd {project_path}[/cyan] then run [cyan]{run_cmd}[/cyan]")
    if not brain.is_canonical_location() and brain.exists():
        try:
            rel = brain.brain_file.relative_to(project_path)
            ui.dim(
                f"Brain file is at [cyan]{rel}[/cyan]. Consider [cyan]docs/project_brain.md[/cyan] for consistency."
            )
        except ValueError:
            pass
    ui.dim("Edit task type in docs/project_brain.md: code | research | plan")


def cmd_work(project_name: str):
    """Start working on a project."""
    ui.header()

    project_path = registry.get(project_name)

    if not project_path:
        ui.error(f"Project '{project_name}' not found")
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

    brain = Brain(project_path)

    if not brain.exists() or brain.is_template():
        console.print(f"[{ui.WARNING}]Setting up project for first use...[/{ui.WARNING}]")
        task_type = ui.ask(
            "What are you working on?",
            choices=["code", "research", "plan"],
            default="code",
        )
        brain.create(task_type)
        ui.success("Project configured!")
        console.print()

    task_type = brain.get_task_type()
    current_task = brain.get_current_task()

    console.print(f"[bold {ui.PRIMARY}]🚀 Starting Work[/bold {ui.PRIMARY}]\n")
    console.print(f"[{ui.SECONDARY}]Project:[/{ui.SECONDARY}] {project_name}")
    console.print(f"[{ui.SECONDARY}]Task:[/{ui.SECONDARY}] {task_type}")
    if current_task and "[" not in current_task:
        console.print(
            f"[{ui.SECONDARY}]Working on:[/{ui.SECONDARY}] {current_task[:200]}{'…' if len(current_task) > 200 else ''}"
        )
    console.print()

    success, message, tool_name, _, launch_mode = router.launch_for_project(project_path)

    if success:
        if launch_mode == LAUNCH_DESKTOP:
            ui.success(message)
            ui.tip(f"{tool_name} should open with folder: {project_path}")
        else:
            ui.warning(message)
            ui.tip("Install the desktop app or use `saois open <project>` to open the folder in Finder.")
        _print_brain_next_steps(brain, project_path)
    else:
        ui.error(message)


def cmd_list():
    """Show all projects."""
    ui.header()

    valid, missing = registry.validate()

    if missing:
        ui.warning(f"{len(missing)} projects have missing paths")
        if ui.confirm("Archive missing projects?"):
            count = registry.archive_missing()
            ui.success(f"Archived {count} projects")
            console.print()

    projects = registry.get_all()
    ui.project_list(projects)

    if projects:
        ui.tip("Run 'saois work <name>' to start working on a project")


def cmd_add(name: str, path: str):
    """Add a new project."""
    ui.header()

    project_path = Path(path).expanduser().resolve()

    if registry.exists(name):
        old = registry.get(name)
        if old and old.resolve() != project_path:
            ui.warning(
                f"Project '{name}' was registered at a different path; updating to the new path."
            )

    if not project_path.exists():
        ui.warning(f"Path not found: {project_path}")
        if not ui.confirm("Add anyway?", default=False):
            ui.dim("Cancelled")
            return

    registry.add(name, project_path)
    ui.success(f"Added '{name}'")
    ui.dim(str(project_path))

    if project_path.exists():
        if ui.confirm("Start working on it now?"):
            cmd_work(name)


def cmd_tools(verbose: bool = False):
    """Show AI tools status."""
    ui.header()

    tools = config.get_installed_tools()
    ui.tool_status(tools, tool_names=config.TOOL_NAMES)

    if verbose:
        console.print(f"\n[bold {ui.PRIMARY}]Detection detail[/bold {ui.PRIMARY}]\n")
        for tid in config.TOOL_NAMES:
            console.print(
                f"  [cyan]{config.TOOL_NAMES[tid]}[/cyan]: {config.explain_tool_detection(tid)}"
            )

    installed = sum(tools.values())
    if installed == 0:
        console.print(f"\n[{ui.WARNING}]No desktop AI tools found[/{ui.WARNING}]")
        console.print(
            f"[{ui.DIM}]`saois work` will open vendor websites until an app is detected.[/{ui.DIM}]"
        )
        console.print("\n[bold]Recommended tools:[/bold]")
        console.print("  • [cyan]Windsurf[/cyan] - https://windsurf.ai")
        console.print("  • [cyan]Cursor[/cyan] - https://cursor.sh")
        console.print("  • [cyan]VS Code[/cyan] - https://code.visualstudio.com")


def cmd_help():
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

    default_path = config.get_ai_projects_path()
    folder = ui.ask("Folder to scan", default=str(default_path) if default_path else "")

    folder_path = Path(folder).expanduser()

    if not folder_path.exists():
        ui.error(f"Folder not found: {folder_path}")
        return

    found = registry.scan_folder(folder_path)

    if not found:
        ui.warning("No projects found in that folder")
        return

    console.print(f"\n[{ui.SUCCESS}]Found {len(found)} projects:[/{ui.SUCCESS}]\n")

    for i, name in enumerate(found.keys(), 1):
        console.print(f"  [{ui.DIM}]{i}.[/{ui.DIM}] [{ui.PRIMARY}]{name}[/{ui.PRIMARY}]")

    console.print()

    choice = ui.ask("Import which?", choices=["all", "none"], default="all")

    if choice == "all":
        new_ct, already_ct = registry.import_projects(found)
        msg = f"Added {new_ct} new project(s)"
        if already_ct:
            msg += f"; {already_ct} already in registry"
        ui.success(msg)
    else:
        ui.dim("Cancelled")


def cmd_suggest(project_name: str):
    """Print brain-driven suggestions without launching tools."""
    ui.header()
    project_path = registry.get(project_name)
    if not project_path or not project_path.exists():
        ui.error(f"Project '{project_name}' not found or path missing")
        return
    brain = Brain(project_path)
    if not brain.exists():
        ui.warning("No project brain yet — run `saois work` once to create it.")
        return
    console.print(f"[bold]{project_name}[/bold] — task: {brain.get_task_type()}\n")
    ct = brain.get_current_task()
    if ct:
        console.print(f"[dim]Current task:[/dim]\n{ct}\n")
    _print_brain_next_steps(brain, project_path)


def cmd_prompts(template_arg: Optional[str]):
    """List or show AI prompt templates (no legacy cli required)."""
    from ..prompt_library import browse_prompts, list_prompt_templates, show_prompt_template

    if not template_arg:
        list_prompt_templates()
        return
    if template_arg.lower() == "browse":
        browse_prompts()
        return
    show_prompt_template(template_arg)


def cmd_experts(args):
    """Manage expert personas for AI tools."""
    from ..experts_cli import list_experts, install_experts, show_expert, browse_experts
    
    action = args[0] if args else "list"
    
    if action == "list":
        list_experts()
    elif action == "browse":
        browse_experts()
    elif action == "install":
        project_name = args[1] if len(args) > 1 else None
        specific = None
        for i, a in enumerate(args):
            if a == "--only" and i + 1 < len(args):
                specific = args[i + 1].split(",")
        install_experts(project_name=project_name, specific_experts=specific)
    elif action == "show":
        if len(args) > 1:
            show_expert(args[1])
        else:
            list_experts()
    else:
        # Treat as direct trigger: saois experts ui_ux_designer
        show_expert(action)


def cmd_run(name: str):
    cmd_work(name)


def cmd_doctor():
    cmd_tools(verbose=True)


def cmd_quickstart():
    cmd_start()


def cmd_setup():
    cmd_start()


def run_command(args):
    """Main command dispatcher."""
    if len(args) < 2:
        projects = registry.get_all()
        if not projects:
            ui.welcome()
        else:
            cmd_help()
        return

    command = args[1].lower()

    if command in ("start", "setup", "quickstart", "init"):
        cmd_start()

    elif command in ("work", "run", "go"):
        if len(args) < 3:
            ui.error("Please specify a project name")
            ui.dim("Usage: saois work <project-name>")
            return
        cmd_work(args[2])

    elif command in ("list", "ls", "projects"):
        cmd_list()

    elif command == "add":
        if len(args) < 4:
            ui.error("Please specify name and path")
            ui.dim("Usage: saois add <name> <path>")
            return
        cmd_add(args[2], args[3])

    elif command in ("tools", "doctor", "check"):
        verbose = "--verbose" in args or "-v" in args
        cmd_tools(verbose=verbose)

    elif command in ("help", "-h", "--help", "?"):
        cmd_help()

    elif command in ("remove", "rm", "delete"):
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

    elif command == "suggest":
        if len(args) < 3:
            ui.error("Please specify a project name")
            ui.dim("Usage: saois suggest <project-name>")
            return
        cmd_suggest(args[2])

    elif command == "prompts":
        sub = args[2] if len(args) > 2 else None
        cmd_prompts(sub)

    elif command == "experts":
        cmd_experts(args[2:] if len(args) > 2 else [])

    else:
        if registry.exists(command):
            cmd_work(command)
        else:
            ui.error(f"Unknown command: {command}")
            ui.tip("Run 'saois help' to see available commands")
