# log.py
#
# Provides a consistent logging function used across Smash.
# Supports future extensions like timestamps, log levels, or formatting.

LEVEL_PREFIX = {
    "info": "ℹ️ ",
    "warn": "⚠️ ",
    "error": "❌",
    "debug": "🐛",
}


def log(msg: str, *, level="info"):
    """
    Log a message with a standard prefix.

    Args:
        msg (str): The message to print
        level (str): Optional level: "info", "warn", "error", "debug"
    """
    prefix = LEVEL_PREFIX.get(level, "")
    print(f"{prefix} {msg}")
