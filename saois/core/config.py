"""
SAOIS Core Configuration
Handles all configuration, paths, and settings with smart defaults.
"""
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Launch outcome for honest CLI messaging
LAUNCH_BROWSER = "browser"
LAUNCH_DESKTOP = "desktop"
LAUNCH_FAILED = "failed"


class Config:
    """Central configuration manager with smart defaults."""

    CONFIG_DIR = Path.home() / ".saois"
    PROJECTS_FILE = CONFIG_DIR / "projects.json"
    SETTINGS_FILE = CONFIG_DIR / "settings.json"
    TOOLS_FILE = CONFIG_DIR / "tools_config.json"

    DEFAULT_PROJECT_PATHS = [
        Path.home() / "Documents" / "AI_PROJECTS",
        Path.home() / "AI_PROJECTS",
        Path.home() / "Projects",
        Path.home() / "projects",
        Path.home() / "dev",
    ]

    DEFAULT_TOOL_ROUTING = {
        "code": ["windsurf", "cursor", "vscode"],
        "research": ["perplexity", "chatgpt"],
        "plan": ["claude", "chatgpt"],
    }

    TOOL_URLS = {
        "windsurf": "https://windsurf.ai",
        "cursor": "https://cursor.sh",
        "vscode": "https://code.visualstudio.com",
        "claude": "https://claude.ai",
        "chatgpt": "https://chat.openai.com",
        "perplexity": "https://perplexity.ai",
    }

    TOOL_NAMES = {
        "windsurf": "Windsurf",
        "cursor": "Cursor",
        "vscode": "VS Code",
        "claude": "Claude",
        "chatgpt": "ChatGPT",
        "perplexity": "Perplexity",
    }

    # Single source: paths + PATH binaries per OS (tool_id keys)
    _TOOL_PATHS_WIN = {
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
        "claude": [],
        "chatgpt": [],
        "perplexity": [],
    }

    _TOOL_PATHS_MAC = {
        "windsurf": [
            Path("/Applications/Windsurf.app"),
            Path("/Applications/Windsurf - Next.app"),
            Path("/Applications/Codeium Windsurf.app"),
        ],
        "cursor": [Path("/Applications/Cursor.app")],
        "vscode": [
            Path("/Applications/Visual Studio Code.app"),
            Path("/Applications/VSCode.app"),
        ],
        "claude": [Path("/Applications/Claude.app")],
        "chatgpt": [
            Path("/Applications/ChatGPT.app"),
        ],
        "perplexity": [],
    }

    _TOOL_PATHS_LINUX = {
        "windsurf": [
            Path("/usr/bin/windsurf"),
            Path.home() / ".local/bin/windsurf",
        ],
        "cursor": [
            Path("/usr/bin/cursor"),
            Path.home() / ".local/bin/cursor",
        ],
        "vscode": [
            Path("/usr/bin/code"),
            Path("/snap/bin/code"),
            Path.home() / ".local/bin/code",
        ],
        "claude": [],
        "chatgpt": [],
        "perplexity": [],
    }

    # Extra PATH lookups (CLI names); primary tool_id often not the binary name (e.g. vscode -> code)
    _WHICH_ALIASES = {
        "windsurf": ["windsurf", "Windsurf"],
        "cursor": ["cursor", "Cursor"],
        "vscode": ["code", "vscode"],
        "claude": ["claude", "Claude"],
        "chatgpt": [],
        "perplexity": [],
    }

    def __init__(self):
        self._ensure_config_dir()
        self._settings = self._load_settings()

    def _ensure_config_dir(self):
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def _load_settings(self) -> Dict[str, Any]:
        if self.SETTINGS_FILE.exists():
            try:
                return json.loads(self.SETTINGS_FILE.read_text())
            except Exception:
                pass
        return {}

    def save_settings(self):
        self.SETTINGS_FILE.write_text(json.dumps(self._settings, indent=2))

    def get_ai_projects_path(self) -> Optional[Path]:
        if "ai_projects_path" in self._settings:
            path = Path(self._settings["ai_projects_path"])
            if path.exists():
                return path

        for path in self.DEFAULT_PROJECT_PATHS:
            if path.exists():
                self._settings["ai_projects_path"] = str(path)
                self.save_settings()
                return path

        return None

    def set_ai_projects_path(self, path: Path):
        self._settings["ai_projects_path"] = str(path)
        self.save_settings()

    def get_os(self) -> str:
        import platform

        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        if system == "windows":
            return "windows"
        return "linux"

    def _paths_for_tool(self, tool_id: str) -> List[Path]:
        os_type = self.get_os()
        if os_type == "windows":
            return list(self._TOOL_PATHS_WIN.get(tool_id, []))
        if os_type == "macos":
            return list(self._TOOL_PATHS_MAC.get(tool_id, []))
        return list(self._TOOL_PATHS_LINUX.get(tool_id, []))

    def _first_existing_app_path(self, tool_id: str) -> Optional[Path]:
        for p in self._paths_for_tool(tool_id):
            if p.exists():
                return p
        return None

    def is_tool_installed(self, tool_id: str) -> bool:
        for p in self._paths_for_tool(tool_id):
            if p.exists():
                return True
        for name in self._WHICH_ALIASES.get(tool_id, []):
            if shutil.which(name):
                return True
        if shutil.which(tool_id):
            return True
        return False

    def explain_tool_detection(self, tool_id: str) -> str:
        """Human-readable reason for detection (for doctor / verbose)."""
        hits = []
        for p in self._paths_for_tool(tool_id):
            if p.exists():
                hits.append(f"path:{p}")
        for name in self._WHICH_ALIASES.get(tool_id, []):
            w = shutil.which(name)
            if w:
                hits.append(f"which:{name}→{w}")
        if shutil.which(tool_id):
            hits.append(f"which:{tool_id}")
        if hits:
            return "; ".join(hits)
        return "no matching path or PATH binary"

    def get_installed_tools(self) -> Dict[str, bool]:
        return {tid: self.is_tool_installed(tid) for tid in self.TOOL_NAMES}

    def get_best_tool_for_task(self, task_type: str) -> Optional[str]:
        task_type = task_type.lower().strip()
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
        simplified = task_mapping.get(task_type, "code")
        chain = self.DEFAULT_TOOL_ROUTING.get(simplified, ["windsurf"])
        for tool_id in chain:
            if self.is_tool_installed(tool_id):
                return tool_id
        return chain[0] if chain else "windsurf"

    def get_tool_launch_command(
        self, tool_id: str, project_path: Path
    ) -> Tuple[Optional[str], Any]:
        """Return (executable, args) for subprocess; (executable, args) with cmd None means URL string in args."""
        os_type = self.get_os()
        p = str(project_path.resolve())

        if os_type == "windows":
            if tool_id == "windsurf":
                return "windsurf", [p]
            if tool_id == "cursor":
                return "cursor", [p]
            if tool_id == "vscode":
                return "code", [p]

        elif os_type == "macos":
            if tool_id in ("windsurf", "cursor", "vscode", "claude", "chatgpt"):
                existing = self._first_existing_app_path(tool_id)
                if existing and existing.suffix == ".app":
                    app_name = existing.stem
                    return "open", ["-a", app_name, p]
                if tool_id == "vscode":
                    if shutil.which("code"):
                        return shutil.which("code"), [p]
                if tool_id == "windsurf" and shutil.which("windsurf"):
                    return shutil.which("windsurf"), [p]
                if tool_id == "cursor" and shutil.which("cursor"):
                    return shutil.which("cursor"), [p]
                if tool_id == "claude" and shutil.which("claude"):
                    return shutil.which("claude"), [p]

        else:
            if tool_id == "vscode":
                code = shutil.which("code")
                if code:
                    return code, [p]
            if tool_id == "windsurf":
                w = shutil.which("windsurf")
                if w:
                    return w, [p]
            if tool_id == "cursor":
                c = shutil.which("cursor")
                if c:
                    return c, [p]
            w = shutil.which(tool_id)
            if w:
                return w, [p]

        return None, self.TOOL_URLS.get(tool_id, "https://windsurf.ai")

    def projects_folder_needs_confirmation(
        self, folder: Path
    ) -> Tuple[bool, str]:
        if os.environ.get("SAOIS_SKIP_PROJECT_GUARD"):
            return False, ""

        parts = folder.parts
        is_volume_root = (
            len(parts) >= 2
            and parts[0] == "/"
            and parts[1] == "Volumes"
            and len(parts) == 3
        )

        try:
            n = sum(
                1
                for x in folder.iterdir()
                if x.is_dir() and not x.name.startswith(".")
            )
        except OSError:
            return False, ""

        reasons = []
        if is_volume_root:
            reasons.append("this path is the root of a mounted volume")
        if n > 15:
            reasons.append(f"it contains {n} top-level folders (all will be listed as projects)")
        if not reasons:
            return False, ""
        return True, " and ".join(reasons)


# Global config instance
config = Config()
