# utils/logger.py

from datetime import datetime

def log(message: str, level: str = "INFO") -> None:
    """
    Simple logger with timestamps and levels.

    Args:
        message (str): Message to log.
        level (str): Log level (INFO, ERROR, DEBUG).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{level}] {timestamp} | {message}")
