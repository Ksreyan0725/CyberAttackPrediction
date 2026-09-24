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
import os, sys, time, threading, traceback, gc, subprocess, json, msvcrt

from scripts.config import *
from scripts.utils import *
from scripts.diagnostics import *
from scripts.operations import *
from scripts.launcher_ui import render_premium_menu, boot_loader, show_help

def main():
    """
    PURPOSE: This is the heart of the switcher. 
    It is wrapped in a 'Global Crash Guard' to ensure the launcher stays alive even if something fails.
    """
    global IS_ADMIN
    IS_ADMIN = is_admin() # Cache for whole session

    # Selecting text in the console used to freeze/kill the running server
    # (Windows QuickEdit pause). Turn that off once at startup.
    disable_quickedit()
    
    # Pillar 7: Stealth Lockdown
    hide_file(LOG_FILE)
    hide_file(SETTINGS_FILE)
    
    # Start Background Connectivity Guard
    t = threading.Thread(target=connectivity_guard, daemon=True)
    t.start()

    # Step 1: Integrated Pre-flight Check (BOOT LOADER)
    boot_context = {
        "FAST_BOOT": CONFIG.get("FAST_BOOT", False),
        "health_data": get_project_health()
    }
    action = boot_loader(boot_context)
    if action == "harden":
        harden_environment()
    elif action == "ignore":
        log_system_event("Startup Health Alert (User ignored fix)", level="WARNING")

    # Step 1.5: First-Time Secure Credentials Setup (Rust Engine)
    run_first_time_setup()

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
            ui_context = {
                "stats": get_system_stats(),
                "health_data": cached_health,
                "IS_ADMIN": IS_ADMIN,
                "IS_VIRTUAL": IS_VIRTUAL,
                "VENV_NAME": VENV_NAME,
                "VERSION": CONFIG["VERSION"],
                "LOG_FILE": LOG_FILE,
                "HAS_PSUTIL": HAS_PSUTIL,
                "net_online": check_internet()
            }
            console.print(render_premium_menu(ui_context, ""))

            # ── INPUT: standard input() — works in every terminal ─────────
            prompt_tag = "cmd_admin" if IS_ADMIN else "cmd_cyber"
            try:
                # 💡 ANSI Cursor Hack: \033[5 q = Blinking Bar cursor
                # (restores the premium 'active' feel in most modern terminals)
                sys.stdout.write('\033[5 q')
                sys.stdout.flush()
                # Ensure any leftover input is cleared before reading
                clear_keyboard_buffer()
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
                'log': '20', 'logs': '20', 'audit_logs': '20',
                'copy': '21', 'snapshot': '21', 'serverlog': '21', 'serverlogs': '21',
                'orbit': '22', 'orbitai': '22', 'ai': '22'
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
                clear_keyboard_buffer()
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
                clear_keyboard_buffer()
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
                
                clear_keyboard_buffer()
                sub_choice = input(f"\n{YELLOW}[?] Select mode: {RESET}").lower()
                
                to_add = []
                if sub_choice == '1':
                    clear_keyboard_buffer()
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

            elif choice in ['21', 'copy', 'snapshot', 'serverlog']:
                # Copy server output WITHOUT touching the running server:
                # reads the mirrored log file, prints it, copies to clipboard.
                clear_keyboard_buffer()
                lines_in = input("\n[?] How many last lines? (ENTER = 80): ").strip()
                try:
                    n = int(lines_in) if lines_in else 80
                except ValueError:
                    n = 80
                snapshot_server_log(lines=n)
                input("\nPress ENTER to return to menu...")

            elif choice in ['22', 'orbit', 'orbitai', 'ai']:
                # Orbit AI: UI menu lives launcher-side (scripts/orbit_ui.py);
                # all engine work goes through the nodes middleware.
                try:
                    from scripts.orbit_ui import run_orbit_menu
                    run_orbit_menu()
                except KeyboardInterrupt:
                    print(f"\n{YELLOW}[!] Orbit AI interrupted. Back to menu.{RESET}")
                except Exception as e:
                    print(f"\n{RED}[-] Orbit AI failed to start: {e}{RESET}")
                    log_system_event(f"Orbit AI launch error: {e}", level="ERROR")
                input("\nPress ENTER to return to menu...")

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

if __name__ == "__main__":
    main()
