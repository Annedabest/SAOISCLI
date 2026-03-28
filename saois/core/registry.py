"""
SAOIS Project Registry
Manages project registration, discovery, and validation.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .config import config

class Registry:
    """Project registry with auto-discovery and validation."""
    
    def __init__(self):
        self._projects: Dict[str, str] = {}
        self._load()
    
    def _load(self):
        """Load projects from file and auto-discover."""
        if config.PROJECTS_FILE.exists():
            try:
                self._projects = json.loads(config.PROJECTS_FILE.read_text())
            except Exception:
                self._projects = {}
        else:
            self._projects = {}

        merged_new = False
        ai_path = config.get_ai_projects_path()
        if ai_path and ai_path.exists():
            for item in ai_path.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    if item.name not in self._projects:
                        self._projects[item.name] = str(item)
                        merged_new = True
        if merged_new:
            self.save()
    
    def save(self):
        """Save projects to file."""
        config.PROJECTS_FILE.write_text(json.dumps(self._projects, indent=2))
    
    def get_all(self) -> Dict[str, str]:
        """Get all registered projects."""
        return self._projects.copy()
    
    def get(self, name: str) -> Optional[Path]:
        """Get project path by name."""
        if name in self._projects:
            return Path(self._projects[name])
        return None
    
    def exists(self, name: str) -> bool:
        """Check if project exists in registry."""
        return name in self._projects
    
    def add(self, name: str, path: Path) -> bool:
        """Add a project to registry."""
        self._projects[name] = str(path.resolve())
        self.save()
        return True
    
    def remove(self, name: str) -> bool:
        """Remove a project from registry."""
        if name in self._projects:
            del self._projects[name]
            self.save()
            return True
        return False
    
    def count(self) -> int:
        """Get number of registered projects."""
        return len(self._projects)
    
    def validate(self) -> Tuple[List[str], List[str]]:
        """Validate all projects, return (valid, missing) lists."""
        valid = []
        missing = []
        
        for name, path in self._projects.items():
            if Path(path).exists():
                valid.append(name)
            else:
                missing.append(name)
        
        return valid, missing
    
    def scan_folder(self, folder: Path) -> Dict[str, str]:
        """Scan a folder for projects."""
        found = {}
        if folder.exists():
            for item in folder.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    found[item.name] = str(item)
        return found
    
    def import_projects(self, projects: Dict[str, str]) -> Tuple[int, int]:
        """Import multiple projects. Returns (newly_added_count, already_present_count)."""
        new_count = 0
        skipped = 0
        for name, path in projects.items():
            if name not in self._projects:
                self._projects[name] = path
                new_count += 1
            else:
                skipped += 1
        self.save()
        return new_count, skipped
    
    def search(self, query: str) -> List[str]:
        """Search projects by name."""
        query = query.lower()
        return [name for name in self._projects.keys() if query in name.lower()]
    
    def archive_missing(self) -> int:
        """Archive all missing projects."""
        _, missing = self.validate()
        
        if not missing:
            return 0
        
        # Create archive
        archive_dir = config.CONFIG_DIR / "archived_projects"
        archive_dir.mkdir(exist_ok=True)
        archive_file = archive_dir / "projects.json"
        
        archived = {}
        if archive_file.exists():
            try:
                archived = json.loads(archive_file.read_text())
            except:
                pass
        
        # Move missing to archive
        for name in missing:
            archived[name] = self._projects[name]
            del self._projects[name]
        
        archive_file.write_text(json.dumps(archived, indent=2))
        self.save()
        
        return len(missing)


# Global registry instance
registry = Registry()
