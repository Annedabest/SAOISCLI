"""
GitHub integration for SAOIS CLI
"""
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def clone_github_repo(repo_url, destination):
    """Clone a GitHub repository."""
    try:
        result = subprocess.run(
            ["git", "clone", repo_url, str(destination)],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Clone operation timed out (5 minutes)"
    except Exception as e:
        return False, str(e)

def is_git_installed():
    """Check if git is installed."""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def parse_github_url(url):
    """Extract repo name from GitHub URL."""
    # Handle various GitHub URL formats
    # https://github.com/user/repo
    # https://github.com/user/repo.git
    # git@github.com:user/repo.git
    
    if "github.com" not in url:
        return None
    
    parts = url.replace(".git", "").split("/")
    if len(parts) >= 2:
        return parts[-1]
    
    # Handle SSH format
    if ":" in url:
        parts = url.split(":")[-1].replace(".git", "").split("/")
        if parts:
            return parts[-1]
    
    return None

def install_git_prompt():
    """Prompt user to install git."""
    console.print("[yellow]Git is not installed[/yellow]")
    console.print("\n[#ff00ff]Install options:[/#ff00ff]")
    console.print("  [#00ffff]1.[/#00ffff] macOS: [bold]brew install git[/bold]")
    console.print("  [#00ffff]2.[/#00ffff] Or download from: [bold]https://git-scm.com/downloads[/bold]")
    
    if Confirm.ask("\nInstall git via Homebrew now?", default=False):
        console.print("\n[dim]Running: brew install git[/dim]")
        try:
            result = subprocess.run(
                ["brew", "install", "git"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                console.print("[#00ff00]✓ Git installed successfully![/#00ff00]")
                return True
            else:
                console.print(f"[red]✗ Installation failed: {result.stderr}[/red]")
                return False
        except FileNotFoundError:
            console.print("[red]✗ Homebrew not found. Install from https://brew.sh[/red]")
            return False
    
    return False
