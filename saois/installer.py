"""
Tool Installation and Management
"""
import subprocess
from rich.console import Console
from rich.prompt import Confirm
from .os_detector import get_os, get_install_command, open_url, check_tool_installed

console = Console()

def check_all_tools():
    """Check which tools are installed."""
    tools_to_check = {
        "Windsurf": "windsurf",
        "Claude": "claude",
        "Perplexity": "perplexity",
        "Cody": "cody",
        "Continue": "continue"
    }
    
    results = {}
    for name, command in tools_to_check.items():
        results[name] = check_tool_installed(command)
    
    return results

def offer_installation(tool_name, tool_command, tool_url):
    """Offer to install a tool if it's not found."""
    os_type = get_os()
    
    console.print(f"\n[yellow]⚠️  {tool_name} not detected[/yellow]")
    
    install_cmd = get_install_command(tool_command, os_type)
    
    # Check if it's a manual install (starts with #)
    if install_cmd.startswith("#"):
        console.print(f"[dim]{install_cmd}[/dim]")
        if Confirm.ask(f"[#ff00ff]Open {tool_name} download page?[/#ff00ff]", default=True):
            console.print(f"[#00ffff]Opening {tool_url}...[/#00ffff]")
            open_url(tool_url, os_type)
        return False
    
    # Show install command
    console.print(f"\n[#00ffff]Install command:[/#00ffff]")
    console.print(f"  [dim]{install_cmd}[/dim]\n")
    
    choice = console.input(
        "[#ff00ff]Options:[/#ff00ff]\n"
        "  [1] Run install command\n"
        "  [2] Open download page\n"
        "  [3] Skip\n"
        "[#ff00ff]Choose (1/2/3):[/#ff00ff] "
    )
    
    if choice == "1":
        if Confirm.ask(f"[yellow]Run: {install_cmd}?[/yellow]", default=False):
            try:
                console.print(f"[#00ffff]Installing {tool_name}...[/#00ffff]")
                result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    console.print(f"[#00ff00]✓ {tool_name} installed successfully![/#00ff00]")
                    return True
                else:
                    console.print(f"[red]✗ Installation failed[/red]")
                    console.print(f"[dim]{result.stderr}[/dim]")
                    if Confirm.ask("[#ff00ff]Open download page instead?[/#ff00ff]", default=True):
                        open_url(tool_url, os_type)
            except Exception as e:
                console.print(f"[red]✗ Error: {e}[/red]")
                if Confirm.ask("[#ff00ff]Open download page instead?[/#ff00ff]", default=True):
                    open_url(tool_url, os_type)
    elif choice == "2":
        console.print(f"[#00ffff]Opening {tool_url}...[/#00ffff]")
        open_url(tool_url, os_type)
    else:
        console.print("[dim]Skipped installation[/dim]")
    
    return False

def verify_tool_installation(tool_command):
    """Verify if a tool was successfully installed."""
    return check_tool_installed(tool_command)
