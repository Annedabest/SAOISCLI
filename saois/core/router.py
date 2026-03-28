"""
SAOIS Tool Router
Handles launching AI tools with smart fallbacks.
"""
import subprocess
import webbrowser
from pathlib import Path
from typing import Tuple

from .config import LAUNCH_BROWSER, LAUNCH_DESKTOP, LAUNCH_FAILED, config
from .brain import Brain


class Router:
    """AI tool router with smart fallbacks."""

    def __init__(self):
        self.config = config

    def get_tool_for_project(self, project_path: Path) -> Tuple[str, str]:
        brain = Brain(project_path)
        task_type = brain.get_task_type()
        tool_id = self.config.get_best_tool_for_task(task_type)
        return tool_id, task_type

    def launch_tool(
        self, tool_id: str, project_path: Path
    ) -> Tuple[bool, str, str]:
        """
        Launch a tool with the project path.
        Returns (success, message, mode) where mode is
        launch_desktop | launch_browser | launch_failed (see config module).
        """
        tool_name = self.config.TOOL_NAMES.get(tool_id, tool_id)

        if not self.config.is_tool_installed(tool_id):
            url = self.config.TOOL_URLS.get(tool_id)
            if url:
                webbrowser.open(url)
                return (
                    True,
                    f"Opened the {tool_name} website in your browser (desktop app not detected). "
                    f"Open this project folder in {tool_name} manually: {project_path}",
                    LAUNCH_BROWSER,
                )
            return False, f"{tool_name} not installed", LAUNCH_FAILED

        cmd, args = self.config.get_tool_launch_command(tool_id, project_path)

        if cmd is None:
            webbrowser.open(args)
            return (
                True,
                f"Opened the {tool_name} website in your browser (no desktop launch command). "
                f"Project folder: {project_path}",
                LAUNCH_BROWSER,
            )

        try:
            if isinstance(args, list):
                subprocess.Popen(
                    [cmd] + args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                subprocess.Popen(
                    [cmd, args],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            return (
                True,
                f"Launched {tool_name} with your project folder.",
                LAUNCH_DESKTOP,
            )
        except Exception as e:
            url = self.config.TOOL_URLS.get(tool_id)
            if url:
                webbrowser.open(url)
                return (
                    True,
                    f"Desktop launch failed ({e}); opened the {tool_name} website instead. "
                    f"Project folder: {project_path}",
                    LAUNCH_BROWSER,
                )
            return False, f"Failed to launch {tool_name}: {e}", LAUNCH_FAILED

    def launch_for_project(
        self, project_path: Path
    ) -> Tuple[bool, str, str, str, str]:
        """
        Launch the best tool for a project.
        Returns (success, message, tool_name, task_type, launch_mode).
        """
        tool_id, task_type = self.get_tool_for_project(project_path)
        tool_name = self.config.TOOL_NAMES.get(tool_id, tool_id)
        success, message, mode = self.launch_tool(tool_id, project_path)
        return success, message, tool_name, task_type, mode


router = Router()
