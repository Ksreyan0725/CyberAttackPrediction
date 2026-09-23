import os
import sys

# --- BLOCK 0.5: PREMIUM UI DETECTION ---
try:
    from rich.console import Console
    import io
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

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_version():
    """Extracts version from the launcher.py header docstring dynamically."""
    try:
        launcher_path = os.path.join(root_dir, "launcher.py")
        with open(launcher_path, "r", encoding="utf-8") as f:
            for line in f:
                if "VERSION:" in line:
                    parts = line.split("VERSION:")[1].split("(")
                    return "v" + parts[0].strip()
    except Exception:
        pass
    return "v2.8.0"

CONFIG = {
    "PROJECT_NAME": "CyberAttackPrediction",
    "REPO_URL": "https://github.com/Ksreyan0725/CyberAttackPrediction---College_Project",
    "VERSION": get_version(),
    "REFRESH_RATE_FAST": 2.0,  
    "REFRESH_RATE_SLOW": 10.0, 
    "COMMAND_NAME": "cs",
    "VENV_DIR": ".venv",
    "FAST_BOOT": False
}

IS_VIRTUAL = sys.prefix != sys.base_prefix or 'VIRTUAL_ENV' in os.environ
IS_ADMIN = False
_INTERNET_STATUS = True

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
LOG_FILE = PATHS["log"]
SETTINGS_FILE = PATHS["settings"]

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
