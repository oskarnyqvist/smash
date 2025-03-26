import json
import time
from pathlib import Path


def find_project_root():
    p = Path.cwd()
    while p != p.parent:
        if (p / ".smash").is_dir():
            return p
        p = p.parent
    return None


def get_runlog(project_root):
    path = project_root / ".smash" / "runlog.json"
    if path.exists():
        return json.loads(path.read_text())
    return {}


def update_runlog(project_root, smashlet_path):
    runlog = get_runlog(project_root)
    runlog[str(smashlet_path)] = int(time.time())
    (project_root / ".smash" / "runlog.json").write_text(json.dumps(runlog, indent=2))
