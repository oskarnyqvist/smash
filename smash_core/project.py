"""
project.py

Handles project-level state and metadata.
Includes logic for locating the project root and managing the runlog.
"""

import json
import time
from pathlib import Path


def find_project_root():
    """
    Locate the root of the Smash project by walking upward from the current directory.

    A project is identified by the presence of a `.smash/` directory.
    Returns None if no root is found.
    """
    p = Path.cwd()
    while p != p.parent:
        if (p / ".smash").is_dir():
            return p
        p = p.parent
    return None


def get_runlog(project_root):
    """
    Read the runlog from `.smash/runlog.json`.

    The runlog tracks when each smashlet was last executed.
    Returns an empty dict if no runlog file exists.
    """
    path = project_root / ".smash" / "runlog.json"
    if path.exists():
        return json.loads(path.read_text())
    return {}


def update_runlog(project_root, smashlet_path):
    """
    Record the current timestamp for a successfully executed smashlet.

    Called after `run()` completes. Writes back to `.smash/runlog.json`.
    """
    runlog = get_runlog(project_root)
    runlog[str(smashlet_path)] = int(time.time())

    runlog_path = project_root / ".smash" / "runlog.json"
    runlog_path.write_text(json.dumps(runlog, indent=2))
