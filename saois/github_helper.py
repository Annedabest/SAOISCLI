"""
GitHub automation helper for SAOIS CLI
"""
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()

def check_git_repo(project_path):
    """Check if directory is a git repository."""
    git_dir = Path(project_path) / ".git"
    return git_dir.exists()

def init_git_repo(project_path):
    """Initialize a git repository."""
    try:
        result = subprocess.run(
            ["git", "init"],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        console.print(f"[red]✗ Failed to init git: {e}[/red]")
        return False

def git_add_all(project_path):
    """Stage all changes."""
    try:
        result = subprocess.run(
            ["git", "add", "."],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        console.print(f"[red]✗ Failed to stage files: {e}[/red]")
        return False

def git_commit(project_path, message):
    """Commit staged changes."""
    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        console.print(f"[red]✗ Failed to commit: {e}[/red]")
        return False, "", str(e)

def git_push(project_path, remote="origin", branch="main"):
    """Push commits to remote."""
    try:
        result = subprocess.run(
            ["git", "push", remote, branch],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        console.print(f"[red]✗ Failed to push: {e}[/red]")
        return False, "", str(e)

def get_git_status(project_path):
    """Get git status."""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return ""

def check_remote_exists(project_path, remote="origin"):
    """Check if remote exists."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout.strip()
    except:
        return False, ""

def add_remote(project_path, remote_url, remote="origin"):
    """Add git remote."""
    try:
        result = subprocess.run(
            ["git", "remote", "add", remote, remote_url],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        console.print(f"[red]✗ Failed to add remote: {e}[/red]")
        return False

def auto_commit_and_push(project_path, commit_message=None):
    """Automated commit and push workflow."""
    console.print("\n[bold #00ffff]🚀 Git Commit & Push Automation[/bold #00ffff]\n")
    
    # Check if git repo
    if not check_git_repo(project_path):
        console.print("[yellow]Not a git repository[/yellow]")
        if Confirm.ask("Initialize git repository?", default=True):
            if not init_git_repo(project_path):
                return False
            console.print("[#00ff00]✓ Git repository initialized[/#00ff00]\n")
        else:
            return False
    
    # Show status
    status = get_git_status(project_path)
    if not status:
        console.print("[#00ff00]✓ No changes to commit[/#00ff00]")
        return True
    
    console.print("[#00ffff]Changes to commit:[/#00ffff]")
    console.print(status)
    
    if not Confirm.ask("\nStage all changes?", default=True):
        return False
    
    # Stage changes
    if not git_add_all(project_path):
        return False
    console.print("[#00ff00]✓ Changes staged[/#00ff00]\n")
    
    # Get commit message
    if not commit_message:
        commit_message = Prompt.ask(
            "[#ff00ff]Commit message[/#ff00ff]",
            default="Update project files"
        )
    
    # Commit
    success, stdout, stderr = git_commit(project_path, commit_message)
    if not success:
        if "nothing to commit" in stderr:
            console.print("[#00ff00]✓ Nothing to commit[/#00ff00]")
        else:
            console.print(f"[red]✗ Commit failed: {stderr}[/red]")
            return False
    else:
        console.print(f"[#00ff00]✓ Committed: {commit_message}[/#00ff00]\n")
    
    # Check for remote
    has_remote, remote_url = check_remote_exists(project_path)
    
    if not has_remote:
        console.print("[yellow]No remote repository configured[/yellow]")
        if Confirm.ask("Add remote repository?", default=True):
            remote_url = Prompt.ask("[#ff00ff]Remote URL (e.g., https://github.com/user/repo.git)[/#ff00ff]")
            if add_remote(project_path, remote_url):
                console.print(f"[#00ff00]✓ Remote added: {remote_url}[/#00ff00]\n")
            else:
                console.print("[yellow]Skipping push - no remote configured[/yellow]")
                return False
        else:
            console.print("[yellow]Skipping push - no remote configured[/yellow]")
            return False
    else:
        console.print(f"[dim]Remote: {remote_url}[/dim]\n")
    
    # Push
    if Confirm.ask("Push to remote?", default=True):
        console.print("[dim]Pushing to origin/main...[/dim]")
        success, stdout, stderr = git_push(project_path)
        
        if success:
            console.print("[#00ff00]✓ Pushed successfully![/#00ff00]")
            return True
        else:
            # Try pushing with upstream
            if "no upstream branch" in stderr or "set-upstream" in stderr:
                console.print("[dim]Setting upstream branch...[/dim]")
                result = subprocess.run(
                    ["git", "push", "-u", "origin", "main"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    console.print("[#00ff00]✓ Pushed successfully![/#00ff00]")
                    return True
            
            console.print(f"[red]✗ Push failed: {stderr}[/red]")
            console.print("\n[dim]You may need to:[/dim]")
            console.print("  1. Check your GitHub credentials")
            console.print("  2. Ensure the remote repository exists")
            console.print("  3. Pull changes first if remote has updates")
            return False
    
    return True
