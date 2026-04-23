"""
SAOIS Project Registry
Manages project registration, discovery, and validation.
"""
import json
import os
import re
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .config import config

logger = logging.getLogger(__name__)

# Valid project name pattern: alphanumeric, dash, underscore
PROJECT_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')

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
            except json.JSONDecodeError as e:
                logger.error(f"Corrupted projects file: {e}")
                # Backup corrupted file
                backup_path = config.PROJECTS_FILE.with_suffix('.json.bak')
                try:
                    config.PROJECTS_FILE.rename(backup_path)
                    logger.info(f"Backed up corrupted file to {backup_path}")
                except OSError:
                    pass
                self._projects = {}
            except FileNotFoundError:
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
        """Save projects to file atomically to prevent corruption."""
        data = json.dumps(self._projects, indent=2)
        
        # Write to temp file in same directory for atomic rename
        fd, tmp_path = tempfile.mkstemp(
            dir=config.CONFIG_DIR,
            suffix='.tmp',
            prefix='projects_'
        )
        try:
            os.write(fd, data.encode('utf-8'))
            os.fsync(fd)  # Ensure written to disk
            os.close(fd)
            # Atomic replace (POSIX guarantees this is atomic)
            os.replace(tmp_path, config.PROJECTS_FILE)
        except Exception:
            # Clean up temp file on error
            try:
                os.close(fd)
            except OSError:
                pass
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
    
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
        """Add a project to registry with validation.
        
        Args:
            name: Project name (alphanumeric, dash, underscore only)
            path: Project directory path
            
        Raises:
            ValueError: If name is invalid or path is not accessible
        """
        # Validate name
        if not name:
            raise ValueError("Project name cannot be empty")
        
        if not PROJECT_NAME_PATTERN.match(name):
            raise ValueError(
                f"Invalid project name '{name}'. Use only letters, numbers, dashes, and underscores."
            )
        
        # Resolve and validate path
        try:
            resolved = path.expanduser().resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid path: {e}")
        
        # Path must exist and be a directory
        if not resolved.exists():
            raise ValueError(f"Path does not exist: {path}")
        
        if not resolved.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        
        # Security: Prevent path traversal outside home
        try:
            resolved.relative_to(Path.home())
        except ValueError:
            # Allow if it's under /Volumes (macOS external drives) or similar
            # but warn about it
            if not str(resolved).startswith(('/Volumes/', '/mnt/', '/media/')):
                logger.warning(f"Project outside home directory: {resolved}")
        
        self._projects[name] = str(resolved)
        self.save()
        logger.info(f"Added project '{name}' at {resolved}")
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
