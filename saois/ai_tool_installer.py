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
    """Interactive workflow to install all 5 AI tools."""
    console.print("\n[bold #00ffff]🚀 Complete AI Tools Setup[/bold #00ffff]\n")
    console.print("[dim]This wizard will help you install all 5 AI tools:[/dim]")
    console.print("  1. Windsurf - Coding & Debugging")
    console.print("  2. Claude - Architecture & Planning")
    console.print("  3. Perplexity - Research")
    console.print("  4. Cody - Code Analysis")
    console.print("  5. Continue - Automation\n")
    
    if not Confirm.ask("Start installation wizard?", default=True):
        return
    
    from .os_detector import check_tool_installed
    from .installer import TOOL_DETAILS
    
    tools_to_install = [
        ("Windsurf", download_and_install_windsurf),
        ("Claude", download_and_install_claude),
        ("Perplexity", lambda: install_browser_tool("Perplexity", "https://perplexity.ai")),
        ("Cody", lambda: install_browser_tool("Cody", "https://sourcegraph.com/cody")),
        ("Continue", lambda: install_browser_tool("Continue", "https://continue.dev"))
    ]
    
    installed_count = 0
    
    for tool_name, install_func in tools_to_install:
        console.print(f"\n{'='*60}")
        console.print(f"[bold #ff00ff]{tool_name}[/bold #ff00ff]")
        console.print(f"{'='*60}\n")
        
        # Check if already installed
        if check_tool_installed(tool_name):
            console.print(f"[#00ff00]✓ {tool_name} is already installed![/#00ff00]")
            installed_count += 1
            
            if not Confirm.ask("Skip to next tool?", default=True):
                break
            continue
        
        # Offer to install
        if Confirm.ask(f"Install {tool_name}?", default=True):
            if install_func():
                installed_count += 1
        else:
            console.print(f"[dim]Skipped {tool_name}[/dim]")
    
    # Summary
    console.print(f"\n{'='*60}")
    console.print("[bold #00ffff]Installation Complete![/bold #00ffff]")
    console.print(f"{'='*60}\n")
    console.print(f"[#00ff00]✓ {installed_count}/5 tools installed[/#00ff00]\n")
    
    if installed_count == 5:
        console.print("[#00ff00]🎉 All AI tools are ready![/#00ff00]")
        console.print("[dim]Run 'saois run PROJECT' to start using them[/dim]")
    else:
        console.print(f"[yellow]{5 - installed_count} tools remaining[/yellow]")
        console.print("[dim]Run 'saois doctor' anytime to check status[/dim]")
        console.print("[dim]Run 'saois setup-tools' to continue installation[/dim]")

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
