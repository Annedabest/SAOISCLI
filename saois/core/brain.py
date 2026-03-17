"""
SAOIS Project Brain
Handles project brain files with smart defaults and auto-creation.
"""
import re
from pathlib import Path
from typing import Optional, Dict, Any
from .config import config

class Brain:
    """Project brain manager with smart defaults."""
    
    # Simple brain template - minimal, easy to understand
    SIMPLE_TEMPLATE = """# {project_name} - Project Brain

## What is this project?
[Brief description of what this project does]

## Current Status
[What stage is this project in? e.g., "In development", "MVP ready", "Needs debugging"]

## What I'm Working On
**Task Type:** code
**Current Task:** [What needs to be done next?]

## How to Run
```bash
# Add your run command here
npm start  # or python main.py, etc.
```

## Notes
[Any important notes for AI assistants]
"""

    # Task type keywords for auto-detection
    TASK_KEYWORDS = {
        "code": ["coding", "implement", "build", "create", "add", "fix", "bug", "feature", "develop"],
        "research": ["research", "find", "search", "learn", "understand", "explore", "investigate"],
        "plan": ["plan", "design", "architect", "structure", "organize", "refactor", "review"],
    }
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.brain_file = project_path / "docs" / "project_brain.md"
        self._data: Dict[str, Any] = {}
        self._load()
    
    def _load(self):
        """Load brain data from file."""
        if not self.brain_file.exists():
            return
        
        try:
            content = self.brain_file.read_text()
            self._parse(content)
        except:
            pass
    
    def _parse(self, content: str):
        """Parse brain file content."""
        # Extract task type
        task_match = re.search(r'\*\*Task Type:\*\*\s*(\w+)', content, re.IGNORECASE)
        if task_match:
            self._data['task_type'] = task_match.group(1).lower().strip()
        else:
            # Try old format
            task_match = re.search(r'NEXT TASK TYPE:\s*(\w+)', content, re.IGNORECASE)
            if task_match:
                self._data['task_type'] = task_match.group(1).lower().strip()
        
        # Extract current task
        task_match = re.search(r'\*\*Current Task:\*\*\s*(.+?)(?:\n|$)', content)
        if task_match:
            self._data['current_task'] = task_match.group(1).strip()
        else:
            # Try old format
            task_match = re.search(r'NEXT TASK:\s*(.+?)(?:\n|$)', content)
            if task_match:
                self._data['current_task'] = task_match.group(1).strip()
        
        # Extract status
        status_match = re.search(r'## Current Status\s*\n(.+?)(?:\n#|$)', content, re.DOTALL)
        if status_match:
            self._data['status'] = status_match.group(1).strip()
        
        # Extract run command
        run_match = re.search(r'```bash\s*\n(.+?)\n```', content, re.DOTALL)
        if run_match:
            lines = [l.strip() for l in run_match.group(1).split('\n') if l.strip() and not l.strip().startswith('#')]
            if lines:
                self._data['run_command'] = lines[0]
    
    def exists(self) -> bool:
        """Check if brain file exists."""
        return self.brain_file.exists()
    
    def is_template(self) -> bool:
        """Check if brain is still using template (not customized)."""
        if not self.exists():
            return True
        
        content = self.brain_file.read_text()
        template_markers = [
            "[Brief description",
            "[What stage",
            "[What needs to be done",
            "[Your project name]",
            "Leave empty if not applicable"
        ]
        
        return any(marker in content for marker in template_markers)
    
    def get_task_type(self) -> str:
        """Get task type with smart default."""
        if 'task_type' in self._data:
            return self._data['task_type']
        
        # Default to 'code' - most common use case
        return "code"
    
    def get_current_task(self) -> Optional[str]:
        """Get current task description."""
        return self._data.get('current_task')
    
    def get_status(self) -> Optional[str]:
        """Get project status."""
        return self._data.get('status')
    
    def get_run_command(self) -> Optional[str]:
        """Get run command."""
        return self._data.get('run_command')
    
    def create(self, task_type: str = "code") -> bool:
        """Create a new brain file with smart defaults."""
        # Create docs directory
        docs_dir = self.project_path / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Generate content
        project_name = self.project_path.name
        content = self.SIMPLE_TEMPLATE.format(project_name=project_name)
        content = content.replace("**Task Type:** code", f"**Task Type:** {task_type}")
        
        # Auto-detect run command based on project type
        run_cmd = self._detect_run_command()
        if run_cmd:
            content = content.replace("npm start  # or python main.py, etc.", run_cmd)
        
        self.brain_file.write_text(content)
        self._load()
        return True
    
    def _detect_run_command(self) -> Optional[str]:
        """Auto-detect run command based on project files."""
        # Check for package.json (Node.js)
        if (self.project_path / "package.json").exists():
            try:
                import json
                pkg = json.loads((self.project_path / "package.json").read_text())
                scripts = pkg.get("scripts", {})
                if "dev" in scripts:
                    return "npm run dev"
                elif "start" in scripts:
                    return "npm start"
            except:
                pass
            return "npm start"
        
        # Check for Python
        if (self.project_path / "requirements.txt").exists():
            if (self.project_path / "main.py").exists():
                return "python main.py"
            elif (self.project_path / "app.py").exists():
                return "python app.py"
            return "python main.py"
        
        # Check for Docker
        if (self.project_path / "docker-compose.yml").exists():
            return "docker-compose up"
        
        # Check for Rust
        if (self.project_path / "Cargo.toml").exists():
            return "cargo run"
        
        # Check for Go
        if (self.project_path / "go.mod").exists():
            return "go run ."
        
        return None
    
    def update_task_type(self, task_type: str):
        """Update the task type in the brain file."""
        if not self.exists():
            self.create(task_type)
            return
        
        content = self.brain_file.read_text()
        
        # Update task type
        if "**Task Type:**" in content:
            content = re.sub(r'\*\*Task Type:\*\*\s*\w+', f'**Task Type:** {task_type}', content)
        elif "NEXT TASK TYPE:" in content:
            content = re.sub(r'NEXT TASK TYPE:\s*\w+', f'NEXT TASK TYPE: {task_type}', content)
        else:
            # Add task type section
            content += f"\n\n**Task Type:** {task_type}\n"
        
        self.brain_file.write_text(content)
        self._data['task_type'] = task_type


def get_brain(project_path: Path) -> Brain:
    """Get brain instance for a project."""
    return Brain(project_path)
