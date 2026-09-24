from scripts.config import *
import os, sys, time, json, socket, msvcrt, ctypes, subprocess
from datetime import datetime
from scripts.logger import log_system_event, get_logger

def disable_quickedit():
    if os.name != 'nt':
        return
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-10)
        mode = ctypes.c_uint32()
        result = kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        if result:
            kernel32.SetConsoleMode(handle, mode.value & ~0x0040)
    except Exception:
        pass

def copy_text_to_clipboard(text):
    if os.name != 'nt':
        return False
    try:
        proc = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE)
        proc.communicate(text.encode('utf-8', errors='replace'))
        return proc.returncode == 0
    except Exception:
        return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def hide_file(path):
    if os.name == 'nt' and os.path.exists(path):
        try:
            ctypes.windll.kernel32.SetFileAttributesW(path, 2)
        except Exception:
            pass

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        hide_file(SETTINGS_FILE)
    except Exception as e:
        log_system_event(f'Failed to save settings: {e}', level='ERROR')

def clear_keyboard_buffer():
    while msvcrt.kbhit():
        try:
            msvcrt.getch()
        except:
            pass

def check_internet():
    import scripts.config as cfg
    return cfg._INTERNET_STATUS