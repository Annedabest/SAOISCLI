"""
OS Detection and Platform-Specific Operations
"""
import json
import platform
import subprocess
import shutil
from pathlib import Path

CONFIG_DIR = Path.home() / ".saois"
SETTINGS_FILE = CONFIG_DIR / "settings.json"

MAC_APP_PATHS = {
    "Windsurf": [
        "/Applications/Windsurf.app",
        "/Applications/Windsurf - Next.app",
        "/Applications/Codeium Windsurf.app"
    ],
    "Claude": ["/Applications/Claude.app"],
    "Cursor": ["/Applications/Cursor.app"],
    "VS Code": [
        "/Applications/Visual Studio Code.app",
        "/Applications/VSCode.app"
    ],
    "ChatGPT": ["/Applications/ChatGPT.app"],
    "Cody": ["/Applications/Cody.app", "/Applications/Sourcegraph Cody.app"],
    "Continue": ["/Applications/Continue.app", "/Applications/Continue Dev.app"]
}

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

DISPLAY_NAME_TO_TOOL_ID = {
    "Windsurf": "windsurf",
    "Cursor": "cursor",
    "VS Code": "vscode",
    "Claude": "claude",
    "ChatGPT": "chatgpt",
    "Cody": "cody",
    "Continue": "continue",
}


def check_tool_installed(tool_command):
    """Check if a tool is installed by looking for CLI binary or macOS app."""
    tool_id = DISPLAY_NAME_TO_TOOL_ID.get(tool_command)
    if tool_id:
        try:
            from saois.core.config import config

            return config.is_tool_installed(tool_id)
        except Exception:
            pass

    if shutil.which(tool_command):
        return True

    os_type = get_os()
    if os_type == "macos":
        app_paths = MAC_APP_PATHS.get(tool_command, [])
        for path in app_paths:
            if Path(path).exists():
                return True

    return False

def load_settings():
    if SETTINGS_FILE.exists():
        try:
            return json.loads(SETTINGS_FILE.read_text())
        except Exception:
            return {}
    return {}

def save_settings(settings):
    CONFIG_DIR.mkdir(exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2))

def get_ai_projects_path(allow_missing=False):
    """Get the configured AI projects folder."""
    settings = load_settings()
    custom_path = settings.get("projects_folder")
    if custom_path:
        custom = Path(custom_path)
        if custom.exists() or allow_missing:
            return custom
    default = Path.home() / "Documents" / "AI_PROJECTS"
    if default.exists() or allow_missing:
        return default
    return None

def set_ai_projects_path(path):
    """Persist a custom AI projects folder."""
    settings = load_settings()
    settings["projects_folder"] = str(path)
    save_settings(settings)
