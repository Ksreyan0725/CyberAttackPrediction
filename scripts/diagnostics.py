from scripts.config import *
from scripts.utils import *
import os, sys, time, importlib
if HAS_PSUTIL:
    import psutil

def connectivity_guard():
    """PURPOSE: A background thread that checks internet health without lag."""
    import scripts.config as cfg
    import socket
    while True:
        try:
            # Pinging Google DNS (Fastest check)
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            cfg._INTERNET_STATUS = True
        except (OSError, socket.timeout):
            cfg._INTERNET_STATUS = False
        time.sleep(30) # Only check every 30s to save CPU/Battery

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