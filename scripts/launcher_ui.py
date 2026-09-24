import os
import sys
import time
from datetime import datetime

import codecs
try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.align import Align
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# We initialize a separate console for UI rendering
_utf8_stdout = codecs.getwriter('utf-8')(sys.stdout.buffer) if hasattr(sys.stdout, 'buffer') else sys.stdout
console = Console(file=_utf8_stdout, highlight=False) if HAS_RICH else None

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def show_help(query=None):
    """
    PURPOSE: This is the 'Quick Guide'. It prints specifically what you need to know.
    If a query is provided (e.g., 'git'), it highlights relevant commands.
    """
    print("\n" + "="*42)
    print("   🛡️ CyberShield AI - COMMAND HELP        ")
    print("="*42)
    
    help_data = [
        ("1/run/start/dashboard", "Launch Dashboard (Integrated)"),
        ("2/ext", "Launch Dashboard (External Window)"),
        ("3/jupyter/notebook", "Launch Jupyter (Integrated)"),
        ("4", "Launch Jupyter (External Window)"),
        ("5/harden/setup/fix", "Harden Environment (Self-Repair)"),
        ("6/github/repo/source", "Open GitHub Repository"),
        ("7/venv/switch", "Switch to Virtual Environment"),
        ("8/upgrade/migrate", "Auto-upgrade to Venv & Restart"),
        ("9/pull/update", "Git: Pull latest code changes"),
        ("10/push/sync", "Git: Commit and Push changes"),
        ("11/ignore", "Git: Edit .gitignore file"),
        ("12/audit/version/path", "Check Python Versions & Paths"),
        ("13/restart/refresh", "Restart the Launcher"),
        ("14/exit/stop/quit", "Close the Launcher"),
        ("15/global/cs/register", "Enable Global 'cs' Command"),
        ("16/reset", "Reset Browser Preferences"),
        ("17/bro/cyber/alias", "Enable ALL Global Aliases (cs, bro, cyber)"),
        ("18/speed/network/test", "Run Network Speed Test"),
        ("19/help/guide", "Open Comprehensive Help Guide"),
        ("20/log/logs/audit", "View Audit Logs (Notepad)"),
        ("21/copy/snapshot/serverlog", "Copy Server Logs (no freeze, server keeps running)"),
        ("22/orbit/ai", "Orbit AI Nodes (chat / conversations / connection test)")
    ]
    
    found = False
    query_str = str(query).lower() if query else ""
    
    for cmd, desc in help_data:
        if not query or query_str in cmd.lower() or query_str in desc.lower():
            label = f"{CYAN}{cmd:25}{RESET}"
            print(f" {label} : {desc}")
            found = True
            
    if not found:
        print(f"{YELLOW}[!] No specific help for '{query}'. Showing all commands:{RESET}")
        for cmd, desc in help_data:
            print(f" {CYAN}{cmd:25}{RESET} : {desc}")

    print("\n[TIP] You can speak naturally: 'help git', 'run help', or 'harden fix'.")
    print("="*42)
    input("Press ENTER to return to menu...")

def boot_loader(context):
    """PURPOSE: A high-tech 'Boot Sequence' for a professional first impression."""
    if not HAS_RICH:
        return

    # Check terminal width for initial clear to avoid weird wrapping
    os.system('cls' if os.name == 'nt' else 'clear')

    if context.get("FAST_BOOT", False):
        time.sleep(0.3)
    else:
        time.sleep(0.5)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40, pulse_style="bright_cyan"),
            transient=True,
            console=console
        ) as progress:
            
            task1 = progress.add_task("[cyan]Initializing Core Registry...", total=100)
            task2 = progress.add_task("[magenta]Loading Neural Weights...", total=100)
            task3 = progress.add_task("[yellow]Synchronizing Uplink...", total=100)

            while not progress.finished:
                progress.update(task1, advance=2)
                if progress.tasks[0].percentage > 40: progress.update(task2, advance=3)
                if progress.tasks[1].percentage > 30: progress.update(task3, advance=5)
                time.sleep(0.03)

    h = context.get('health_data', {})
    if h.get("score", 0) < 70:
        console.print(Panel(
            f"[bold red]⚠️  SYSTEM INTEGRITY ALERT: {h.get('score')}%[/]\n[yellow]Reason: {h.get('msg')}[/]",
            title="[bold red]PRE-FLIGHT DIAGNOSTIC[/]", border_style="red"
        ))
        console.print("\n[bold cyan][?] AUTO-REPAIR RECOMMENDED[/bold cyan]")
        fix = input("Would you like me to attempt an Auto-Repair (Harden) now? (y/n): ").lower()
        if fix == 'y':
            return "harden"
        else:
            return "ignore"
    else:
        console.print(Align.center(f"[bold green]✅ SYSTEM NOMINAL: {h.get('score', 100)}% INTEGRITY VERIFIED[/]"))
        time.sleep(0.8)
    return "ok"


def render_premium_menu(context, current_input=""):
    """
    PURPOSE: This is the 'Wow Factor' UI. It builds a beautiful two-column dashboard
    that adapts to the terminal width to prevent line wrapping and border breaks.
    """
    if not HAS_RICH:
        return "" 

    stats = context.get("stats", {"cpu": 0, "ram": 0, "disk": 0})
    h = context.get("health_data", {"score": 100, "status": "Good", "color": "green", "msg": "Ok"})
    IS_ADMIN = context.get("IS_ADMIN", False)
    IS_VIRTUAL = context.get("IS_VIRTUAL", False)
    VENV_NAME = context.get("VENV_NAME", ".venv")
    version = context.get("VERSION", "2.8.0")
    log_file = context.get("LOG_FILE", "launcher_debug.log")
    has_psutil = context.get("HAS_PSUTIL", False)
    net_online = context.get("net_online", False)
    
    # 0. HEADER WITH LIVE CLOCK & ADMIN STATUS
    now = datetime.now().strftime("%I:%M %p")
    admin_tag = "[bold green]ADMIN[/]" if IS_ADMIN else "[bold yellow]USER[/]"
    
    header_grid = Table.grid(expand=True)
    header_grid.add_column(justify="left", ratio=1)
    header_grid.add_column(justify="center", ratio=2)
    header_grid.add_column(justify="right", ratio=1)
    
    env_badge = f"[bold white]Env:[/] [bold {('green' if IS_VIRTUAL else 'yellow')}]{VENV_NAME}[/]"
    center_title = f"[bold cyan]CYBERSHIELD COMMAND CENTER[/]  [dim]{version}[/]"
    status_badge = f"{admin_tag} | [bold cyan]{now}[/]"
    
    header_grid.add_row(env_badge, center_title, status_badge)
    header_panel = Panel(header_grid, border_style="cyan", padding=(0, 0))

    # 1. TOP BAR: SYSTEM STATUS (Real-time Telemetry)
    stats_text = Text.assemble(
        (f"💻 CPU: {stats['cpu']}% ", "bold green" if stats['cpu'] < 70 else "bold red"),
        (f" | 💾 RAM: {stats['ram']}% ", "bold blue" if stats['ram'] < 80 else "bold red"),
        (f" | 📂 DISK: {stats['disk']}% ", "bold white"),
        (" | ", "white"),
        Text.from_markup(f"[bold {h['color']}]Integrity: {h['status']}[/]"),
        (" | ", "white"),
        Text.from_markup(f"[bold cyan]Py: {sys.executable.split('\\')[-1]}[/]")
    )
    telemetry_panel = Panel(Align.center(stats_text), border_style="bright_blue", padding=(0, 0))
    
    # RESPONSIVE WIDTH DETECTION
    term_width = console.measure(header_panel).maximum
    # If the terminal is narrower than 90 chars, stack panels vertically instead of side-by-side
    use_stacked_layout = term_width < 90

    # 2. LEFT MENU COLUMN
    if IS_ADMIN:
        menu_columns = Table.grid(expand=True)
        menu_columns.add_column(ratio=1)
        menu_columns.add_column(ratio=1)
        
        launch_text = "[bold green]1.[/] WebApp (Int)   [bold green]2.[/] WebApp (Ext)\n[bold green]3.[/] Jupyter NB    [bold green]4.[/] Jupyter (Ext)"
        system_text = "[bold magenta]5.[/] Harden Env    [bold magenta]6.[/] GitHub Repo\n[bold magenta]7.[/] Switch Venv   [bold magenta]8.[/] Auto-Upgrade"
        git_text    = "[bold yellow]9.[/] Git Pull     [bold yellow]10.[/] Git Sync\n[bold yellow]11.[/] Edit Ignore"
        
        maint_grid = Table.grid(expand=True)
        maint_grid.add_column(ratio=1)
        maint_grid.add_column(ratio=1)
        maint_grid.add_row("[bold cyan]12.[/] Audit Sys", "[bold red]13.[/] Restart")
        maint_grid.add_row("[bold red]14.[/] Exit Hub", "[bold yellow]15.[/] Add 'cs'")
        maint_grid.add_row("[bold cyan]16.[/] Reset Browser", "[bold cyan]17.[/] Aliases")
        maint_grid.add_row("[bold green]18.[/] Speed Test", "[bold white]19.[/] Help")
        maint_grid.add_row("[bold cyan]20.[/] Audit Logs", "[bold cyan]21.[/] Copy Logs")
        maint_grid.add_row("[bold magenta]22.[/] Orbit AI", "")
        
        menu_columns.add_row(
            Panel(launch_text, title="[green]LAUNCH[/]", border_style="green"),
            Panel(system_text, title="[magenta]OPS[/]", border_style="magenta")
        )
        menu_columns.add_row(
            Panel(git_text, title="[yellow]GIT[/]", border_style="yellow"),
            Panel(maint_grid, title="[blue]MAINT[/]", border_style="blue")
        )
        left_col = menu_columns
        sidebar_height = 10 if not use_stacked_layout else None
    else:
        user_opt_grid = Table.grid(expand=True)
        user_opt_grid.add_column(ratio=1)
        user_opt_grid.add_column(ratio=1)

        user_opt_grid.add_row("[bold green] 1[/] WebApp (Int)",   "[bold green] 2[/] WebApp (Ext)")
        user_opt_grid.add_row("[bold green] 3[/] Jupyter NB",     "[bold green] 4[/] Jupyter (Ext)")
        user_opt_grid.add_row("[bold magenta] 5[/] Harden Env",    "[bold magenta] 6[/] GitHub Repo")
        user_opt_grid.add_row("[bold magenta] 7[/] Switch Venv",   "[bold magenta] 8[/] Auto-Upgrade")
        user_opt_grid.add_row("[bold yellow] 9[/] Git Pull",      "[bold yellow]10[/] Git Sync")
        user_opt_grid.add_row("[bold yellow]11[/] Edit Ignore",   "[bold cyan]12[/] Diagnostic")
        user_opt_grid.add_row("[bold red]13[/] Restart",       "[bold red]14[/] Exit Hub")
        user_opt_grid.add_row("[bold cyan]20[/] Audit Logs",  "[bold cyan]21[/] Copy Logs")
        user_opt_grid.add_row("[bold magenta]22[/] Orbit AI", "")

        left_col = Panel(user_opt_grid, title="[bold cyan]COMMANDS[/]", border_style="cyan", padding=(0, 2))
        sidebar_height = 9 if not use_stacked_layout else None

    # 3. RIGHT STATUS COLUMN
    net_status   = "[bold green]ONLINE[/]"  if net_online else "[bold red]OFFLINE[/]"
    venv_status  = "[bold green]ACTIVE[/]"  if IS_VIRTUAL else "[bold yellow]GLOBAL[/]"
    rich_status  = "[bold green]READY[/]"   if HAS_RICH else "[bold red]MISSING[/]"
    psutil_status= "[bold green]READY[/]"   if has_psutil else "[bold red]MISSING[/]"
    admin_status = "[bold green]ADMIN[/]"   if IS_ADMIN else "[bold yellow]USER[/]"

    status_table = Table(show_header=True, header_style="bold cyan", box=None, expand=True)
    status_table.add_column("NODE", style="dim")
    status_table.add_column("STATUS", justify="right")
    
    status_table.add_row("Network",    net_status)
    status_table.add_row("Venv",       venv_status)
    status_table.add_row("Rich TUI",   rich_status)
    status_table.add_row("Telemetry",  psutil_status)
    status_table.add_row("Privilege",  admin_status)
    
    sidebar_panel = Panel(status_table, title="[cyan]STATUS[/]", border_style="cyan", padding=(0, 1), height=sidebar_height)

    # DYNAMIC LAYOUT COMBINATION
    if use_stacked_layout:
        main_display = Group(left_col, sidebar_panel)
    else:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=2)
        grid.add_column(justify="left", ratio=1)
        grid.add_row(left_col, sidebar_panel)
        main_display = grid

    # 4. ASSEMBLE ALL COMPONENTS
    components = [header_panel]
    if IS_ADMIN: components.append(telemetry_panel)
    components.append(main_display)
    
    footer = Text()
    footer = Text.from_markup(f"  [bold green]Tip: Type 'help' for details[/]  |  [dim white]Session Log: {os.path.basename(log_file)}[/]\n")
    
    components.append(footer)

    return Group(*components)
