# smash_core/helpers.py
#
# Built-in utility functions for smashlets.
# These are exposed via `from smash.helpers import ...`

from pathlib import Path


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
