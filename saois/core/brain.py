"""
SAOIS Project Brain
Handles project brain files with smart defaults and auto-creation.
"""
import re
from importlib import resources
from pathlib import Path
from typing import Any, Dict, List, Optional

SKIP_DIR_NAMES = frozenset(
    {
        "node_modules",
        "venv",
        ".venv",
        "__pycache__",
        "dist",
        "build",
        ".git",
    }
)


def resolve_brain_file(project_path: Path) -> Path:
    """Prefer docs/project_brain.md; otherwise shallow rglob, else canonical path."""
    project_path = project_path.resolve()
    canonical = project_path / "docs" / "project_brain.md"
    if canonical.exists():
        return canonical

    found: List[Path] = []
    try:
        for brain_file in project_path.rglob("project_brain.md"):
            try:
                rel_parts = brain_file.relative_to(project_path).parts
            except ValueError:
                continue
            if any(p.startswith(".") for p in rel_parts):
                continue
            if any(p in SKIP_DIR_NAMES for p in rel_parts):
                continue
            if len(rel_parts) > 4:
                continue
            found.append(brain_file)
    except OSError:
        pass

    if found:
        found.sort(key=lambda p: len(p.parts))
        return found[0]
    return canonical


class Brain:
    """Project brain manager with smart defaults."""

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

    TASK_KEYWORDS = {
        "code": [
            "coding",
            "implement",
            "build",
            "create",
            "add",
            "fix",
            "bug",
            "feature",
            "develop",
        ],
        "research": [
            "research",
            "find",
            "search",
            "learn",
            "understand",
            "explore",
            "investigate",
        ],
        "plan": [
            "plan",
            "design",
            "architect",
            "structure",
            "organize",
            "refactor",
            "review",
        ],
    }

    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()
        self.brain_file = resolve_brain_file(self.project_path)
        self._data: Dict[str, Any] = {}
        self._load()

    def canonical_brain_path(self) -> Path:
        return self.project_path / "docs" / "project_brain.md"

    def is_canonical_location(self) -> bool:
        return self.brain_file.resolve() == self.canonical_brain_path().resolve()

    def _load(self):
        if not self.brain_file.exists():
            return
        try:
            content = self.brain_file.read_text()
            self._parse(content)
        except Exception:
            pass

    def _normalize_task_type(self, raw: str) -> str:
        t = raw.lower().strip()
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
        return task_mapping.get(t, t if t in ("code", "research", "plan") else t)

    def _parse(self, content: str):
        task_match = re.search(
            r"\*\*Task Type:\*\*\s*(\w+)", content, re.IGNORECASE
        )
        if task_match:
            self._data["task_type"] = self._normalize_task_type(
                task_match.group(1).lower().strip()
            )
        else:
            task_match = re.search(
                r"NEXT TASK TYPE:\s*(\w+)", content, re.IGNORECASE
            )
            if task_match:
                self._data["task_type"] = self._normalize_task_type(
                    task_match.group(1).lower().strip()
                )

        task_match = re.search(
            r"\*\*Current Task:\*\*\s*(.+?)(?:\n|$)", content, re.DOTALL
        )
        if task_match:
            self._data["current_task"] = task_match.group(1).strip()
        else:
            task_match = re.search(
                r"NEXT TASK:\s*(.+?)(?=\n[A-Z][A-Z \t]+:|\n---|\Z)",
                content,
                re.DOTALL | re.IGNORECASE,
            )
            if task_match:
                self._data["current_task"] = task_match.group(1).strip()

        status_match = re.search(
            r"## Current Status\s*\n(.+?)(?:\n#|$)", content, re.DOTALL
        )
        if status_match:
            self._data["status"] = status_match.group(1).strip()

        run_match = re.search(r"```bash\s*\n(.+?)\n```", content, re.DOTALL)
        if run_match:
            lines = [
                l.strip()
                for l in run_match.group(1).split("\n")
                if l.strip() and not l.strip().startswith("#")
            ]
            if lines:
                self._data["run_command"] = lines[0]

    def exists(self) -> bool:
        return self.brain_file.exists()

    def is_template(self) -> bool:
        if not self.exists():
            return True
        content = self.brain_file.read_text()
        template_markers = [
            "[Brief description",
            "[What stage",
            "[What needs to be done",
            "[Your project name]",
            "Leave empty if not applicable",
        ]
        return any(marker in content for marker in template_markers)

    def get_task_type(self) -> str:
        if "task_type" in self._data:
            t = self._data["task_type"]
            if t in ("code", "research", "plan"):
                return t
            return self._normalize_task_type(t)
        return "code"

    def get_current_task(self) -> Optional[str]:
        return self._data.get("current_task")

    def get_status(self) -> Optional[str]:
        return self._data.get("status")

    def get_run_command(self) -> Optional[str]:
        return self._data.get("run_command")

    def _load_packaged_template(self) -> str:
        try:
            t = resources.files("saois").joinpath("templates/project_brain_template.md")
            with t.open("r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
        tpl = Path(__file__).resolve().parent.parent / "templates" / "project_brain_template.md"
        if tpl.exists():
            return tpl.read_text(encoding="utf-8")
        return self.SIMPLE_TEMPLATE

    def create(self, task_type: str = "code") -> bool:
        docs_dir = self.project_path / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        self.brain_file = self.canonical_brain_path()

        project_name = self.project_path.name
        template = self._load_packaged_template()
        try:
            content = template.format(project_name=project_name)
        except (KeyError, IndexError):
            content = self.SIMPLE_TEMPLATE.format(project_name=project_name)

        content = re.sub(
            r"(\*\*Task Type:\*\*)\s*\S+",
            rf"\1 {task_type}",
            content,
            count=1,
            flags=re.IGNORECASE,
        )

        run_cmd = self._detect_run_command()
        if run_cmd:
            content = content.replace(
                "npm start  # or python main.py, etc.", run_cmd
            )

        self.brain_file.write_text(content, encoding="utf-8")
        self._load()
        return True

    def _detect_run_command(self) -> Optional[str]:
        if (self.project_path / "package.json").exists():
            try:
                import json

                pkg = json.loads((self.project_path / "package.json").read_text())
                scripts = pkg.get("scripts", {})
                if "dev" in scripts:
                    return "npm run dev"
                if "start" in scripts:
                    return "npm start"
            except Exception:
                pass
            return "npm start"

        if (self.project_path / "requirements.txt").exists():
            if (self.project_path / "main.py").exists():
                return "python main.py"
            if (self.project_path / "app.py").exists():
                return "python app.py"
            return "python main.py"

        if (self.project_path / "docker-compose.yml").exists():
            return "docker-compose up"

        if (self.project_path / "Cargo.toml").exists():
            return "cargo run"

        if (self.project_path / "go.mod").exists():
            return "go run ."

        return None

    def update_task_type(self, task_type: str):
        if not self.exists():
            self.create(task_type)
            return

        content = self.brain_file.read_text()
        if "**Task Type:**" in content:
            content = re.sub(
                r"\*\*Task Type:\*\*\s*\w+",
                f"**Task Type:** {task_type}",
                content,
            )
        elif "NEXT TASK TYPE:" in content:
            content = re.sub(
                r"NEXT TASK TYPE:\s*\w+",
                f"NEXT TASK TYPE: {task_type}",
                content,
            )
        else:
            content += f"\n\n**Task Type:** {task_type}\n"

        self.brain_file.write_text(content, encoding="utf-8")
        self._data["task_type"] = task_type


def get_brain(project_path: Path) -> Brain:
    return Brain(project_path)
