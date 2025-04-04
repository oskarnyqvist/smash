# init.py

"""
Handles the `smash init` command by creating a new `.smash/` directory.

Used by the public CLI to initialize a Smash project. Not part of the importable API.
"""

from pathlib import Path
from smash_core.log import log


def run_init():
    """
    Initialize a new Smash project by creating a .smash/ directory.

    If the directory already exists, informs the user without modifying it.
    """
    project_root = Path.cwd()
    smash_dir = project_root / ".smash"

    if smash_dir.exists():
        log("✅ Project already initialized.")
        return

    try:
        smash_dir.mkdir()
        log("✅ Initialized new Smash project.")
    except Exception as e:
        log(f"❌ Failed to create .smash/: {e}", level="error")
