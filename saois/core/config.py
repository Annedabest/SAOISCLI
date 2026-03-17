"""
SAOIS Core Configuration
Handles all configuration, paths, and settings with smart defaults.
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any

class Config:
    """Central configuration manager with smart defaults."""
    
    # Default paths
    CONFIG_DIR = Path.home() / ".saois"
    PROJECTS_FILE = CONFIG_DIR / "projects.json"
    SETTINGS_FILE = CONFIG_DIR / "settings.json"
    TOOLS_FILE = CONFIG_DIR / "tools_config.json"
    
    # Default AI_PROJECTS locations to check
    DEFAULT_PROJECT_PATHS = [
        Path.home() / "Documents" / "AI_PROJECTS",
        Path.home() / "AI_PROJECTS",
        Path.home() / "Projects",
        Path.home() / "projects",
        Path.home() / "dev",
    ]
    
    # Simplified tool routing - 3 task types only
    DEFAULT_TOOL_ROUTING = {
        "code": ["windsurf", "cursor", "vscode"],      # Coding tasks
        "research": ["perplexity", "chatgpt"],          # Research tasks  
        "plan": ["claude", "chatgpt"],                  # Planning/architecture
    }
    
    # Tool detection paths by OS
    TOOL_PATHS = {
        "windows": {
            "windsurf": [
                Path.home() / "AppData" / "Local" / "Programs" / "Windsurf" / "Windsurf.exe",
                Path("C:/Program Files/Windsurf/Windsurf.exe"),
            ],
            "cursor": [
                Path.home() / "AppData" / "Local" / "Programs" / "cursor" / "Cursor.exe",
            ],
            "vscode": [
                Path.home() / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "Code.exe",
                Path("C:/Program Files/Microsoft VS Code/Code.exe"),
            ],
            "claude": [],  # Browser-based
            "chatgpt": [], # Browser-based
            "perplexity": [], # Browser-based
        },
        "macos": {
            "windsurf": [Path("/Applications/Windsurf.app")],
            "cursor": [Path("/Applications/Cursor.app")],
            "vscode": [Path("/Applications/Visual Studio Code.app")],
            "claude": [Path("/Applications/Claude.app")],
            "chatgpt": [],
            "perplexity": [],
        },
        "linux": {
            "windsurf": [Path("/usr/bin/windsurf"), Path.home() / ".local/bin/windsurf"],
            "cursor": [Path("/usr/bin/cursor"), Path.home() / ".local/bin/cursor"],
            "vscode": [Path("/usr/bin/code"), Path("/snap/bin/code")],
            "claude": [],
            "chatgpt": [],
            "perplexity": [],
        }
    }
    
    # Tool URLs for browser fallback
    TOOL_URLS = {
        "windsurf": "https://windsurf.ai",
        "cursor": "https://cursor.sh",
        "vscode": "https://code.visualstudio.com",
        "claude": "https://claude.ai",
        "chatgpt": "https://chat.openai.com",
        "perplexity": "https://perplexity.ai",
    }
    
    # Tool display names
    TOOL_NAMES = {
        "windsurf": "Windsurf",
        "cursor": "Cursor",
        "vscode": "VS Code",
        "claude": "Claude",
        "chatgpt": "ChatGPT",
        "perplexity": "Perplexity",
    }
    
    def __init__(self):
        self._ensure_config_dir()
        self._settings = self._load_settings()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings with smart defaults."""
        if self.SETTINGS_FILE.exists():
            try:
                return json.loads(self.SETTINGS_FILE.read_text())
            except:
                pass
        return {}
    
    def save_settings(self):
        """Save current settings."""
        self.SETTINGS_FILE.write_text(json.dumps(self._settings, indent=2))
    
    def get_ai_projects_path(self) -> Optional[Path]:
        """Get AI_PROJECTS path, auto-detecting if not set."""
        # Check if explicitly set
        if "ai_projects_path" in self._settings:
            path = Path(self._settings["ai_projects_path"])
            if path.exists():
                return path
        
        # Auto-detect from common locations
        for path in self.DEFAULT_PROJECT_PATHS:
            if path.exists():
                self._settings["ai_projects_path"] = str(path)
                self.save_settings()
                return path
        
        return None
    
    def set_ai_projects_path(self, path: Path):
        """Set AI_PROJECTS path."""
        self._settings["ai_projects_path"] = str(path)
        self.save_settings()
    
    def get_os(self) -> str:
        """Detect operating system."""
        import platform
        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        elif system == "windows":
            return "windows"
        return "linux"
    
    def is_tool_installed(self, tool_id: str) -> bool:
        """Check if a tool is installed."""
        os_type = self.get_os()
        paths = self.TOOL_PATHS.get(os_type, {}).get(tool_id, [])
        
        for path in paths:
            if path.exists():
                return True
        
        # Also check if command is in PATH
        import shutil
        if shutil.which(tool_id):
            return True
        
        return False
    
    def get_installed_tools(self) -> Dict[str, bool]:
        """Get status of all tools."""
        return {
            tool_id: self.is_tool_installed(tool_id)
            for tool_id in self.TOOL_NAMES.keys()
        }
    
    def get_best_tool_for_task(self, task_type: str) -> Optional[str]:
        """Get the best available tool for a task type."""
        # Normalize task type
        task_type = task_type.lower().strip()
        
        # Map old task types to new simplified ones
        task_mapping = {
            "coding": "code",
            "debugging": "code",
            "code": "code",
            "research": "research",
            "analysis": "research",
            "architecture": "plan",
            "planning": "plan",
            "plan": "plan",
            "documentation": "code",
            "deployment": "code",
            "automation": "code",
        }
        
        simplified_task = task_mapping.get(task_type, "code")
        tool_chain = self.DEFAULT_TOOL_ROUTING.get(simplified_task, ["windsurf"])
        
        # Return first installed tool in the chain
        for tool_id in tool_chain:
            if self.is_tool_installed(tool_id):
                return tool_id
        
        # Return first tool (will use browser fallback)
        return tool_chain[0] if tool_chain else "windsurf"
    
    def get_tool_launch_command(self, tool_id: str, project_path: Path) -> tuple:
        """Get command to launch a tool with project path."""
        os_type = self.get_os()
        
        if os_type == "windows":
            if tool_id == "windsurf":
                return ("windsurf", [str(project_path)])
            elif tool_id == "cursor":
                return ("cursor", [str(project_path)])
            elif tool_id == "vscode":
                return ("code", [str(project_path)])
        elif os_type == "macos":
            if tool_id in ["windsurf", "cursor", "vscode"]:
                app_name = self.TOOL_NAMES[tool_id]
                return ("open", ["-a", app_name, str(project_path)])
        else:  # Linux
            return (tool_id, [str(project_path)])
        
        # Browser fallback
        return (None, self.TOOL_URLS.get(tool_id, "https://windsurf.ai"))


# Global config instance
config = Config()
