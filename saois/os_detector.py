"""
OS Detection and Platform-Specific Operations
"""
import platform
import subprocess
import shutil
from pathlib import Path

def get_os():
    """Detect the current operating system."""
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    elif system == "Windows":
        return "windows"
    else:
        return "unknown"

def get_install_command(tool_name, os_type):
    """Get the installation command for a tool based on OS."""
    install_commands = {
        "macos": {
            "windsurf": "brew install --cask windsurf",
            "claude": "# Visit https://claude.ai/code",
            "perplexity": "# Visit https://perplexity.ai",
            "cody": "brew install sourcegraph/cody/cody",
            "continue": "# Visit https://continue.dev"
        },
        "linux": {
            "windsurf": "# Visit https://codeium.com/windsurf",
            "claude": "# Visit https://claude.ai/code",
            "perplexity": "# Visit https://perplexity.ai",
            "cody": "# Visit https://sourcegraph.com/cody",
            "continue": "# Visit https://continue.dev"
        },
        "windows": {
            "windsurf": "winget install Codeium.Windsurf",
            "claude": "# Visit https://claude.ai/code",
            "perplexity": "# Visit https://perplexity.ai",
            "cody": "# Visit https://sourcegraph.com/cody",
            "continue": "# Visit https://continue.dev"
        }
    }
    
    return install_commands.get(os_type, {}).get(tool_name, "# No install command available")

def open_application(app_name, os_type):
    """Open an application based on OS."""
    try:
        if os_type == "macos":
            subprocess.run(["open", "-a", app_name], check=True)
            return True
        elif os_type == "linux":
            # Try direct command first
            if shutil.which(app_name.lower()):
                subprocess.run([app_name.lower()], check=False)
                return True
            else:
                subprocess.run(["xdg-open", app_name], check=False)
                return True
        elif os_type == "windows":
            subprocess.run(["start", app_name], shell=True, check=True)
            return True
    except:
        return False
    
    return False

def open_url(url, os_type):
    """Open a URL in the default browser."""
    try:
        if os_type == "macos":
            subprocess.run(["open", url], check=True)
        elif os_type == "linux":
            subprocess.run(["xdg-open", url], check=True)
        elif os_type == "windows":
            subprocess.run(["start", url], shell=True, check=True)
        return True
    except:
        return False

def check_tool_installed(tool_command):
    """Check if a tool is installed by looking for its command."""
    return shutil.which(tool_command) is not None

def get_ai_projects_path():
    """Get the path to AI_PROJECTS folder."""
    home = Path.home()
    ai_projects = home / "Documents" / "AI_PROJECTS"
    return ai_projects if ai_projects.exists() else None
