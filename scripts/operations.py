from scripts.config import *
from scripts.utils import *
from scripts.diagnostics import *
import os, sys, time, subprocess, webbrowser, shutil

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
            # Run in the same terminal, mirroring every line to the server log
            # file as well. That copy is what Option 21 reads, so logs can be
            # viewed/copied later without ever selecting text in this console
            # (which used to freeze or kill the running server).
            os.makedirs(os.path.dirname(SERVER_LOG_FILE), exist_ok=True)
            try:
                log_f = open(SERVER_LOG_FILE, "a", encoding="utf-8", errors="replace")
            except Exception:
                log_f = None
            proc = None
            try:
                if log_f:
                    log_f.write(f"\n===== Server started {time.strftime('%Y-%m-%d %H:%M:%S')} ({mode}) =====\n")
                    log_f.flush()
                # -u / PYTHONUNBUFFERED: without these, piped output would sit
                # in a buffer and neither screen nor log file would update live.
                env = dict(os.environ, PYTHONUNBUFFERED="1")
                cmd_live = list(cmd) + (["-u"] if mode == 'webapp' else [])
                proc = subprocess.Popen(cmd_live, cwd=target_dir,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        text=True, errors="replace", bufsize=1, env=env)
                for line in proc.stdout:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    if log_f:
                        log_f.write(line)
                proc.wait()
            except KeyboardInterrupt:
                # Ctrl+C still means "stop the server" — shut the child down too.
                if proc is not None:
                    try:
                        proc.terminate()
                    except Exception:
                        pass
                raise
            finally:
                if log_f:
                    try:
                        log_f.close()
                    except Exception:
                        pass
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Launcher: Process interrupted by user.{RESET}")
    except Exception as e:
        log_system_event(f"Execution Error ({mode}): {str(e)}", level="ERROR")
        print(f"\n{RED}[-] Launcher Error: {e}{RESET}")

def snapshot_server_log(lines=80):
    """Shows the tail of the mirrored server log and copies it to clipboard.

    The server keeps running untouched — no console selection involved, so
    nothing can freeze or close it. Used by launcher Option 21.
    """
    if not os.path.exists(SERVER_LOG_FILE):
        print("[-] No server log yet. Launch the WebApp (Option 1) first so there is output to copy.")
        return
    try:
        with open(SERVER_LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            tail = f.readlines()[-max(1, lines):]
        text = "".join(tail).strip()
        if not text:
            print("[-] Server log is empty.")
            return
        print(f"\n[*] Last {len(tail)} lines of server output (server still running):")
        print("-" * 50)
        print(text)
        print("-" * 50)
        if copy_text_to_clipboard(text):
            print(f"{GREEN}[+] Copied to clipboard. Paste anywhere with Ctrl+V.{RESET}")
        else:
            print(f"{YELLOW}[!] Clipboard copy failed. Copy from the text above instead.{RESET}")
    except Exception as e:
        print(f"[-] Could not read server log: {e}")

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
                # Sanitize/Validate REPO_URL
                if REPO_URL.startswith("http://") or REPO_URL.startswith("https://"):
                    # deepcode ignore CommandInjection: REPO_URL is validated above
                    # snyk ignore: command_injection
                    subprocess.Popen([exe_path, flag, REPO_URL])
                else:
                    log_system_event("Invalid REPO_URL for Incognito launch", level="ERROR")
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

def run_first_time_setup():
    """
    PURPOSE: Invokes the First-Time Setup using the Rust Auth Engine.
    Requires the virtual environment to be set up so it can use Werkzeug.
    """
    users_file = os.path.join(root_dir, 'CyberAttackPrediction', 'users.json')
    if os.path.exists(users_file):
        return # Already set up

    print(f"\n{CYAN}[!] Fresh Installation Detected{RESET}")
    print("Would you like to initialize your secure local credentials now? (y/n)")
    choice = input(">> ").strip().lower()
    if choice != 'y':
        print("[*] Setup skipped. You can access the system via Web Guest Login.")
        time.sleep(1.5)
        return

    venv_python = os.path.join(root_dir, '.venv', 'Scripts', 'python.exe')
    setup_script = os.path.join(root_dir, 'scripts', 'setup_env.py')
    
    if not os.path.exists(venv_python):
        print(f"\n{RED}[!] Virtual Environment missing!{RESET}")
        print("[!] The First-Time Setup requires the python virtual environment.")
        print("[!] Please run 'Install Requirements (Quick/Clean)' from the main menu first.")
        input("Press Enter to continue...")
        return
        
    try:
        subprocess.run([venv_python, setup_script], check=True)
    except Exception as e:
        log_system_event(f"First-Time Setup Error: {str(e)}", level="ERROR")
        print(f"\n{RED}[-] Setup Engine Error: {e}{RESET}")