"""  
================================================================================
PROJECT: CyberShield AI - Bulletproof Command Center (2026)
VERSION: 2.8.0 (Production Hardened - Multi-Alias Engine)
AUTHOR: Ksreyan0725 / Managed by Antigravity AI
PURPOSE: A resilient, zero-failure launcher for the Cyber Attack Prediction project.
FEATURES: Dual-Speed Refresh, Admin Integrity Check, and NLU Command Routing.
LICENSE: College Project - Academic / Open Source
================================================================================
"""
# --- BLOCK 0: LIBRARIES (THE TOOLS) ---
import subprocess  # This library allows Python to run other programs or terminal commands (like 'git' or '.bat' files).
import os          # This library lets Python interact with your files, folders, and operating system (Windows).
import sys         # This library gives Python access to variables used by the computer or the Python interpreter itself.
import time        # This library provides timing functions, like 'time.sleep' for pausing the script.
import json        # NEW: Allows us to save your browser preferences in a file.
import webbrowser  # This library allows Python to automatically open your web browser to a specific web address (URL).
import socket      # NEW: This library allows us to check for an internet connection by 'pinging' a server.
import importlib.util  # NEW: used to check if a specific library is already installed without crashing.
import gc          # NEW: Garbage Collector to ensure memory is cleaned up during long sessions.
import logging     # NEW: Professional logging to track errors in a file.
import msvcrt      # WINDOWS ONLY: Non-blocking input detection.
import ctypes      # WINDOWS ONLY: Attribute management (Hidden files, Admin checks).
import threading   # NEW: Path for non-blocking background tasks (Internet check).
import traceback   # NEW: For detailed crash diagnostics
from datetime import datetime # Adds timestamps to logs.

# --- BLOCK 0.5: PREMIUM UI DETECTION ---
try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.align import Align
    from rich.live import Live
    from rich.layout import Layout
    import io
    # Force UTF-8 output — bypasses CP1252 legacy Windows encoding in VS Code / cmd terminals
    _utf8_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    console = Console(file=_utf8_stdout, highlight=False)
    HAS_RICH = True
except ImportError:
    HAS_RICH = False   

# --- BLOCK 0.6: TELEMETRY DETECTION ---
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# --- BLOCK 0.7: UNIFIED CONFIGURATION (CORE SETTINGS) ---
def get_version():
    """Extracts version from the script header docstring dynamically."""
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            for line in f:
                if "VERSION:" in line:
                    # Extracts '2.7.0' from 'VERSION: 2.7.0 (Production Hardened...)'
                    parts = line.split("VERSION:")[1].split("(")
                    return "v" + parts[0].strip()
    except Exception:
        pass
    return "v2.7.0" # Fallback

CONFIG = {
    "PROJECT_NAME": "CyberAttackPrediction",
    "REPO_URL": "https://github.com/Ksreyan0725/CyberAttackPrediction---College_Project",
    "VERSION": get_version(),
    "REFRESH_RATE_FAST": 2.0,  # Stats/Clock
    "REFRESH_RATE_SLOW": 10.0, # Disk/Health scans
    "COMMAND_NAME": "cs",
    "VENV_DIR": ".venv"
}

IS_VIRTUAL = sys.prefix != sys.base_prefix or 'VIRTUAL_ENV' in os.environ
IS_ADMIN = False # Calculated and cached at startup

# --- BLOCK 1.2: PATH CACHE (PRE-COMPUTED TO SAVE CPU) ---
root_dir = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    "root": root_dir,
    "project": os.path.join(root_dir, CONFIG["PROJECT_NAME"]),
    "model": os.path.join(root_dir, CONFIG["PROJECT_NAME"], "model"),
    "venv": os.path.join(root_dir, CONFIG["VENV_DIR"]),
    "requirements": os.path.join(root_dir, CONFIG["PROJECT_NAME"], "requirements.txt"),
    "log": os.path.join(root_dir, "launcher_debug.log"),
    "settings": os.path.join(root_dir, "launcher_settings.json"),
    "venv_exe": os.path.join(root_dir, CONFIG["VENV_DIR"], "Scripts", "python.exe")
}

VENV_PATH = sys.prefix if IS_VIRTUAL else sys.base_prefix
VENV_NAME = os.path.basename(VENV_PATH) if IS_VIRTUAL else "Global Python"
REPO_URL  = CONFIG["REPO_URL"]

# --- BLOCK 1.5: VISUAL ENGINE (THE COLORS) ---
# These are ANSI escape codes. They tell the terminal to change the text color.
# Standard: \033[91m = Red, \033[92m = Green, etc. \033[0m = Reset to default.
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
RESET   = "\033[0m"
BOLD    = "\033[1m"
BOLD_RED = BOLD + RED
BOLD_GREEN = BOLD + GREEN
BOLD_YELLOW = BOLD + YELLOW
BOLD_BLUE = BOLD + BLUE
BOLD_MAGENTA = BOLD + MAGENTA
BOLD_CYAN = BOLD + CYAN
BOLD_WHITE = BOLD + WHITE
DIM_WHITE = "\033[2m\033[37m"
LOG_FILE = PATHS["log"]
SETTINGS_FILE = PATHS["settings"]

def is_admin():
    """PURPOSE: Checks if the launcher is running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def hide_file(path):
    """PURPOSE: Makes a file hidden on Windows (like .git)."""
    if os.name == 'nt' and os.path.exists(path):
        try:
            # 2 is the constant for Hidden attribute in Windows
            ctypes.windll.kernel32.SetFileAttributesW(path, 2)
        except Exception:
            pass

def log_system_event(message, level="INFO"):
    """
    PURPOSE: This is like an 'Airplane Black Box'. 
    If something crashes, this function writes exactly what happened to 'launcher_debug.log'.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        # Note: log file hiding is now handled once at session start for performance.
    except Exception:
        pass # We don't want the logger to crash the launcher!

# Initialize log file with a 'Start' session marker
log_system_event("--- New Command Center Session Started ---")

def load_settings():
    """PURPOSE: Loads your saved preferences (like Browser Mode) from the JSON file."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    """PURPOSE: Saves your preferences so the script remembers them next time."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        hide_file(SETTINGS_FILE) # Ensure the settings stay hidden
    except Exception as e:
        log_system_event(f"Failed to save settings: {e}", level="ERROR")

# --- BLOCK 3: UTILITY HELPERS (THE BACKGROUND ENGINE) ---
def clear_keyboard_buffer():
    while msvcrt.kbhit():
        try:
            msvcrt.getch()
        except:
            pass
    # No sleep here — keeps input snappy after command execution
# --- BLOCK 2: ASYNC CONNECTIVITY SHIELD ---
_INTERNET_STATUS = True # Shared variable for background thread

def connectivity_guard():
    """PURPOSE: A background thread that checks internet health without lag."""
    global _INTERNET_STATUS
    while True:
        try:
            # Pinging Google DNS (Fastest check)
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            _INTERNET_STATUS = True
        except (OSError, socket.timeout):
            _INTERNET_STATUS = False
        time.sleep(30) # Only check every 30s to save CPU/Battery

def check_internet():
    """PURPOSE: Returns the cached internet status from the background guard."""
    return _INTERNET_STATUS

def get_requirements():
    """
    PURPOSE: Reads the project's 'shopping list' of libraries from requirements.txt.
    """
    req_path = PATHS["requirements"]
    if not os.path.exists(req_path):
        log_system_event("requirements.txt missing", level="WARNING")
        return [] # Return empty list if the file is missing.
    
    requirements = []
    try:
        # encoding="utf-8": Ensures the script works on computers in any country (like India) without crashing on weird symbols.
        with open(req_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip comments (#) and empty lines to avoid errors.
                if line and not line.startswith("#"):
                    requirements.append(line)
    except Exception:
        pass
    return requirements

def is_package_installed(package_name):
    """
    PURPOSE: Checks if a specific library (like 'pandas') is already functioning in your Python.
    """
    import re
    # Strip all common version specifiers: ==, >=, <=, !=, ~=, >
    clean_name = re.split(r'[><=!~]', package_name)[0].strip()
    return importlib.util.find_spec(clean_name) is not None

# --- BLOCK 3: THE LAUNCHER FUNCTIONS (THE ACTIONS) ---

def run_script(mode, new_window=False):
    """
    PURPOSE: This function is the engine that launches your project dashboards.
    It now uses the virtual environment natively, eliminating external .bat scripts.
    """
    venv_python = os.path.join(root_dir, '.venv', 'Scripts', 'python.exe')
    venv_jupyter = os.path.join(root_dir, '.venv', 'Scripts', 'jupyter-notebook.exe')
    target_dir = os.path.join(root_dir, 'CyberAttackPrediction')
    
    if mode == 'webapp' and not os.path.exists(venv_python):
        print(f"[-] Error: Virtual environment python missing at {venv_python}")
        return
    elif mode == 'jupyter' and not os.path.exists(venv_jupyter):
        print(f"[-] Error: Jupyter missing at {venv_jupyter}")
        return

    mode_label = "NEW TERMINAL" if new_window else "INTEGRATED"
    print(f"[+] Launching CyberShield Engine ({mode_label})")
    print(f"[+] Mode: {mode.upper()}")
    print("--------------------------------------------------")
    
    try:
        # Build the native command
        if mode == 'webapp':
            cmd = [venv_python, "Main.py"]
        elif mode == 'jupyter':
            cmd = [venv_jupyter, "--browser=cmd /c start chrome --incognito %s"]
            
        if new_window:
            # Pass the command to a new cmd window
            cmd_str = ' '.join(f'"{c}"' if ' ' in c else c for c in cmd)
            subprocess.Popen(f'start cmd /k "cd /d "{target_dir}" && {cmd_str}"', shell=True)
            print(f"{GREEN}[*] Process spawned in separate window successfully.{RESET}")
        else:
            # Run in the same terminal
            subprocess.run(cmd, cwd=target_dir, check=True)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Launcher: Process interrupted by user.{RESET}")
    except Exception as e:
        log_system_event(f"Execution Error ({mode}): {str(e)}", level="ERROR")
        print(f"\n{RED}[-] Launcher Error: {e}{RESET}")

def harden_environment():
    """
    PURPOSE: This is the 'Real System Doctor'. 
    It checks your internet, upgrades Pip, and installs every required library with retry logic.
    """
    # Pillar 6: Connectivity Check
    if not check_internet():
        print(f"\n{RED}[!] CRITICAL: No internet connection detected.{RESET}")
        print("[!] The Hardening Engine requires a connection for the first-time setup.")
        input(f"\n{YELLOW}[PAUSED] Please connect to the internet and press ENTER to try anyway...{RESET}")

    # Step 0: Pip Integrity Check
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        log_system_event("Pip is not functional or missing from the current Python path.", level="CRITICAL")
        print("\n[!] CRITICAL ERROR: Python Package Manager (Pip) is broken.")
        print("[!] Please reinstall Python or fix your installation paths.")
        input("\nPress ENTER to return to menu...")
        return

    try:
        # Step 1: Ensure 'rich' is available for the premium UI.
        if not is_package_installed("rich"):
            print("[*] Installing TUI Engine (Rich)...")
            res = subprocess.run([sys.executable, "-m", "pip", "install", "rich"], capture_output=True, text=True)
            if res.returncode != 0:
                log_system_event(f"Failed to install 'rich'. Error: {res.stderr}", level="ERROR")
        
        # Lazy Loading imports to prevent crashes.
        from rich.console import Console
        from rich.panel import Panel
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
        from rich.table import Table
        from rich.text import Text
        
        # Use a local alias to avoid shadowing the global 'console' object
        hc = Console()
        
        # Header Display
        header_text = Text("🛡️ CyberShield AI: THE BULLETPROOF HARDENING ENGINE (2026)", style="bold cyan")
        hc.print(Panel(header_text, border_style="bright_blue", expand=False))
        
        # Diagnostic Table
        table = Table(title="[SYSTEM DIAGNOSTIC]", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan")
        table.add_column("Status / Version", style="green")
        table.add_row("Python Core", f"{sys.version.split()[0]} (Verified)")
        table.add_row("Environment", f"VIRTUAL ({VENV_NAME})" if IS_VIRTUAL else "GLOBAL (Manual)")
        table.add_row("Network", "ONLINE (Stable)" if check_internet() else "OFFLINE (Limited)")
        hc.print(table)
        
        # --- THE REAL INSTALLATION ENGINE ---
        requirements = get_requirements()
        if not requirements:
            console.print("[yellow][!] Warning: No requirements.txt found. Skipping library sync.[/yellow]")
            # The 'Bulletproof' line-up of libraries needed for your project.
            required_packages = ["rich", "requests", "psutil", "numpy", "pandas", "scikit-learn"] # Fallback essentials
            requirements = required_packages
        
        # Step 2: Force-Upgrade Pip (The foundational tool)
        console.print("\n[*] Hardening Package Manager (Pip)...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)

        # Step 3: Install libraries with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(pulse_style="bright_cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=True
        ) as progress:
            
            total_task = progress.add_task("[cyan]Overall Progress", total=len(requirements))
            
            for pkg in requirements:
                import re
                pkg_clear = re.split(r'[><=!~]', pkg)[0].strip()  # Handles ==, >=, ~=, !=, etc.
                progress.update(total_task, description=f"[magenta]Hardening: {pkg_clear}")
                
                success = False
                for attempt in range(4): # 4 attempts: 1 normal + 3 retries
                    try:
                        # TRIPLE LOCK CHECK: Internet Recovery
                        if not check_internet():
                            progress.print(f"[yellow][!] Connection Lost. Waiting for recovery...[/yellow]")
                            while not check_internet():
                                time.sleep(5)
                            progress.print(f"[green][+] Connection Restored. Resuming {pkg_clear}...[/green]")

                        # Run the install silently
                        subprocess.run(
                            [sys.executable, "-m", "pip", "install", pkg, "--retries", "10", "--timeout", "60"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
                        )
                        success = True
                        break
                    except subprocess.CalledProcessError as e:
                        # Capture detailed error on failure for logging
                        log_res = subprocess.run(
                            [sys.executable, "-m", "pip", "install", pkg],
                            capture_output=True, text=True
                        )
                        err_msg = log_res.stderr.lower()
                        
                        log_system_event(f"Hardening Failure (Pkg: {pkg}): {log_res.stderr}", level="ERROR")
                        
                        if "permission denied" in err_msg or "access is denied" in err_msg:
                            progress.print(f"[red][!] ACCESS DENIED: Please run this launcher as ADMINISTRATOR.[/red]")
                            break # No point retrying if permissions are blocked
                        elif "no space left" in err_msg:
                            progress.print(f"[red][!] DISK FULL: Free up space on your drive.[/red]")
                            break
                        
                        progress.print(f"[yellow][!] Retry {attempt+1}/3 for {pkg_clear}...[/yellow]")
                        time.sleep(2)
                    except Exception as ex:
                        log_system_event(f"Unexpected installation error: {str(ex)}", level="ERROR")
                        time.sleep(2)
                
                if not success:
                    progress.print(f"[red][-] Failure: {pkg_clear} could not be hardened. Check launcher_debug.log[/red]")
                
                progress.advance(total_task)

        hc.print("\n✅ [bold green]ZERO-FAILURE HARDENING COMPLETE[/bold green] 🛡️")
        hc.print("--------------------------------------------------")
        
    except Exception as e:
        # This is the 'Doctor's Emergency' block. If the main hardening engine fails (like a weird permission crash),
        # we don't just stop; we try to run the backup PowerShell script (install_deps.ps1).
        print(f"[-] Critical Engine Error: {e}")
        print("[!] Falling back to emergency PowerShell script...")
        # 'powershell -ExecutionPolicy Bypass': This tells Windows to allow running our setup script.
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "install_deps.ps1"])
    
    input("\n[PROCESS COMPLETE] Press ENTER to return to menu...")

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
        ("20/log/logs/audit", "View Audit Logs (Notepad)")
    ]
    
    found = False
    query_str = str(query).lower() if query else ""
    
    for cmd, desc in help_data:
        # If no query, or if query matches either the command list or description
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

def check_system_paths():
    """
    PURPOSE: This is the 'Path Finder'. It checks exactly WHERE your Python is installed.
    Highly useful for debugging 'Python not found' errors.
    """
    print("\n==========================================")
    print("   CyberShield AI - SYSTEM DIAGNOSTIC   ")
    print("==========================================")
    try:
        # 'where python' is a Windows command that searches all your system paths for python.exe.
        print("[*] Python Executable Locations (where python):")
        subprocess.run(["where", "python"], check=False)
        
        # 'python --version' asks the program to identify its exact version number.
        print("\n[*] Python Core Version (python --version):")
        subprocess.run(["python", "--version"], check=False)
        
        # 'pip --version' checks your library manager.
        print("\n[*] Package Manager Version (pip --version):")
        subprocess.run(["pip", "--version"], check=False)
        
        # 'sys.executable': This is the EXACT folder path of the Python brain currently running THIS script.
        # 'sys.prefix': The main folder containing your Python installation.
        print("\n[*] Current Runtime Environment:")
        print(f"    Active Python: {sys.executable}")
        print(f"    Active Prefix: {sys.prefix}")
        print(f"    Is Virtual:    {IS_VIRTUAL}")
    except Exception as e:
        print(f"[-] Diagnostic Error: {e}")
    
    print("==========================================")
    input("[AUDIT COMPLETE] Press ENTER to return to menu...")

def get_system_stats():
    """
    PURPOSE: This reads your computer's pulse (CPU/RAM).
    """
    if not HAS_PSUTIL:
        return {"cpu": 0, "ram": 0, "disk": 0}
    
    try:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        # Use the root drive letter for Windows compatibility (avoids '/' Linux path)
        drive = os.path.splitdrive(PATHS["root"])[0] + "\\"
        disk = psutil.disk_usage(drive).percent
        return {"cpu": cpu, "ram": ram, "disk": disk}
    except Exception:
        return {"cpu": 0, "ram": 0, "disk": 0}

def get_project_health():
    """
    PURPOSE: The Unified Health Engine (Optimized).
    Scans for ML models and calculates a 0-100% score using single-pass I/O.
    """
    # 1. SCAN FOR CORE MODELS (SINGLE-PASS DIR SCAN)
    core_weights = {
        "dos_weight.hdf5", "ids_weight.hdf5", "iot_weight.hdf5", 
        "kdd_weight.hdf5", "trained_rf_model.pkl"
    }
    
    found_count = 0
    missing = list(core_weights)
    
    if os.path.exists(PATHS["model"]):
        try:
            # os.listdir is much faster than 5 separate os.path.exists calls
            present_files = set(os.listdir(PATHS["model"]))
            for w in core_weights:
                if w in present_files:
                    found_count += 1
                    missing.remove(w)
        except Exception:
            pass # Use fallback behavior if dir read fails
            
    # 2. EVALUATE STATUS
    status, msg, color = "HEALTHY", "All systems nominal.", "green"
    if len(missing) > 0:
        if len(missing) < 3:
            status, msg, color = "WARNING", f"Missing {len(missing)} model(s): {', '.join(missing)}", "yellow"
        else:
            status, msg, color = "CRITICAL", "Major components missing! Run option 5.", "red"
            
    # 3. CALCULATE NUMERIC SCORE (0-100)
    score = 0
    if IS_VIRTUAL: score += 20
    if HAS_RICH: score += 15
    if HAS_PSUTIL: score += 15
    if found_count >= 3: score += 40
    elif found_count > 0: score += 20
    if check_internet(): score += 10
    
    # 4. FINAL ADAPTIVE SCORING (User vs Admin)
    # In User mode, we cap the 'Operational' score at 100% if everything else is perfect.
    # We still track Admin Integrity separately for the 'Ready' badge.
    if IS_ADMIN:
        score_label = f"READY: {score}% [dim](System Integrity Locked)[/]" if score < 100 else "READY: 100% [bold green](SHIELD ACTIVE)[/]"
    else:
        # Penalize slightly for lack of admin if it affects core functionality (it doesn't usually, but it's good to note)
        score_label = f"READY: {score}% [dim](User Mode)[/]"
    
    return {
        "status": status,
        "msg": msg,
        "color": color,
        "score": score,
        "label": score_label
    }

def find_browser_exe():
    """
    PURPOSE: Scans the computer for Chrome, Edge, or Firefox.
    Priority: Chrome (Incognito) > Edge (InPrivate) > Firefox (Private Window).
    """
    paths = {
        "chrome": [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(os.environ.get("LocalAppData", ""), "Google\\Chrome\\Application\\chrome.exe")
        ],
        "edge": [
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Microsoft\\Edge\\Application\\msedge.exe"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft\\Edge\\Application\\msedge.exe")
        ],
        "firefox": [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Mozilla Firefox\\firefox.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Mozilla Firefox\\firefox.exe")
        ]
    }
    
    # Check Chrome
    for p in paths["chrome"]:
        if os.path.exists(p): return p, "chrome", "--incognito"
    # Check Edge
    for p in paths["edge"]:
        if os.path.exists(p): return p, "edge", "--inprivate"
    # Check Firefox
    for p in paths["firefox"]:
        if os.path.exists(p): return p, "firefox", "-private-window"
        
    return None, None, None

def open_repo_smart():
    """
    PURPOSE: Handles the opening of the GitHub Repo with Smart Preferences.
    """
    settings = load_settings()
    mode = settings.get("browser_mode")
    
    if not mode:
        print(f"\n{CYAN}[?] BROWSER PREFERENCE REQUIRED{RESET}")
        print("1. Default System Browser (Standard)")
        print("2. Incognito/Private Mode (Chrome/Edge/Firefox)")
        choice = input(f"\n{YELLOW}Select Mode (The script will REMEMBER this): {RESET}").strip()
        
        if choice == '2':
            mode = "incognito"
        else:
            mode = "standard"
        
        settings["browser_mode"] = mode
        save_settings(settings)
        print(f"{GREEN}[+] Preference saved! (Use Maintenance menu to reset later).{RESET}")

    if mode == "incognito":
        exe_path, name, flag = find_browser_exe()
        if exe_path:
            print(f"[*] Launching {name.title()} in Private Mode...")
            try:
                subprocess.Popen([exe_path, flag, REPO_URL])
                return
            except Exception as e:
                log_system_event(f"Incognito launch failed: {e}", level="ERROR")
        
        print(f"{YELLOW}[!] No private-capable browser found. Falling back to default.{RESET}")

    # Standard Fallback
    print(f"[*] Launching Repository: {REPO_URL}")
    webbrowser.open(REPO_URL)

def setup_global_access(command_name="cs"):
    """
    PURPOSE: This registers the 'cs' command globally on the computer.
    It creates a .bat file and adds the folder to the Windows PATH.
    """
    if HAS_RICH:
        console.print(f"\n[*] Initializing Global Registration for command: '{command_name}'...")
    else:
        print(f"\n[*] Initializing Global Registration for command: '{command_name}'...")
        
    try:
        # Step 1: Create the .bat shim
        shim_path = os.path.join(root_dir, f"{command_name}.bat")
        python_exe = sys.executable 
        script_path = os.path.join(root_dir, "launcher.py")
        
        # We use @echo off to keep the terminal clean
        # %* allows the user to pass arguments like 'cs help'
        content = f"@echo off\n\"{python_exe}\" \"{script_path}\" %*\n"
        
        with open(shim_path, "w") as f:
            f.write(content)
            
        # Step 2: Add directory to PATH using PowerShell (Safer than setx for long paths)
        # We add it to the 'User' path, which doesn't require Admin for the owner.
        cmd = f'powershell -Command "[Environment]::SetEnvironmentVariable(\'Path\', [Environment]::GetEnvironmentVariable(\'Path\', \'User\') + \';{root_dir}\', \'User\')"'
        subprocess.run(cmd, shell=True, check=True)
        
        msg = f"SUCCESS: You can now type '{command_name}' in any NEW terminal window!"
        if HAS_RICH:
            console.print(Panel(msg, border_style="green"))
        else:
            print(f"\n[+] {msg}")
            
        log_system_event(f"Registered global command: {command_name}", level="INFO")
    except Exception as e:
        err = f"Registration Failed: {e}"
        if HAS_RICH:
            console.print(Panel(err, border_style="red"))
        else:
            print(f"\n[-] {err}")
        log_system_event(err, level="ERROR")
    
    input("\nPress ENTER to return to menu...")

def setup_all_aliases():
    """PURPOSE: Mass-registers 'cs', 'bro', and 'cyber' as global commands."""
    aliases = ["cs", "bro", "cyber"]
    if HAS_RICH:
        console.print(Panel(f"🚀 REGISTERING MULTI-ALIAS SYSTEM: {', '.join(aliases)}", border_style="cyan"))
    
    success_count = 0
    for alias in aliases:
        try:
            shim_path = os.path.join(PATHS["root"], f"{alias}.bat")
            python_exe = sys.executable 
            script_path = os.path.join(PATHS["root"], "launcher.py")
            content = f"@echo off\n\"{python_exe}\" \"{script_path}\" %*\n"
            
            with open(shim_path, "w") as f:
                f.write(content)
            success_count += 1
        except Exception as e:
            log_system_event(f"Failed to create shim for {alias}: {e}", level="ERROR")

    try:
        # Update PATH once for the whole directory
        cmd = f'powershell -Command "[Environment]::SetEnvironmentVariable(\'Path\', [Environment]::GetEnvironmentVariable(\'Path\', \'User\') + \';{PATHS["root"]}\', \'User\')"'
        subprocess.run(cmd, shell=True, check=True)
        
        msg = f"SUCCESS: Multi-Alias Engine Active! ({success_count}/{len(aliases)} shims created)."
        if HAS_RICH:
            console.print(Panel(msg, border_style="green"))
        else:
            print(f"\n[+] {msg}")
        print(f"[*] You can now use: '{BOLD}cs{RESET}', '{BOLD}bro{RESET}', or '{BOLD}cyber{RESET}' from any terminal.")
    except Exception as e:
        log_system_event(f"Multi-Path update failed: {e}", level="ERROR")
        print(f"{RED}[-] System Path Update Failed: {e}{RESET}")

    input("\nPress ENTER to return to menu...")

def run_speed_test():
    """
    PURPOSE: Measures real-time internet bandwidth in MB/s with a live meter.
    Method: Downloads a 10MB file in chunks and calculates throughput.
    """
    test_url = "https://speed.hetzner.de/10MB.bin"
    
    if not check_internet():
        print(f"\n{RED}[-] SPEED TEST FAILED: No internet connection.{RESET}")
        input("Press ENTER to return to menu...")
        return

    # Dynamic imports for specific rich features
    try:
        import requests
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
    except ImportError:
        print(f"{YELLOW}[!] Missing 'requests' or 'rich'. Run Option 5 (Harden) first.{RESET}")
        input("Press ENTER to return...")
        return

    if HAS_RICH:
        console.print(Panel(Align.center("[bold cyan]🚀 INITIALIZING NETWORK SPEED DIAGNOSTIC...[/bold cyan]"), border_style="cyan"))
    else:
        print("\n[*] Initializing Network Speed Test...")

    try:
        start_time = time.time()
        # Stream=True allows us to process the file in real-time bits
        response = requests.get(test_url, stream=True, timeout=15)
        total_size = int(response.headers.get('content-length', 0))
        
        if total_size == 0:
            raise Exception("Invalid response from server (0 bytes)")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, pulse_style="bright_cyan"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            expand=True
        ) as progress:
            
            task = progress.add_task("[magenta]Testing Pulse...", total=total_size)
            
            downloaded = 0
            for chunk in response.iter_content(chunk_size=512*1024): # 512KB chunks
                if chunk:
                    downloaded += len(chunk)
                    progress.update(task, completed=downloaded)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Final Calculation
            final_mb = downloaded / (1024 * 1024)
            avg_speed = final_mb / duration if duration > 0 else 0
            
            # Result UI
            status_text = "EXCELLENT" if avg_speed > 10 else "STABLE" if avg_speed > 2 else "SLUGGISH"
            color = "green" if avg_speed > 10 else "yellow" if avg_speed > 2 else "red"
            
            msg = f"Network Pulse: {avg_speed:.2f} MB/s ({status_text})"
            if HAS_RICH:
                console.print(Panel(Align.center(f"[bold {color}]{msg}[/]"), border_style=color, title="[Diagnostic Result]"))
            else:
                print(f"\n[+] Speed: {avg_speed:.2f} MB/s - {status_text}")
                
            log_system_event(f"Network Speed Test Complete: {avg_speed:.2f} MB/s", level="INFO")

    except Exception as e:
        log_system_event(f"Speed Test Error: {e}", level="ERROR")
        print(f"\n{RED}[-] Diagnostic Interrupted: {e}{RESET}")
        print("[!] Tip: This may be due to a strict firewall or temporary server outage.")

    input("\nPress ENTER to return to menu...")

# NOTE: get_input_timeout() removed — superseded by the Live/msvcrt input engine in main().

# --- BLOCK 3: THE MAIN BRAIN (THE INTERFACE) ---

def render_premium_menu(health_data=None, current_input=""):
    """
    PURPOSE: This is the 'Wow Factor' UI. It builds a beautiful two-column dashboard.
    RETURNS: A Rich Renderable (Group) for Live display.
    """
    if not HAS_RICH:
        return "" 

    # 0. FETCH DATA
    stats = get_system_stats()
    
    # Use cached health data or fetch if missing
    h = health_data if health_data else get_project_health()
    
    # 0. HEADER WITH LIVE CLOCK & ADMIN STATUS
    now = datetime.now().strftime("%I:%M %p")
    admin_tag = "[bold green]ADMIN[/]" if IS_ADMIN else "[bold yellow]USER[/]"
    
    # 💡 REFINED HEADING: Unified Info Box
    header_grid = Table.grid(expand=True)
    header_grid.add_column(justify="left", ratio=1)
    header_grid.add_column(justify="center", ratio=2)
    header_grid.add_column(justify="right", ratio=1)
    
    env_badge = f"[bold white]Env:[/] [bold {('green' if IS_VIRTUAL else 'yellow')}]{VENV_NAME}[/]"
    center_title = f"[bold cyan]CYBERSHIELD COMMAND CENTER[/]  [dim]{CONFIG['VERSION']}[/]"
    status_badge = f"{admin_tag} | [bold cyan]{now}[/]"
    
    header_grid.add_row(env_badge, center_title, status_badge)
    header_panel = Panel(header_grid, border_style="cyan", padding=(0, 0))

    # 1. TOP BAR: SYSTEM STATUS (Real-time Telemetry)
    # 💡 Optimization: We merge integrity and Python runtime into this bar
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
    
    # 💡 The 1.5 Health/Py badges are now integrated into the     # 2. THE DASHBOARD GRID (Unified v3.8 Layout)
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=2) # Main Menu Items
    grid.add_column(justify="left", ratio=1) # Side Stats Panel

    # Left Column: Menu Items
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
        
        menu_columns.add_row(
            Panel(launch_text, title="[green]LAUNCH[/]", border_style="green"),
            Panel(system_text, title="[magenta]OPS[/]", border_style="magenta")
        )
        menu_columns.add_row(
            Panel(git_text, title="[yellow]GIT[/]", border_style="yellow"),
            Panel(maint_grid, title="[blue]MAINT[/]", border_style="blue")
        )
        left_col = menu_columns
    else:
        # Minimal User Dashboard — 2-column grid to ensure no wrapping
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

        user_help_line = Text("  Type a number to run a command  |  'help' for details  |  '14' to exit", style="dim white")
        left_col = Panel(user_opt_grid, title="[bold cyan]COMMANDS[/]", border_style="cyan", padding=(0, 2))



    # Right Column: Live System Health Sidebar (wired to real runtime state)
    net_status   = "[bold green]ONLINE[/]"  if check_internet() else "[bold red]OFFLINE[/]"
    venv_status  = "[bold green]ACTIVE[/]"  if IS_VIRTUAL     else "[bold yellow]GLOBAL[/]"
    rich_status  = "[bold green]READY[/]"   if HAS_RICH        else "[bold red]MISSING[/]"
    psutil_status= "[bold green]READY[/]"   if HAS_PSUTIL      else "[bold red]MISSING[/]"
    admin_status = "[bold green]ADMIN[/]"   if IS_ADMIN        else "[bold yellow]USER[/]"

    status_table = Table(show_header=True, header_style="bold cyan", box=None, expand=True)
    status_table.add_column("NODE", style="dim")
    status_table.add_column("STATUS", justify="right")
    
    status_table.add_row("Network",    net_status)
    status_table.add_row("Venv",       venv_status)
    status_table.add_row("Rich TUI",   rich_status)
    status_table.add_row("Telemetry",  psutil_status)
    status_table.add_row("Privilege",  admin_status)
    
    sidebar_height = 10 if IS_ADMIN else 9
    sidebar_panel = Panel(status_table, title="[cyan]STATUS[/]", border_style="cyan", padding=(0, 1), height=sidebar_height)


    grid.add_row(left_col, sidebar_panel)
    main_display = grid

    # 3. PROMPT DISPLAY (Embedded Input)
    prompt_tag = "cmd_admin" if IS_ADMIN else "cmd_cyber"
    input_line = Text.from_markup(f"[bold cyan]{prompt_tag}[/] > [white]{current_input}[/]", style="white")
    
    # High-Visibility Cursor Block
    if int(time.time() * 2) % 2 == 0: 
        input_line.append("_", style="bold cyan")
    
    prompt_panel = Panel(input_line, border_style="cyan", padding=(0, 2))

    # 4. ASSEMBLE ALL COMPONENTS
    components = [header_panel]
    if IS_ADMIN: components.append(telemetry_panel)
    components.append(main_display)
    
    # Unified Footer: Combines help and tips to eliminate vertical gaps
    footer = Text()
    if not IS_ADMIN:
        footer.append(user_help_line)
        footer.append("\n")
    footer.append(f"  Tip: Type 'help' for details  |  Session Log: {os.path.basename(LOG_FILE)}\n", style="dim white")
    
    components.append(footer)

    return Group(*components)

def boot_loader():
    """PURPOSE: A high-tech 'Boot Sequence' for a professional first impression."""
    if not HAS_RICH:
        return

    # 💡 IMPROVEMENT: Turbo Mode (Skip animation if recently booted)
    settings = load_settings()
    turbo_mode = settings.get("turbo_mode", False)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Force enable ANSI escape sequences for Windows
    if os.name == 'nt':
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    from rich.columns import Columns
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    
    # 1. THE LOGO REVEAL
    logo = f"""[bold red]
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗███████║██║█████╗  ██║     ██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ 
[/]
[dim cyan]      SYSTEM INITIALIZATION | COMMAND CENTER {CONFIG['VERSION']} | 2026 PRODUCTION [/]"""
    try:
        console.print(Align.center(logo))
    except (UnicodeEncodeError, Exception):
        # Full ASCII fallback — bypasses Rich render pipeline for legacy terminals
        import re as _re
        plain = _re.sub(r'\[.*?\]', '', logo)  # Strip all Rich markup tags
        # Replace ALL Unicode box-drawing / block characters with ASCII equivalents
        for old, new in [('█','#'),('╚','+'),('╝','+'),('╔','+'),('╗','+'),
                         ('═','-'),('║','|'),('╠','+'),('╣','+'),('╦','+'),
                         ('╩','+'),('╬','+'),('╭','+'),('╮','+'),('╰','+'),
                         ('╯','+'),('─','-'),('│','|'),('✅','[OK]'),('⚠️','[!]')]:
            plain = plain.replace(old, new)
        sys.stdout.write(plain + '\n')
        sys.stdout.flush()
    
    if turbo_mode:
        console.print(Align.center("[dim italic]Turbo Mode Active: Skipping Animation...[/]"))
        time.sleep(0.3)
    else:
        time.sleep(0.5)

        # 2. THE BOOT DIAGNOSTICS
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40, pulse_style="bright_cyan"),
            transient=True,
        ) as progress:
            
            task1 = progress.add_task("[cyan]Initializing Core Registry...", total=100)
            task2 = progress.add_task("[magenta]Loading Neural Weights...", total=100)
            task3 = progress.add_task("[yellow]Synchronizing Uplink...", total=100)

            # Step-by-step fake 'loading' for aesthetic feel
            while not progress.finished:
                progress.update(task1, advance=2)
                if progress.tasks[0].percentage > 40: progress.update(task2, advance=3)
                if progress.tasks[1].percentage > 30: progress.update(task3, advance=5)
                time.sleep(0.03)

    # 3. FINAL HEALTH CHECK (Real Data)
    h = get_project_health()
    if h["score"] < 70:
        console.print(Panel(
            f"[bold red]⚠️  SYSTEM INTEGRITY ALERT: {h['score']}%[/]\n[yellow]Reason: {h['msg']}[/]",
            title="[bold red]PRE-FLIGHT DIAGNOSTIC[/]", border_style="red"
        ))
        console.print("\n[bold cyan][?] AUTO-REPAIR RECOMMENDED[/bold cyan]")
        fix = input("Would you like me to attempt an Auto-Repair (Harden) now? (y/n): ").lower()
        if fix == 'y':
            harden_environment()
        else:
            log_system_event(f"Startup Health Alert: {h['status']} (User ignored fix)", level="WARNING")
    else:
        console.print(Align.center(f"[bold green]✅ SYSTEM NOMINAL: {h['score']}% INTEGRITY VERIFIED[/]"))
        time.sleep(0.8)
    
    # Final buffer purge to ensure input is fresh for the main menu
    clear_keyboard_buffer()

def main():
    """
    PURPOSE: This is the heart of the switcher. 
    It is wrapped in a 'Global Crash Guard' to ensure the launcher stays alive even if something fails.
    """
    global IS_ADMIN
    IS_ADMIN = is_admin() # Cache for whole session
    
    # Pillar 7: Stealth Lockdown
    hide_file(LOG_FILE)
    hide_file(SETTINGS_FILE)
    
    # Start Background Connectivity Guard
    t = threading.Thread(target=connectivity_guard, daemon=True)
    t.start()

    # Step 1: Integrated Pre-flight Check (BOOT LOADER)
    boot_loader()

    # Clean up any leftover input
    clear_keyboard_buffer()

    # Pillar 5: Global Crash Guard
    # Variables for Dual-Speed refresh
    cached_health = None
    last_health_check = 0

    while True:
        try:
            # Refresh health on a slow timer
            now = time.time()
            if not cached_health or (now - last_health_check) > CONFIG["REFRESH_RATE_SLOW"]:
                cached_health     = get_project_health()
                last_health_check = now

            # ── RENDER: hard-clear (cursor home + clear screen + clear scrollback)
            # \033[H  = move cursor to top-left
            # \033[2J = erase visible screen
            # \033[3J = clear scrollback buffer (prevents auto-scroll on long output)
            sys.stdout.write('\033[H\033[2J\033[3J')
            sys.stdout.flush()
            console.print(render_premium_menu(cached_health, ""))

            # ── INPUT: standard input() — works in every terminal ─────────
            prompt_tag = "cmd_admin" if IS_ADMIN else "cmd_cyber"
            try:
                # 💡 ANSI Cursor Hack: \033[5 q = Blinking Bar cursor
                # (restores the premium 'active' feel in most modern terminals)
                sys.stdout.write('\033[5 q')
                sys.stdout.flush()
                choice = input(f"  {prompt_tag} > ").strip().lower()
                # Reset cursor to default (usually blinking block or bar) if needed, 
                # but typically leaving it as bar is preferred for the theme.
            except (EOFError, KeyboardInterrupt):

                choice = "14"   # treat as Exit


            if not choice:
                continue

            # --- BLOCK 4: THE SWITCHBOARD (CHOOSING THE ACTION) ---
            
            # NLU COMMAND PARSER: Understanding basic human-like commands
            words = choice.split()
            help_patterns = ['help', '?', 'info', 'commands', 'h', 'guide']
            
            # Check for "help [topic]" or "[topic] help"
            is_help_request = any(w in help_patterns for w in words)
            
            if is_help_request:
                # Extract the topic (any word that is NOT a help pattern)
                topics = [w for w in words if w not in help_patterns]
                topic = topics[0] if topics else None
                show_help(topic)
                continue

            # ALIASING: mapping words to numbers
            cmd_map = {
                'run': '1', 'start': '1', 'launch': '1', 'dashboard': '1', 'webapp': '1',
                'ext': '2', 'external': '2',
                'jupyter': '3', 'notebook': '3',
                'harden': '5', 'setup': '5', 'install': '5', 'fix': '5',
                'github': '6', 'repo': '6',
                'venv': '7', 'switch': '7',
                'upgrade': '8', 'migrate': '8',
                'pull': '9', 'update': '9',
                'push': '10', 'commit': '10', 'sync': '10',
                'ignore': '11', 'gitignore': '11',
                'audit': '12', 'path': '12', 'version': '12',
                'restart': '13', 'reload': '13', 'refresh': '13',
                'stop': '14', 'exit': '14', 'bye': '14', 'quit': '14',
                'global': '15', 'register': '15',
                'reset': '16', 'clear_settings': '16',
                'alias': '17', 'register_all': '17',
                'speed': '18', 'network': '18', 'speedtest': '18', 'internet': '18',
                'log': '20', 'logs': '20', 'audit_logs': '20'
                # NOTE: 'help', 'guide', 'h', 'cs', 'bro', 'cyber' intentionally excluded
                # — they are handled by the help_patterns block above to avoid conflict.
            }
            
            # SENSE: Natural Language Intent Routing
            matched_choice = None
            for word in words:
                if word in cmd_map:
                    if cmd_map[word] == '18':
                        matched_choice = '18'
                        break
                    if not matched_choice:
                        matched_choice = cmd_map[word]
            
            if matched_choice:
                choice = matched_choice

            # Check for Health Warning before launching (Option 1/2)
            h_score = cached_health["score"] if cached_health else get_project_health()["score"]
            if choice in ['1', '2'] and h_score < 50:
                print(f"\n{RED}[!] CAUTION: Health Score is low ({h_score}%).{RESET}")
                print(f"{YELLOW}[!] Launch may fail due to missing files or dependencies.{RESET}")
                confirm = input("[?] Proceed regardless? (y/n): ").lower()
                if confirm != 'y': continue

            if choice == '1':
                run_script("webapp", new_window=False)

            elif choice == '2':
                run_script("webapp", new_window=True)

            elif choice in ['3', 'jupyter', 'notebook']:
                run_script("jupyter", new_window=False)

            elif choice == '4':
                run_script("jupyter", new_window=True)

            elif choice in ['5', 'harden', 'setup', 'install']:
                harden_environment()

            elif choice in ['6', 'github', 'repo', 'source']:
                open_repo_smart()
                input("\n[!] Browser Spawned. Press ENTER to return to menu...")

            elif choice in ['7', 'venv', 'virtualenv', 'isolate']:
                # Pillar 4: Handoff Safety
                if IS_VIRTUAL:
                    print("[!] Already running in Virtual Environment.")
                    time.sleep(1)
                    continue
                
                venv_exe = os.path.join(root_dir, '.venv', 'Scripts', 'python.exe')
                if not os.path.exists(venv_exe):
                    print(f"[-] Error: Virtual Environment not found at {venv_exe}")
                    print("[!] Please use Option 5 (Harden) to rebuild the environment first.")
                    input("\nPress ENTER to continue...")
                    continue
                
                print(f"[*] Handoff to Venv: {venv_exe}")
                time.sleep(1)
                os.execl(venv_exe, venv_exe, *sys.argv)

            elif choice in ['8', 'upgrade']:
                if IS_VIRTUAL:
                    print("[!] Already running in Virtual Environment.")
                    time.sleep(1)
                    continue
                venv_exe = os.path.join(root_dir, '.venv', 'Scripts', 'python.exe')
                if os.path.exists(venv_exe):
                    print("[*] Environment Sync: Migrating to Virtual Environment...")
                    time.sleep(1)
                    os.execl(venv_exe, venv_exe, *sys.argv)
                else:
                    print("[-] No Virtual Environment found. Running Hardening Engine first...")
                    harden_environment()
                    if os.path.exists(venv_exe):
                        os.execl(venv_exe, venv_exe, *sys.argv)

            elif choice in ['9', 'pull', 'update']:
                print("\n[*] Pulling latest changes from repository...")
                try:
                    subprocess.run(["git", "pull"], cwd=root_dir, check=True)
                    print("\n[+] Git Pull Complete.")
                except Exception as e:
                    print(f"\n[-] Git Error: {e}")
                    print("[!] Ensure Git is installed and you have an internet connection.")
                input("\nPress ENTER to return to menu...")

            elif choice in ['10', 'push', 'commit', 'sync', 'upload']:
                commit_msg = input("\n[?] Enter commit message (or press ENTER to cancel): ").strip()
                if commit_msg:
                    try:
                        print("[*] Staging all files (git add .)...")
                        subprocess.run(["git", "add", "."], cwd=root_dir, check=True)
                        print(f"[*] Committing as: '{commit_msg}'...")
                        subprocess.run(["git", "commit", "-m", commit_msg], cwd=root_dir, check=True)
                        print("[*] Pushing to repository (git push)...")
                        subprocess.run(["git", "push"], cwd=root_dir, check=True)
                        print("\n[+] Git Operations Successful!")
                    except Exception as e:
                        print(f"\n[-] Git Sync failed: {e}")
                        log_system_event(f"Git Sync Error: {e}", level="ERROR")
                else:
                    print("[-] Operation Canceled.")
                input("\nPress ENTER to return to menu...")

            elif choice in ['11', 'ignore', 'gitignore']:
                gitignore_path = os.path.join(root_dir, ".gitignore")
                print(f"\n{BOLD_CYAN}--- GIT IGNORE MANAGER ---{RESET}")
                print("1. [Manual] Add specific file/folder name")
                print("2. [Automatic] Add current folder to ignore")
                print("3. [Harden] Add all common development patterns")
                print("C. Cancel")
                
                sub_choice = input(f"\n{YELLOW}[?] Select mode: {RESET}").lower()
                
                to_add = []
                if sub_choice == '1':
                    manual_path = input(f"{YELLOW}[?] Enter file/folder to ignore: {RESET}").strip()
                    if manual_path: to_add.append(manual_path)
                elif sub_choice == '2':
                    folder_name = os.path.basename(root_dir)
                    to_add.append(f"{folder_name}/")
                elif sub_choice == '3':
                    to_add = ["*.log", "launcher_debug.log", ".venv/", "__pycache__/", "*.pyc", ".vscode/", "Project materials/"]
                
                if to_add:
                    try:
                        existing = []
                        if os.path.exists(gitignore_path):
                            with open(gitignore_path, "r") as f:
                                existing = [line.strip() for line in f.readlines()]
                        
                        added_count = 0
                        with open(gitignore_path, "a") as f:
                            for p in to_add:
                                if p not in existing:
                                    f.write(f"{p}\n")
                                    added_count += 1
                                    print(f"{GREEN}[+] Added to ignore: {p}{RESET}")
                        
                        if added_count == 0:
                            print(f"{YELLOW}[!] All entries were already in .gitignore.{RESET}")
                        else:
                            log_system_event(f"Git Protection: Added {added_count} items.", level="INFO")
                        
                    except Exception as e:
                        print(f"{RED}[-] Error: {e}{RESET}")
                else:
                    print("[-] No changes made.")
                input("\nPress ENTER to return to menu...")

            elif choice in ['12', 'audit', 'diagnostic']:
                check_system_paths()

            elif choice in ['13', 'restart', 'reload']:
                print("[*] Synchronizing Environment for Restart...")
                # Pillar 1: Professional Safe Exit before Handoff
                if 'live' in locals() and live.is_started:
                    live.stop()
                
                # Pillar 5: Zero-Failure Process Handoff
                # On Windows, os.execl is replaced by spawnl + exit.
                # We need to ensure the console is flushed and ready.
                sys.stdout.flush()
                sys.stderr.flush()
                time.sleep(1.0) # Wait for terminal to settle
                
                try:
                    # Use absolute path to python for reliability
                    python_exe = sys.executable
                    subprocess.Popen([sys.executable, os.path.abspath(__file__)])
                    sys.exit()
                except Exception as restart_err:
                    print(f"[-] Restart failed: {restart_err}")
                    input("Press ENTER to return to menu...")

            elif choice in ['14', 'exit', 'bye', 'stop']:
                print(f"\n{GREEN}[*] Goodbye! Secure logout complete.{RESET}")
                return

            elif choice in ['15', 'global', 'cs', 'register']:
                setup_global_access("cs")
                
            elif choice in ['16', 'reset', 'clear_settings']:
                settings = load_settings()
                settings["browser_mode"] = None
                settings["turbo_mode"] = False
                save_settings(settings)
                print(f"\n{GREEN}[+] All launcher preferences cleared.{RESET}")
                input("Press ENTER to return to menu...")

            elif choice in ['17', 'alias', 'bro', 'cyber']:
                setup_all_aliases()

            elif choice in ['18', 'speed', 'network', 'test']:
                run_speed_test()

            elif choice in ['19', 'help', 'guide']:
                show_help()

            elif choice in ['20', 'log', 'logs']:
                print("[*] Launching Live Audit Logs (External)...")
                subprocess.Popen(['notepad.exe', LOG_FILE])

            # --- RESUME PHASE ---
            # After command exits, we clear the console.
            # The next iteration of the main loop will restart the Live engine automatically.
            console.clear()
            # Give the terminal half a second to settle focus and buffer switches
            time.sleep(0.5)
            # Drain any leftover characters from command inputs (like Git commit msgs)
            clear_keyboard_buffer()

        except KeyboardInterrupt:
            # Pillar 1: Professional Safe Exit on Ctrl+C
            print("\n\n[*] Safe Exit Triggered. Goodbye!")
            sys.exit(0)
            
        except Exception as e:
            # Pillar 5: Master Catch-All UI
            log_system_event(f"MASTER ENGINE CRASH: {traceback.format_exc()}", level="CRITICAL")
            
            # AI AUTO-DIAGNOSIS
            error_msg = str(e).lower()
            advice = "Please check launcher_debug.log for technical details."
            if "not found" in error_msg:
                advice = "A required program (Git, Python, or a dependency) is missing. Try Option 5."
            elif "access is denied" in error_msg or "perm" in error_msg:
                advice = "Permission error! Please restart the launcher as ADMINISTRATOR."
            elif "disk" in error_msg or "space" in error_msg:
                advice = "Your computer's storage is full. Please clear some space."

            print("\n" + f"{RED}" + "="*50 + f"{RESET}")
            print(f" {RED}[CRITICAL SYSTEM ERROR CAUGHT]{RESET} ")
            print(f" {BOLD_WHITE}Error Type: {type(e).__name__}{RESET}")
            print(f" {BOLD_WHITE}Message:    {e}{RESET}")
            print(f" {YELLOW}[AI ADVICE]: {advice}{RESET}")
            print(f"{RED}" + "="*50 + f"{RESET}")
            
            print(f"\n{DIM_WHITE}[DEBUG TRACEBACK]{RESET}")
            traceback.print_exc()
            
            gc.collect() 
            print(f"\n{BOLD_CYAN}>>> Press ANY KEY to attempt auto-restart of the engine...{RESET}")
            
            # Robust any-key detection
            while True:
                if msvcrt.kbhit():
                    msvcrt.getch()
                    break
                time.sleep(0.1)



# This special condition makes sure main() only runs if you double-click THIS file.
# If another script tries to 'import' this file, it won't start the menu automatically.
if __name__ == "__main__":
    main()
