"""
CyberShield AI — Unified Logging Component
Reusable logging component for launcher and Flask app.
Logs to logs/ folder with rotation, structured formatting, and multiple handlers.
"""
import os
import sys
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path

# ─── Configuration ───
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LAUNCHER_LOG_FILE = LOG_DIR / "launcher.log"
SERVER_LOG_FILE = LOG_DIR / "server.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"

MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

# ─── Formatters ───
class ColoredFormatter(logging.Formatter):
    """Formatter with optional color codes for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def __init__(self, fmt=None, datefmt=None, use_color=True):
        super().__init__(fmt, datefmt)
        self.use_color = use_color
    
    def format(self, record):
        if self.use_color and record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            record.msg = f"{self.COLORS.get(record.levelname, '')}{record.msg}{self.RESET}"
        return super().format(record)


# ─── Logger Factory ───
class LoggerFactory:
    """Creates and configures loggers with consistent formatting."""
    
    _loggers = {}
    _initialized = False
    
    @classmethod
    def _setup_root_logger(cls):
        """Configure root logger with file and console handlers."""
        if cls._initialized:
            return
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Console handler (colored)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(ColoredFormatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
            use_color=True
        ))
        root_logger.addHandler(console_handler)
        
        # Main rotating file handler
        main_handler = logging.handlers.RotatingFileHandler(
            LAUNCHER_LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        main_handler.setLevel(logging.DEBUG)
        main_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        root_logger.addHandler(main_handler)
        
        # Error-only file handler
        error_handler = logging.handlers.RotatingFileHandler(
            ERROR_LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        root_logger.addHandler(error_handler)
        
        cls._initialized = True
    
    @classmethod
    def get_logger(cls, name: str = "cybershield") -> logging.Logger:
        """Get a configured logger instance."""
        if not cls._initialized:
            cls._setup_root_logger()
        return logging.getLogger(name)
    
    @classmethod
    def get_launcher_logger(cls) -> logging.Logger:
        """Get logger specifically for launcher operations."""
        return cls.get_logger("cybershield.launcher")
    
    @classmethod
    def get_server_logger(cls) -> logging.Logger:
        """Get logger specifically for server operations."""
        return cls.get_logger("cybershield.server")
    
    @classmethod
    def get_error_logger(cls) -> logging.Logger:
        """Get logger for error tracking."""
        return cls.get_logger("cybershield.error")


# ─── Convenience Functions ───
def get_logger(name: str = "cybershield") -> logging.Logger:
    """Get a logger instance. Main entry point."""
    return LoggerFactory.get_logger(name)


def log_launcher_start(version: str = ""):
    """Log launcher startup with version info."""
    logger = LoggerFactory.get_launcher_logger()
    logger.info(f"{'='*60}")
    logger.info(f"CyberShield AI Launcher Starting {version}")
    logger.info(f"{'='*60}")
    logger.info(f"Working Directory: {Path.cwd()}")
    logger.info(f"Python: {sys.version.split()[0]}")
    logger.info(f"Platform: {sys.platform}")


def log_launcher_stop():
    """Log launcher shutdown."""
    logger = LoggerFactory.get_launcher_logger()
    logger.info("Launcher stopped gracefully")


def log_critical_error(error: Exception, context: str = ""):
    """Log critical errors with full traceback."""
    logger = LoggerFactory.get_error_logger()
    logger.critical(f"{context}: {error}", exc_info=True)


# Backward compatibility with existing log_system_event
def log_system_event(message: str, level: str = "INFO"):
    """
    Backward compatible function for existing launcher code.
    Maps to new structured logging system.
    """
    logger = LoggerFactory.get_launcher_logger()
    level_num = getattr(logging, level.upper(), logging.INFO)
    logger.log(level_num, message)


# Initialize on import
LoggerFactory._setup_root_logger()

# Export commonly used items
__all__ = [
    'get_logger',
    'get_launcher_logger',
    'get_server_logger', 
    'get_error_logger',
    'log_system_event',
    'log_launcher_start',
    'log_launcher_stop',
    'log_critical_error',
]