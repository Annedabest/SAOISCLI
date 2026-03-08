"""
Tool Routing Logic - Maps task types to AI tools
"""
from pathlib import Path
import re

# Tool mapping
TOOL_MAP = {
    "coding": {"name": "Windsurf", "command": "windsurf", "url": "https://codeium.com/windsurf"},
    "debugging": {"name": "Windsurf", "command": "windsurf", "url": "https://codeium.com/windsurf"},
    "architecture": {"name": "Claude Code", "command": "claude", "url": "https://claude.ai/code"},
    "research": {"name": "Perplexity AI", "command": "perplexity", "url": "https://perplexity.ai"},
    "analysis": {"name": "Sourcegraph Cody", "command": "cody", "url": "https://sourcegraph.com/cody"},
    "automation": {"name": "Continue.dev", "command": "continue", "url": "https://continue.dev"},
    "planning": {"name": "Claude Code", "command": "claude", "url": "https://claude.ai/code"}
}

def read_project_brain(project_path):
    """Read and parse the project brain file."""
    brain_file = Path(project_path) / "docs" / "project_brain.md"
    
    if not brain_file.exists():
        return None
    
    try:
        content = brain_file.read_text()
        
        # Extract project info
        brain_data = {
            "project_name": extract_field(content, "PROJECT NAME"),
            "mission": extract_field(content, "MISSION"),
            "current_status": extract_field(content, "CURRENT STATUS"),
            "architecture": extract_field(content, "ARCHITECTURE SUMMARY"),
            "known_issues": extract_field(content, "KNOWN ISSUES"),
            "next_task_type": extract_field(content, "NEXT TASK TYPE"),
            "next_task": extract_field(content, "NEXT TASK"),
            "raw_content": content
        }
        
        return brain_data
    except Exception as e:
        return None

def extract_field(content, field_name):
    """Extract a field value from the project brain content."""
    pattern = rf"{field_name}:\s*\n?(.*?)(?=\n[A-Z\s]+:|$)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if match:
        value = match.group(1).strip()
        return value if value else None
    return None

def get_tool_for_task(task_type):
    """Get the appropriate tool for a task type."""
    if not task_type:
        return None
    
    task_type = task_type.lower().strip()
    return TOOL_MAP.get(task_type)

def check_ai_rules_exists(project_path):
    """Check if .ai_rules.md exists in the project."""
    ai_rules = Path(project_path) / ".ai_rules.md"
    return ai_rules.exists()

def get_project_brain_template():
    """Return the project brain template."""
    return """PROJECT NAME:
[Your project name]

MISSION:
[What this project does]

CURRENT STATUS:
[Current development state]

ARCHITECTURE SUMMARY:
[High-level architecture]

KNOWN ISSUES:
[List of known problems]

NEXT TASK TYPE:
[coding | research | architecture | debugging | analysis | planning | automation]

NEXT TASK:
[Describe the next development action]
"""

def get_ai_rules_template():
    """Return the AI rules template."""
    return """# AI RULES

Before coding:
1. Read docs/project_brain.md
2. Understand NEXT TASK

Rules:
- Only modify files related to the task
- Do not refactor the whole project
- Prefer small changes
- Maintain compatibility

Recommended Models:
- For simple tasks: GPT-4o-mini, Claude 3.5 Haiku (saves credits)
- For complex architecture: Claude 3.5 Sonnet, GPT-4o
- For debugging: Claude 3.5 Sonnet (best at understanding context)
- For research: Use Perplexity Pro for latest information
"""

def get_recommended_model(task_type):
    """Get recommended AI model for a task type."""
    recommendations = {
        "coding": "Claude 3.5 Sonnet or GPT-4o (for complex), GPT-4o-mini (for simple)",
        "debugging": "Claude 3.5 Sonnet (best context understanding)",
        "architecture": "Claude 3.5 Sonnet or GPT-4o",
        "research": "Perplexity Pro",
        "analysis": "Claude 3.5 Sonnet",
        "automation": "GPT-4o-mini (cost-effective)",
        "planning": "Claude 3.5 Sonnet"
    }
    return recommendations.get(task_type, "Claude 3.5 Sonnet or GPT-4o")
