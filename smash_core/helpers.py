# smash_core/helpers.py

"""
Reusable helper functions for writing smashlets.

Includes logging, directory setup, safe writes, and batch file reading.
Exposed to users via the public `smash` API.
"""

import hashlib
from pathlib import Path

from smash_core.files import resolve


def get_digest(content):
    return hashlib.sha1(content.encode("utf-8")).hexdigest()


def read_text_files(paths):
    """
    Read a list of file paths and return their contents as strings.
    """
    return [Path(p).read_text() for p in paths]


def write_output(path, content):
    """
    Write string content to a file, creating parent directories if needed.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def smash_log(msg):
    """
    Standardized log output for use in smashlets.
    """
    print(f"[smash] {msg}")


def ensure_dir(path):
    """
    Ensure a directory exists (like mkdir -p).
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def flatten_json_dir(path):
    """
    Load and flatten all JSON files in a directory into a list of dicts.
    Ignores non-.json files. Returns list of parsed objects.
    """
    import json

    result = []
    for file in Path(path).glob("*.json"):
        try:
            data = json.loads(file.read_text())
            result.append(data)
        except Exception:
            pass
    return result


def write_output_if_changed(path, content, context):
    """
    Writes `content` to the resolved path only if it differs from what's already there.
    Returns True if a write occurred (content changed), else False.
    """
    out_path = path if isinstance(path, Path) else resolve(path, context)
    old = out_path.read_text() if out_path.exists() else ""

    if content != old:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        return True

    return False
