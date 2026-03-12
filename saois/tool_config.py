"""
Configurable AI tools system for SAOIS CLI
Allows users to set their preferred tools (Windsurf, Cursor, VS Code, Claude, etc.)
"""
import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

console = Console()

CONFIG_DIR = Path.home() / ".saois"
TOOLS_CONFIG_FILE = CONFIG_DIR / "tools_config.json"

# Available AI tools with their details
AVAILABLE_TOOLS = {
    "windsurf": {
        "name": "Windsurf",
        "description": "AI-powered IDE by Codeium",
        "url": "https://codeium.com/windsurf",
        "app_path_mac": "/Applications/Windsurf.app",
        "tasks": ["coding", "debugging"],
        "models": ["Cascade (default)", "GPT-4", "Claude"]
    },
    "cursor": {
        "name": "Cursor",
        "description": "AI-first code editor",
        "url": "https://cursor.sh",
        "app_path_mac": "/Applications/Cursor.app",
        "tasks": ["coding", "debugging"],
        "models": ["GPT-4", "Claude", "Cursor-small"]
    },
    "vscode": {
        "name": "VS Code",
        "description": "Visual Studio Code with AI extensions",
        "url": "https://code.visualstudio.com",
        "app_path_mac": "/Applications/Visual Studio Code.app",
        "tasks": ["coding", "debugging"],
        "models": ["GitHub Copilot", "Cody", "Continue"]
    },
    "claude_desktop": {
        "name": "Claude Desktop",
        "description": "Anthropic's Claude AI assistant",
        "url": "https://claude.ai/download",
        "app_path_mac": "/Applications/Claude.app",
        "tasks": ["architecture", "planning", "research"],
        "models": ["Claude Opus", "Claude Sonnet"]
    },
    "perplexity": {
        "name": "Perplexity",
        "description": "AI-powered research assistant",
        "url": "https://perplexity.ai",
        "app_path_mac": None,  # Browser-based
        "tasks": ["research"],
        "models": ["Perplexity Pro"]
    },
    "chatgpt": {
        "name": "ChatGPT",
        "description": "OpenAI's ChatGPT",
        "url": "https://chat.openai.com",
        "app_path_mac": "/Applications/ChatGPT.app",
        "tasks": ["planning", "research"],
        "models": ["GPT-4", "GPT-4o"]
    }
}

# Default task-to-tool mapping
DEFAULT_TOOL_MAPPING = {
    "coding": "windsurf",
    "debugging": "windsurf",
    "architecture": "claude_desktop",
    "planning": "claude_desktop",
    "research": "perplexity",
    "analysis": "windsurf"
}

def load_tools_config():
    """Load user's tool configuration."""
    if TOOLS_CONFIG_FILE.exists():
        try:
            return json.loads(TOOLS_CONFIG_FILE.read_text())
        except:
            pass
    
    # Return default config
    return {
        "installed_tools": [],
        "task_mapping": DEFAULT_TOOL_MAPPING.copy(),
        "preferred_models": {}
    }

def save_tools_config(config):
    """Save user's tool configuration."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TOOLS_CONFIG_FILE.write_text(json.dumps(config, indent=2))

def check_tool_installed(tool_id):
    """Check if a tool is installed on the system."""
    from .os_detector import check_tool_installed as os_check
    
    # Map tool_id to tool name
    name_map = {
        "windsurf": "Windsurf",
        "claude_desktop": "Claude",
        "cursor": "Cursor",
        "vscode": "VS Code",
        "chatgpt": "ChatGPT"
    }
    
    tool_name = tool_name_map.get(tool_id)
    if tool_name:
        return os_check_tool(tool_name)
    
    # Browser-based tools are NOT installed
    return False

def detect_installed_tools():
    """Detect which AI tools are installed."""
    installed = []
    for tool_id, tool_info in AVAILABLE_TOOLS.items():
        if check_tool_installed(tool_id):
            installed.append(tool_id)
    return installed

def show_tool_selection_menu():
    """Interactive menu for selecting AI tools."""
    console.print("\n[bold #00ffff]🛠️  Configure Your AI Tools[/bold #00ffff]\n")
    console.print("[dim]Select which tools you want to use with SAOIS:[/dim]\n")
    
    config = load_tools_config()
    
    # Show available tools
    table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    table.add_column("#", style="dim", width=3)
    table.add_column("Tool", style="#00ffff")
    table.add_column("Status", justify="center")
    table.add_column("Used For", style="dim")
    
    tool_list = list(AVAILABLE_TOOLS.items())
    for i, (tool_id, tool_info) in enumerate(tool_list, 1):
        installed = check_tool_installed(tool_id)
        status = "[#00ff00]✓ Installed[/#00ff00]" if installed else "[yellow]Not installed[/yellow]"
        tasks = ", ".join(tool_info["tasks"])
        table.add_row(str(i), tool_info["name"], status, tasks)
    
    console.print(table)
    console.print()
    
    return tool_list

def configure_task_mapping():
    """Let user configure which tool to use for each task type."""
    console.print("\n[bold #00ffff]📋 Configure Task Routing[/bold #00ffff]\n")
    console.print("[dim]Choose which tool to use for each task type:[/dim]\n")
    
    config = load_tools_config()
    installed = detect_installed_tools()
    
    if not installed:
        console.print("[yellow]No AI tools detected. Run 'saois setup-tools' first.[/yellow]")
        return
    
    task_types = ["coding", "debugging", "architecture", "planning", "research", "analysis"]
    
    for task in task_types:
        current = config["task_mapping"].get(task, "windsurf")
        current_name = AVAILABLE_TOOLS.get(current, {}).get("name", current)
        
        # Filter to installed tools that support this task
        valid_tools = []
        for tool_id in installed:
            tool_info = AVAILABLE_TOOLS.get(tool_id, {})
            if task in tool_info.get("tasks", []):
                valid_tools.append(tool_id)
        
        if not valid_tools:
            valid_tools = installed  # Fallback to all installed
        
        choices = [AVAILABLE_TOOLS[t]["name"] for t in valid_tools]
        
        console.print(f"[#ff00ff]{task.capitalize()}[/#ff00ff] (current: {current_name})")
        
        if len(choices) == 1:
            console.print(f"  [dim]Only {choices[0]} available[/dim]")
            config["task_mapping"][task] = valid_tools[0]
        else:
            choice = Prompt.ask(
                f"  [dim]Choose tool[/dim]",
                choices=choices,
                default=current_name if current_name in choices else choices[0]
            )
            # Find tool_id from name
            for tool_id in valid_tools:
                if AVAILABLE_TOOLS[tool_id]["name"] == choice:
                    config["task_mapping"][task] = tool_id
                    break
    
    save_tools_config(config)
    console.print("\n[#00ff00]✓ Task routing configured![/#00ff00]")

def get_tool_for_task(task_type):
    """Get the configured tool for a task type."""
    config = load_tools_config()
    tool_id = config["task_mapping"].get(task_type, DEFAULT_TOOL_MAPPING.get(task_type, "windsurf"))
    return AVAILABLE_TOOLS.get(tool_id, AVAILABLE_TOOLS["windsurf"])

def show_current_config():
    """Display current tool configuration."""
    config = load_tools_config()
    installed = detect_installed_tools()
    
    console.print("\n[bold #00ffff]⚙️  Current Configuration[/bold #00ffff]\n")
    
    # Installed tools
    console.print("[#ff00ff]Installed Tools:[/#ff00ff]")
    if installed:
        for tool_id in installed:
            tool_name = AVAILABLE_TOOLS[tool_id]["name"]
            console.print(f"  [#00ff00]✓[/#00ff00] {tool_name}")
    else:
        console.print("  [yellow]None detected[/yellow]")
    
    console.print()
    
    # Task mapping
    console.print("[#ff00ff]Task Routing:[/#ff00ff]")
    for task, tool_id in config["task_mapping"].items():
        tool_name = AVAILABLE_TOOLS.get(tool_id, {}).get("name", tool_id)
        console.print(f"  {task}: [#00ffff]{tool_name}[/#00ffff]")
