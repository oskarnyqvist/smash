# smash_core/log.py

"""
Standard logging utility used across Smash and in smashlets.

Adds consistent emoji prefixes for log levels like info, warn, error, and debug.
Part of the public smashlet API via `from smash import log`.
"""

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
