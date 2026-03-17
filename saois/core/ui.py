"""
SAOIS UI Components
Clean, simple terminal UI using Rich library.
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from typing import List, Dict, Optional, Tuple

console = Console()

class UI:
    """Simple, clean UI components."""
    
    # Color scheme
    PRIMARY = "#00ffff"      # Cyan
    SECONDARY = "#ff00ff"    # Magenta
    SUCCESS = "#00ff00"      # Green
    WARNING = "#ffff00"      # Yellow
    ERROR = "#ff0000"        # Red
    DIM = "dim"
    
    @staticmethod
    def header():
        """Show app header."""
        console.print(Panel(
            f"[bold {UI.PRIMARY}]⚡ SAOIS[/bold {UI.PRIMARY}]\n"
            f"[{UI.DIM}]Your AI Development Assistant[/{UI.DIM}]",
            border_style=UI.PRIMARY,
            box=box.ROUNDED,
            padding=(0, 2)
        ))
        console.print()
    
    @staticmethod
    def success(message: str):
        """Show success message."""
        console.print(f"[{UI.SUCCESS}]✓ {message}[/{UI.SUCCESS}]")
    
    @staticmethod
    def error(message: str):
        """Show error message."""
        console.print(f"[{UI.ERROR}]✗ {message}[/{UI.ERROR}]")
    
    @staticmethod
    def warning(message: str):
        """Show warning message."""
        console.print(f"[{UI.WARNING}]⚠ {message}[/{UI.WARNING}]")
    
    @staticmethod
    def info(message: str):
        """Show info message."""
        console.print(f"[{UI.PRIMARY}]ℹ {message}[/{UI.PRIMARY}]")
    
    @staticmethod
    def dim(message: str):
        """Show dimmed message."""
        console.print(f"[{UI.DIM}]{message}[/{UI.DIM}]")
    
    @staticmethod
    def tip(message: str):
        """Show a helpful tip."""
        console.print(f"\n[{UI.DIM}]💡 {message}[/{UI.DIM}]")
    
    @staticmethod
    def title(message: str):
        """Show a section title."""
        console.print(f"\n[bold {UI.PRIMARY}]{message}[/bold {UI.PRIMARY}]\n")
    
    @staticmethod
    def ask(question: str, default: str = None, choices: List[str] = None) -> str:
        """Ask user a question."""
        if choices:
            return Prompt.ask(f"[{UI.SECONDARY}]{question}[/{UI.SECONDARY}]", 
                            choices=choices, default=default)
        return Prompt.ask(f"[{UI.SECONDARY}]{question}[/{UI.SECONDARY}]", 
                         default=default)
    
    @staticmethod
    def confirm(question: str, default: bool = True) -> bool:
        """Ask yes/no question."""
        return Confirm.ask(f"[{UI.SECONDARY}]{question}[/{UI.SECONDARY}]", 
                          default=default)
    
    @staticmethod
    def table(title: str, columns: List[str], rows: List[List[str]]):
        """Show a table."""
        table = Table(
            title=f"[bold {UI.PRIMARY}]{title}[/bold {UI.PRIMARY}]",
            show_header=True,
            header_style=f"bold {UI.SECONDARY}",
            border_style=UI.PRIMARY,
            box=box.ROUNDED
        )
        
        for col in columns:
            table.add_column(col)
        
        for row in rows:
            table.add_row(*row)
        
        console.print(table)
    
    @staticmethod
    def project_list(projects: Dict[str, str], show_status: bool = True):
        """Show list of projects."""
        if not projects:
            console.print(Panel(
                f"[{UI.WARNING}]No projects yet![/{UI.WARNING}]\n\n"
                f"[{UI.DIM}]Get started:[/{UI.DIM}]\n"
                f"  [{UI.PRIMARY}]saois start[/{UI.PRIMARY}] - Quick setup\n"
                f"  [{UI.PRIMARY}]saois add NAME PATH[/{UI.PRIMARY}] - Add a project",
                border_style=UI.WARNING,
                box=box.ROUNDED
            ))
            return
        
        table = Table(
            title=f"[bold {UI.PRIMARY}]Your Projects[/bold {UI.PRIMARY}] [{UI.DIM}]({len(projects)} total)[/{UI.DIM}]",
            show_header=True,
            header_style=f"bold {UI.SECONDARY}",
            border_style=UI.PRIMARY,
            box=box.ROUNDED
        )
        
        table.add_column("#", style=UI.SECONDARY, width=4, justify="right")
        table.add_column("Name", style=f"bold {UI.PRIMARY}")
        table.add_column("Path", style=UI.SUCCESS)
        if show_status:
            table.add_column("Status", justify="center", width=10)
        
        from pathlib import Path
        for idx, (name, path) in enumerate(projects.items(), 1):
            exists = Path(path).exists()
            status = f"[{UI.SUCCESS}]✓ Ready[/{UI.SUCCESS}]" if exists else f"[{UI.ERROR}]✗ Missing[/{UI.ERROR}]"
            
            if show_status:
                table.add_row(str(idx), name, path, status)
            else:
                table.add_row(str(idx), name, path)
        
        console.print(table)
    
    @staticmethod
    def tool_status(tools: Dict[str, bool]):
        """Show AI tools status."""
        table = Table(
            title=f"[bold {UI.PRIMARY}]AI Tools[/bold {UI.PRIMARY}]",
            show_header=True,
            header_style=f"bold {UI.SECONDARY}",
            border_style=UI.PRIMARY,
            box=box.ROUNDED
        )
        
        table.add_column("Tool", style=UI.PRIMARY)
        table.add_column("Status", justify="center")
        table.add_column("Best For", style=UI.DIM)
        
        tool_purposes = {
            "windsurf": "Coding with AI",
            "cursor": "AI-first editing",
            "vscode": "General coding",
            "claude": "Planning & architecture",
            "chatgpt": "General AI help",
            "perplexity": "Research & learning",
        }
        
        for tool, installed in tools.items():
            status = f"[{UI.SUCCESS}]✓ Ready[/{UI.SUCCESS}]" if installed else f"[{UI.DIM}]Not installed[/{UI.DIM}]"
            purpose = tool_purposes.get(tool, "")
            table.add_row(tool.title(), status, purpose)
        
        console.print(table)
        
        installed_count = sum(tools.values())
        console.print(f"\n[{UI.DIM}]{installed_count}/{len(tools)} tools available[/{UI.DIM}]")
    
    @staticmethod
    def welcome():
        """Show welcome message for new users."""
        console.print(Panel(
            f"[bold {UI.PRIMARY}]Welcome to SAOIS! 🚀[/bold {UI.PRIMARY}]\n\n"
            f"SAOIS helps you work on projects with AI assistance.\n"
            f"It automatically picks the best AI tool for your task.\n\n"
            f"[bold]Quick Start:[/bold]\n"
            f"  [{UI.PRIMARY}]saois start[/{UI.PRIMARY}]  →  Set up in 30 seconds\n"
            f"  [{UI.PRIMARY}]saois work NAME[/{UI.PRIMARY}]  →  Start working on a project\n"
            f"  [{UI.PRIMARY}]saois help[/{UI.PRIMARY}]  →  See all commands",
            border_style=UI.PRIMARY,
            box=box.ROUNDED,
            padding=(1, 2)
        ))
    
    @staticmethod
    def help_commands():
        """Show simplified help."""
        UI.header()
        
        console.print(f"[bold {UI.PRIMARY}]Essential Commands[/bold {UI.PRIMARY}]\n")
        
        commands = [
            ("start", "Quick setup (run this first!)", "saois start"),
            ("work <name>", "Start working on a project", "saois work myapp"),
            ("list", "See all your projects", "saois list"),
            ("add <name> <path>", "Add a new project", "saois add myapp ~/projects/myapp"),
            ("tools", "Check your AI tools", "saois tools"),
            ("help", "Show this help", "saois help"),
        ]
        
        table = Table(
            show_header=True,
            header_style=f"bold {UI.SECONDARY}",
            border_style=UI.PRIMARY,
            box=box.ROUNDED
        )
        
        table.add_column("Command", style=UI.PRIMARY)
        table.add_column("What it does", style="white")
        table.add_column("Example", style=UI.SUCCESS)
        
        for cmd, desc, example in commands:
            table.add_row(cmd, desc, example)
        
        console.print(table)
        
        console.print(f"\n[{UI.DIM}]That's it! Just 6 commands to remember.[/{UI.DIM}]")
        console.print(f"[{UI.DIM}]Run 'saois start' to get started.[/{UI.DIM}]")


# Global UI instance
ui = UI()
