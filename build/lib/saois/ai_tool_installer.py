"""
Complete AI tool installation, download, and setup automation
"""
import subprocess
import time
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def download_and_install_windsurf():
    """Complete Windsurf installation workflow."""
    console.print("\n[bold #00ffff]🌊 Windsurf Installation[/bold #00ffff]\n")
    
    # Step 1: Download
    console.print("[#ff00ff]Step 1: Download & Install[/#ff00ff]")
    console.print("Opening download page: https://codeium.com/windsurf")
    
    import webbrowser
    webbrowser.open("https://codeium.com/windsurf")
    
    console.print("\n[dim]Complete these steps:[/dim]")
    console.print("  1. Download Windsurf for your platform")
    console.print("  2. Install the application to /Applications (macOS)")
    console.print("  3. Open Windsurf")
    console.print("  4. [bold]Sign in or create a Codeium account[/bold]")
    console.print("  5. Complete the welcome tutorial (optional)")
    
    console.print("\n[yellow]⚠️  Important: You must sign in for Windsurf to work![/yellow]")
    
    if not Confirm.ask("\nHave you installed AND signed in to Windsurf?", default=False):
        console.print("[yellow]Installation incomplete. Run 'saois setup-tools' when ready.[/yellow]")
        return False
    
    # Step 2: Verify Installation
    console.print("\n[#ff00ff]Step 2: Verify Installation[/#ff00ff]")
    
    from .os_detector import check_tool_installed
    if check_tool_installed("Windsurf"):
        console.print("[#00ff00]✓ Windsurf application detected![/#00ff00]")
        
        # Step 3: Verify Sign-In
        console.print("\n[#ff00ff]Step 3: Verify Sign-In[/#ff00ff]")
        if Confirm.ask("Can you see your account name in Windsurf's top-right corner?", default=True):
            console.print("[#00ff00]✓ Windsurf is fully configured![/#00ff00]")
            console.print("\n[dim]Usage:[/dim]")
            console.print("  • Run: [bold]saois run PROJECT[/bold] to launch Windsurf for coding tasks")
            console.print("  • Windsurf will open with full project context")
            return True
        else:
            console.print("[yellow]⚠️  Please sign in to Windsurf before using it[/yellow]")
            console.print("[dim]Open Windsurf and sign in, then run 'saois doctor' to verify[/dim]")
            return False
    else:
        console.print("[yellow]⚠️  Windsurf not detected[/yellow]")
        console.print("[dim]Make sure it's installed in /Applications (macOS)[/dim]")
        console.print("[dim]Run 'saois doctor' to check again[/dim]")
        return False

def download_and_install_claude():
    """Complete Claude installation workflow."""
    console.print("\n[bold #00ffff]🤖 Claude Desktop Installation[/bold #00ffff]\n")
    
    console.print("[#ff00ff]Step 1: Download & Install[/#ff00ff]")
    console.print("Opening Claude download page...")
    
    import webbrowser
    webbrowser.open("https://claude.ai/download")
    
    console.print("\n[dim]Complete these steps:[/dim]")
    console.print("  1. Download Claude Desktop for your platform")
    console.print("  2. Install the application to /Applications (macOS)")
    console.print("  3. Open Claude Desktop")
    console.print("  4. [bold]Sign in with your Anthropic account[/bold]")
    console.print("  5. If you don't have an account, create one (free tier available)")
    
    console.print("\n[yellow]⚠️  Important: You must sign in for Claude to work![/yellow]")
    
    if not Confirm.ask("\nHave you installed AND signed in to Claude?", default=False):
        console.print("[yellow]Installation incomplete. Run 'saois setup-tools' when ready.[/yellow]")
        return False
    
    console.print("\n[#ff00ff]Step 2: Verify Installation[/#ff00ff]")
    from .os_detector import check_tool_installed
    
    if check_tool_installed("Claude"):
        console.print("[#00ff00]✓ Claude application detected![/#00ff00]")
        
        # Verify sign-in
        console.print("\n[#ff00ff]Step 3: Verify Sign-In[/#ff00ff]")
        if Confirm.ask("Can you see the Claude chat interface (not a login screen)?", default=True):
            console.print("[#00ff00]✓ Claude is fully configured![/#00ff00]")
            console.print("\n[dim]Usage:[/dim]")
            console.print("  • Run: [bold]saois run PROJECT[/bold] to launch Claude for architecture tasks")
            console.print("  • Claude will open with full project context")
            return True
        else:
            console.print("[yellow]⚠️  Please sign in to Claude before using it[/yellow]")
            console.print("[dim]Open Claude and sign in, then run 'saois doctor' to verify[/dim]")
            return False
    else:
        console.print("[yellow]⚠️  Claude not detected[/yellow]")
        console.print("[dim]Make sure it's installed in /Applications (macOS)[/dim]")
        console.print("[dim]Run 'saois doctor' to check again[/dim]")
        return False

def install_all_ai_tools():
    """Interactive workflow to install AI tools - user chooses which ones."""
    from .tool_config import AVAILABLE_TOOLS, check_tool_installed, detect_installed_tools, save_tools_config, load_tools_config
    from rich.table import Table
    from rich import box
    
    console.print("\n[bold #00ffff]🚀 AI Tools Setup Wizard[/bold #00ffff]\n")
    console.print("[dim]Let's set up your AI development tools![/dim]\n")
    
    # Show what's available
    console.print("[bold #ff00ff]Available Tools:[/bold #ff00ff]\n")
    
    table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    table.add_column("#", style="dim", width=3)
    table.add_column("Tool", style="#00ffff")
    table.add_column("Status", justify="center")
    table.add_column("Best For", style="dim")
    
    tool_list = [
        ("windsurf", "Windsurf", "AI-powered coding IDE", "https://codeium.com/windsurf"),
        ("cursor", "Cursor", "AI-first code editor", "https://cursor.sh"),
        ("vscode", "VS Code", "Code editor with AI extensions", "https://code.visualstudio.com"),
        ("claude_desktop", "Claude Desktop", "Architecture & planning", "https://claude.ai/download"),
        ("chatgpt", "ChatGPT", "General AI assistant", "https://chat.openai.com"),
        ("perplexity", "Perplexity", "AI research assistant", "https://perplexity.ai"),
    ]
    
    for i, (tool_id, name, desc, _) in enumerate(tool_list, 1):
        installed = check_tool_installed(tool_id)
        status = "[#00ff00]✓ Installed[/#00ff00]" if installed else "[yellow]Not installed[/yellow]"
        table.add_row(str(i), name, status, desc)
    
    console.print(table)
    console.print()
    
    # Ask which to install
    console.print("[dim]Enter numbers of tools to install (comma-separated), or 'all', or 'skip':[/dim]")
    console.print("[dim]Example: 1,2,4 or all[/dim]")
    selection = Prompt.ask("[#ff00ff]Tools to install[/#ff00ff]", default="1,4")
    
    if selection.lower() == "skip":
        console.print("[dim]Skipped tool installation[/dim]")
        return
    
    # Parse selection
    selected_indices = set()
    if selection.lower() == "all":
        selected_indices = set(range(1, len(tool_list) + 1))
    else:
        for part in selection.split(","):
            part = part.strip()
            if part.isdigit():
                selected_indices.add(int(part))
    
    installed_count = 0
    
    for idx in sorted(selected_indices):
        if 1 <= idx <= len(tool_list):
            tool_id, name, desc, url = tool_list[idx - 1]
            
            console.print(f"\n{'='*60}")
            console.print(f"[bold #ff00ff]{name}[/bold #ff00ff]")
            console.print(f"{'='*60}\n")
            
            # Check if already installed
            if check_tool_installed(tool_id):
                console.print(f"[#00ff00]✓ {name} is already installed![/#00ff00]")
                installed_count += 1
                continue
            
            # Install based on tool type
            if tool_id == "windsurf":
                if download_and_install_windsurf():
                    installed_count += 1
            elif tool_id == "cursor":
                if install_desktop_tool("Cursor", "https://cursor.sh", "/Applications/Cursor.app"):
                    installed_count += 1
            elif tool_id == "vscode":
                if install_desktop_tool("VS Code", "https://code.visualstudio.com", "/Applications/Visual Studio Code.app"):
                    installed_count += 1
            elif tool_id == "claude_desktop":
                if download_and_install_claude():
                    installed_count += 1
            elif tool_id == "chatgpt":
                if install_desktop_tool("ChatGPT", "https://chat.openai.com", "/Applications/ChatGPT.app"):
                    installed_count += 1
            else:
                if install_browser_tool(name, url):
                    installed_count += 1
    
    # Summary
    console.print(f"\n{'='*60}")
    console.print("[bold #00ffff]Setup Complete![/bold #00ffff]")
    console.print(f"{'='*60}\n")
    console.print(f"[#00ff00]✓ {installed_count} tools configured[/#00ff00]\n")
    
    # Offer to configure task routing
    if Confirm.ask("Configure which tool to use for each task type?", default=True):
        from .tool_config import configure_task_mapping
        configure_task_mapping()
    
    console.print("\n[dim]Run 'saois config-tools' anytime to change your tool preferences[/dim]")
    console.print("[dim]Run 'saois run PROJECT' to start working![/dim]")

def install_desktop_tool(name, url, app_path):
    """Install a desktop application."""
    console.print(f"\n[#ff00ff]Step 1: Download {name}[/#ff00ff]")
    console.print(f"Opening {url}...")
    
    import webbrowser
    webbrowser.open(url)
    
    console.print(f"\n[dim]Complete these steps:[/dim]")
    console.print(f"  1. Download {name} for your platform")
    console.print(f"  2. Install the application")
    console.print(f"  3. Open {name} and sign in")
    
    console.print(f"\n[yellow]⚠️  Important: Sign in to {name} before continuing![/yellow]")
    
    if not Confirm.ask(f"\nHave you installed AND signed in to {name}?", default=False):
        console.print(f"[yellow]Setup incomplete. Run 'saois setup-tools' when ready.[/yellow]")
        return False
    
    # Verify installation
    console.print(f"\n[#ff00ff]Step 2: Verify Installation[/#ff00ff]")
    if Path(app_path).exists():
        console.print(f"[#00ff00]✓ {name} detected![/#00ff00]")
        return True
    else:
        console.print(f"[yellow]⚠️  {name} not detected at {app_path}[/yellow]")
        if Confirm.ask("Is it installed in a different location?", default=True):
            console.print(f"[#00ff00]✓ {name} configured![/#00ff00]")
            return True
        return False

def install_browser_tool(tool_name, url):
    """Install a browser-based tool."""
    console.print(f"\n[#ff00ff]Step 1: Access {tool_name}[/#ff00ff]")
    console.print(f"Opening {url}...")
    
    import webbrowser
    webbrowser.open(url)
    
    console.print("\n[dim]Complete these steps:[/dim]")
    console.print(f"  1. [bold]Create an account or sign in[/bold]")
    console.print(f"  2. Complete any onboarding steps")
    console.print(f"  3. Bookmark {url} for easy access")
    console.print(f"  4. Keep the browser tab open or bookmark it")
    
    console.print(f"\n[yellow]⚠️  Important: You must sign in to use {tool_name}![/yellow]")
    
    if not Confirm.ask(f"\nHave you signed in to {tool_name}?", default=False):
        console.print(f"[yellow]Setup incomplete. Run 'saois setup-tools' when ready.[/yellow]")
        return False
    
    # Verify sign-in
    console.print(f"\n[#ff00ff]Step 2: Verify Sign-In[/#ff00ff]")
    if Confirm.ask(f"Can you see your account/profile in {tool_name}?", default=True):
        console.print(f"[#00ff00]✓ {tool_name} is configured![/#00ff00]")
        console.print(f"\n[dim]Usage:[/dim]")
        console.print(f"  • Run: [bold]saois run PROJECT[/bold] to open {tool_name} when needed")
        console.print(f"  • SAOIS will open {url} with project context")
        return True
    else:
        console.print(f"[yellow]⚠️  Please sign in to {tool_name} before using it[/yellow]")
        console.print(f"[dim]Visit {url} and sign in, then run 'saois doctor' to verify[/dim]")
        return False
