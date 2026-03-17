"""
SAOIS Tool Router
Handles launching AI tools with smart fallbacks.
"""
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional, Tuple
from .config import config
from .brain import Brain

class Router:
    """AI tool router with smart fallbacks."""
    
    def __init__(self):
        self.config = config
    
    def get_tool_for_project(self, project_path: Path) -> Tuple[str, str]:
        """
        Get the best tool for a project based on its brain.
        Returns (tool_id, task_type).
        """
        brain = Brain(project_path)
        task_type = brain.get_task_type()
        tool_id = self.config.get_best_tool_for_task(task_type)
        return tool_id, task_type
    
    def launch_tool(self, tool_id: str, project_path: Path) -> Tuple[bool, str]:
        """
        Launch a tool with the project path.
        Returns (success, message).
        """
        tool_name = self.config.TOOL_NAMES.get(tool_id, tool_id)
        
        # Check if tool is installed
        if not self.config.is_tool_installed(tool_id):
            # Use browser fallback
            url = self.config.TOOL_URLS.get(tool_id)
            if url:
                webbrowser.open(url)
                return True, f"Opened {tool_name} in browser"
            return False, f"{tool_name} not installed"
        
        # Get launch command
        cmd, args = self.config.get_tool_launch_command(tool_id, project_path)
        
        if cmd is None:
            # Browser fallback
            webbrowser.open(args)  # args is URL in this case
            return True, f"Opened {tool_name} in browser"
        
        try:
            # Launch the tool
            if isinstance(args, list):
                subprocess.Popen([cmd] + args, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([cmd, args],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            return True, f"Launched {tool_name}"
        except Exception as e:
            # Try browser fallback
            url = self.config.TOOL_URLS.get(tool_id)
            if url:
                webbrowser.open(url)
                return True, f"Opened {tool_name} in browser (app launch failed)"
            return False, f"Failed to launch {tool_name}: {e}"
    
    def launch_for_project(self, project_path: Path) -> Tuple[bool, str, str, str]:
        """
        Launch the best tool for a project.
        Returns (success, message, tool_name, task_type).
        """
        tool_id, task_type = self.get_tool_for_project(project_path)
        tool_name = self.config.TOOL_NAMES.get(tool_id, tool_id)
        success, message = self.launch_tool(tool_id, project_path)
        return success, message, tool_name, task_type


# Global router instance
router = Router()
