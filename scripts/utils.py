from scripts.config import *
import os, sys, time, json, socket, msvcrt, ctypes, logging

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

def clear_keyboard_buffer():
    while msvcrt.kbhit():
        try:
            msvcrt.getch()
        except:
            pass

def check_internet():
    """PURPOSE: Returns the cached internet status from the background guard."""
    import scripts.config as cfg
    return cfg._INTERNET_STATUS