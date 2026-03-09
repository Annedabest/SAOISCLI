"""
Helper utilities for SAOIS CLI
"""
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def detect_project_type(project_path):
    """Detect project type and dependencies."""
    path = Path(project_path)
    
    info = {
        "type": None,
        "package_manager": None,
        "docker": False,
        "docker_compose": False,
        "dependencies_file": None,
        "start_command": None
    }
    
    # Check for Node.js
    if (path / "package.json").exists():
        info["type"] = "node"
        info["dependencies_file"] = "package.json"
        
        # Detect package manager
        if (path / "pnpm-lock.yaml").exists():
            info["package_manager"] = "pnpm"
            info["start_command"] = "pnpm install && pnpm dev"
        elif (path / "yarn.lock").exists():
            info["package_manager"] = "yarn"
            info["start_command"] = "yarn install && yarn dev"
        else:
            info["package_manager"] = "npm"
            info["start_command"] = "npm install && npm run dev"
    
    # Check for Python
    elif (path / "requirements.txt").exists():
        info["type"] = "python"
        info["dependencies_file"] = "requirements.txt"
        info["start_command"] = "pip install -r requirements.txt && python main.py"
    
    # Check for Rust
    elif (path / "Cargo.toml").exists():
        info["type"] = "rust"
        info["dependencies_file"] = "Cargo.toml"
        info["start_command"] = "cargo run"
    
    # Check for Go
    elif (path / "go.mod").exists():
        info["type"] = "go"
        info["dependencies_file"] = "go.mod"
        info["start_command"] = "go run ."
    
    # Check for Docker
    if (path / "docker-compose.yml").exists() or (path / "docker-compose.yaml").exists():
        info["docker_compose"] = True
        info["start_command"] = "docker-compose up -d"
    elif (path / "Dockerfile").exists():
        info["docker"] = True
        info["start_command"] = "docker build -t project . && docker run -p 3000:3000 project"
    
    return info

def run_command_with_output(command, cwd):
    """Run a command and capture output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out after 30 seconds",
            "returncode": -1
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

def simplify_error(error_text, project_type):
    """Simplify error messages for common issues."""
    error_lower = error_text.lower()
    
    # Common Node.js errors
    if project_type == "node":
        if "enoent" in error_lower or "cannot find module" in error_lower:
            return "Missing dependencies. Run: npm install (or pnpm/yarn install)"
        elif "port" in error_lower and "already in use" in error_lower:
            return "Port already in use. Stop the other process or change the port."
        elif "eslint" in error_lower or "prettier" in error_lower:
            return "Linting/formatting error. Check your code style."
        elif "syntax" in error_lower:
            return "Syntax error in your code. Check the file mentioned in the error."
    
    # Common Python errors
    elif project_type == "python":
        if "modulenotfounderror" in error_lower or "no module named" in error_lower:
            return "Missing Python package. Run: pip install -r requirements.txt"
        elif "syntaxerror" in error_lower:
            return "Python syntax error. Check your code."
        elif "indentation" in error_lower:
            return "Indentation error. Fix spacing/tabs in your Python code."
    
    # Docker errors
    if "docker" in error_lower:
        if "cannot connect" in error_lower or "daemon" in error_lower:
            return "Docker is not running. Start Docker Desktop."
        elif "port is already allocated" in error_lower:
            return "Port already in use. Stop other containers or change the port."
        elif "no such file" in error_lower and "dockerfile" in error_lower:
            return "Dockerfile not found or has errors."
    
    # Generic errors
    if "permission denied" in error_lower:
        return "Permission denied. Try running with sudo or check file permissions."
    elif "command not found" in error_lower:
        return "Command not found. Install the required tool first."
    
    # Return first 200 chars if no simplification
    return error_text[:200] + "..." if len(error_text) > 200 else error_text

def get_fix_prompt(error_simplified, project_type, project_info):
    """Generate a prompt for AI tools to fix the error."""
    prompt = f"""I'm working on a {project_type} project and encountered this error:

{error_simplified}

Project details:
- Type: {project_type}
- Package manager: {project_info.get('package_manager', 'N/A')}
- Dependencies file: {project_info.get('dependencies_file', 'N/A')}

Please help me:
1. Understand what's causing this error
2. Provide step-by-step instructions to fix it
3. Suggest any missing dependencies or configuration
4. Show the exact commands I need to run

Keep the explanation clear and actionable."""
    
    return prompt

def log_error_to_file(project_name, error_info, log_dir, ask_permission=True):
    """Save error details to a .txt file for future reference."""
    from rich.prompt import Confirm
    
    if ask_permission:
        if not Confirm.ask("\n[dim]Save error log for future reference?[/dim]", default=False):
            return None
    
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"{project_name}_errors.txt"
    
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_content = f"""
{'='*60}
ERROR LOG - {project_name}
Timestamp: {timestamp}
{'='*60}

Project Type: {error_info.get('project_type', 'Unknown')}
Command: {error_info.get('command', 'N/A')}

SIMPLIFIED ERROR:
{error_info.get('simplified', 'N/A')}

FULL ERROR OUTPUT:
{error_info.get('full_error', 'N/A')}

RECOMMENDED ACTION:
{error_info.get('recommendation', 'N/A')}

FIX PROMPT FOR AI:
{error_info.get('ai_prompt', 'N/A')}

{'='*60}

"""
    
    with open(log_file, 'a') as f:
        f.write(log_content)
    
    return log_file
