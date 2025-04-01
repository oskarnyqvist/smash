# smash_core/files.py
#
# Path-safe helpers for reading, writing, and resolving files using context["cwd"]

from pathlib import Path


def resolve(relative_path, context):
    """
    Resolve a file path relative to the smashlet's directory.

    Uses context["cwd"], with fallback to context["smashlet_dir"].
    """
    cwd = context.get("cwd") or context.get("smashlet_dir")
    if not cwd:
        raise ValueError("Context missing 'cwd' or 'smashlet_dir'")
    return Path(cwd) / relative_path


def read(relative_path, context):
    """
    Read a file's contents relative to the smashlet directory.
    """
    return resolve(relative_path, context).read_text()


def write(relative_path, data, context):
    """
    Write a string to a file relative to the smashlet directory.
    """
    path = resolve(relative_path, context)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
