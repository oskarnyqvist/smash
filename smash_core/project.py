# smash_core/project.py

"""
Manages project-level state, including project root detection and runlog persistence.

- Locates the Smash project root (identified by a `.smash/` directory)
- Reads and writes `.smash/runlog.json` with structured per-smashlet metadata

Note: This module is internal and not part of the public Smash API.
"""

import json
import time
from pathlib import Path

from smash_core.log import log


def find_project_root():
    """
    Walks upward from the current directory to find the Smash project root.

    A valid root contains a `.smash/` directory. Returns None if not found.
    """
    p = Path.cwd()
    while p != p.parent:
        if (p / ".smash").is_dir():
            return p
        p = p.parent
    return None


def get_runlog(project_root):
    """
    Loads and normalizes the `.smash/runlog.json` file.

    Filters out legacy or malformed entries. Keeps at most 10 recent runs per smashlet.
    Returns a dict keyed by smashlet path with structured run metadata.
    """
    path = project_root / ".smash" / "runlog.json"
    if not path.exists():
        return {}

    try:
        raw = json.loads(path.read_text())
    except Exception as e:
        log(f"Failed to read runlog.json: {e}", level="error")
        return {}

    runlog = {}

    for key, value in raw.items():
        if not isinstance(value, dict):
            log(f"Ignoring legacy runlog entry: {key}", level="debug")
            continue

        if "last_run" not in value:
            log(
                f"Ignoring malformed runlog entry (missing last_run): {key}",
                level="debug",
            )
            continue

        history = value.get("history", [])
        if not isinstance(history, list):
            history = []

        normalized = []
        for h in history:
            if isinstance(h, dict) and "finished_on" in h:
                normalized.append(h)

        runlog[key] = {
            "last_run": value["last_run"],
            "runs": value.get("runs", len(normalized)),
            "history": normalized[-10:],
        }

    return runlog


def update_runlog(project_root, smashlet_path, finished_on=None, duration=None):
    """
    Updates the runlog with a new completed run for the given smashlet.

    Appends a history entry and bumps the run count. Truncates to the 10 most recent runs.
    Writes the updated `.smash/
    """
    runlog = get_runlog(project_root)
    key = str(smashlet_path)
    now = int(finished_on or time.time())

    history_entry = {"finished_on": now}
    if duration is not None:
        history_entry["duration"] = duration

    entry = runlog.get(key)

    if isinstance(entry, dict):
        entry["last_run"] = now
        entry["runs"] = entry.get("runs", 0) + 1
        history = entry.get("history", [])
        history.append(history_entry)
        entry["history"] = history[-10:]
    else:
        runlog[key] = {"last_run": now, "runs": 1, "history": [history_entry]}

    runlog_path = project_root / ".smash" / "runlog.json"
    runlog_path.write_text(json.dumps(runlog, indent=2))
