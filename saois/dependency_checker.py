"""
Dependency checker for SAOIS CLI - checks for required tools and offers installation
"""
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

console = Console()

def check_command_exists(command):
    """Check if a command exists in PATH."""
    return shutil.which(command) is not None

def check_docker():
    """Check if Docker is installed and running."""
    if not check_command_exists("docker"):
        return {"installed": False, "running": False}
    
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return {"installed": True, "running": result.returncode == 0}
    except:
        return {"installed": True, "running": False}

def check_node_tools():
    """Check for Node.js package managers."""
    return {
        "node": check_command_exists("node"),
        "npm": check_command_exists("npm"),
        "pnpm": check_command_exists("pnpm"),
        "yarn": check_command_exists("yarn")
    }

def check_python_tools():
    """Check for Python tools."""
    return {
        "python": check_command_exists("python") or check_command_exists("python3"),
        "pip": check_command_exists("pip") or check_command_exists("pip3")
    }

def install_via_homebrew(package_name, formula=None):
    """Install a package via Homebrew."""
    if not check_command_exists("brew"):
        console.print("[red]✗ Homebrew not installed[/red]")
        console.print("[dim]Install from: https://brew.sh[/dim]")
        return False
    
    formula = formula or package_name
    console.print(f"\n[dim]Running: brew install {formula}[/dim]")
    
    try:
        result = subprocess.run(
            ["brew", "install", formula],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print(f"[#00ff00]✓ {package_name} installed successfully![/#00ff00]")
            return True
        else:
            console.print(f"[red]✗ Installation failed: {result.stderr}[/red]")
            return False
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        return False

def offer_docker_install():
    """Offer to install or start Docker."""
    docker_status = check_docker()
    
    if not docker_status["installed"]:
        console.print("[yellow]Docker is not installed[/yellow]")
        console.print("\n[#ff00ff]Install options:[/#ff00ff]")
        console.print("  [#00ffff]1.[/#00ffff] macOS: [bold]brew install --cask docker[/bold]")
        console.print("  [#00ffff]2.[/#00ffff] Or download from: [bold]https://docker.com/get-started[/bold]")
        
        if Confirm.ask("\nInstall Docker Desktop via Homebrew?", default=False):
            return install_via_homebrew("Docker Desktop", "docker")
    
    elif not docker_status["running"]:
        console.print("[yellow]Docker is installed but not running[/yellow]")
        console.print("[dim]Please start Docker Desktop manually[/dim]")
    
    return docker_status["running"]

def offer_node_install():
    """Offer to install Node.js and package managers."""
    node_status = check_node_tools()
    
    if not node_status["node"]:
        console.print("[yellow]Node.js is not installed[/yellow]")
        console.print("\n[#ff00ff]Install options:[/#ff00ff]")
        console.print("  [#00ffff]1.[/#00ffff] macOS: [bold]brew install node[/bold]")
        console.print("  [#00ffff]2.[/#00ffff] Or download from: [bold]https://nodejs.org[/bold]")
        
        if Confirm.ask("\nInstall Node.js via Homebrew?", default=False):
            if install_via_homebrew("Node.js", "node"):
                return check_node_tools()
    
    # Offer to install pnpm/yarn if npm exists
    if node_status["npm"]:
        if not node_status["pnpm"]:
            if Confirm.ask("\nInstall pnpm (fast package manager)?", default=False):
                subprocess.run(["npm", "install", "-g", "pnpm"])
        
        if not node_status["yarn"]:
            if Confirm.ask("\nInstall yarn?", default=False):
                subprocess.run(["npm", "install", "-g", "yarn"])
    
    return check_node_tools()

def offer_python_install():
    """Offer to install Python tools."""
    python_status = check_python_tools()
    
    if not python_status["python"]:
        console.print("[yellow]Python is not installed[/yellow]")
        console.print("\n[#ff00ff]Install options:[/#ff00ff]")
        console.print("  [#00ffff]1.[/#00ffff] macOS: [bold]brew install python[/bold]")
        console.print("  [#00ffff]2.[/#00ffff] Or download from: [bold]https://python.org[/bold]")
        
        if Confirm.ask("\nInstall Python via Homebrew?", default=False):
            return install_via_homebrew("Python", "python")
    
    return python_status["python"]

def check_dependencies_for_project(project_info):
    """Check and offer to install dependencies based on project type."""
    missing = []
    
    if project_info.get("docker") or project_info.get("docker_compose"):
        docker_status = check_docker()
        if not docker_status["installed"]:
            missing.append("docker")
        elif not docker_status["running"]:
            console.print("\n[yellow]⚠️  Docker is installed but not running[/yellow]")
            console.print("[dim]Please start Docker Desktop[/dim]")
    
    if project_info.get("type") == "node":
        node_status = check_node_tools()
        if not node_status["node"]:
            missing.append("node")
        
        pm = project_info.get("package_manager")
        if pm and not node_status.get(pm):
            missing.append(pm)
    
    elif project_info.get("type") == "python":
        python_status = check_python_tools()
        if not python_status["python"]:
            missing.append("python")
        if not python_status["pip"]:
            missing.append("pip")
    
    if missing:
        console.print(f"\n[yellow]⚠️  Missing dependencies: {', '.join(missing)}[/yellow]")
        
        if Confirm.ask("\nWould you like to install missing dependencies?", default=True):
            for dep in missing:
                if dep == "docker":
                    offer_docker_install()
                elif dep == "node":
                    offer_node_install()
                elif dep == "python":
                    offer_python_install()
                elif dep == "pnpm":
                    subprocess.run(["npm", "install", "-g", "pnpm"])
                elif dep == "yarn":
                    subprocess.run(["npm", "install", "-g", "yarn"])
        
        return False
    
    return True
