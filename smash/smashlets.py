import importlib.util
import time
from pathlib import Path
from .project import get_runlog, update_runlog

ONE_MINUTE = 60
RUN_NEVER = 0


def discover_smashlets(root):
    return [p for p in root.rglob("smashlet.py")]


def load_smashlet_module(path):
    try:
        spec = importlib.util.spec_from_file_location("smashlet", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        return None


def should_run(smashlet_path, project_root):
    mod = load_smashlet_module(smashlet_path)
    if not mod:
        return False

    run_mode = getattr(mod, "RUN", "if_changed")

    if run_mode == "always":
        runlog = get_runlog(project_root)
        last_run = runlog.get(str(smashlet_path), RUN_NEVER)
        timeout = getattr(mod, "RUN_TIMEOUT", ONE_MINUTE)

        if timeout and (time.time() - last_run < timeout):
            print(f"⏳ Skipping {smashlet_path.name}: RUN_TIMEOUT not reached")
            return False

        return True

    # Default behavior (INPUT_GLOB comparison)
    if not hasattr(mod, "run"):
        print(f"⚠️  Skipping {smashlet_path}: no run() function")
        return False

    input_glob = getattr(mod, "INPUT_GLOB", None)
    if not input_glob:
        return False

    input_files = list(smashlet_path.parent.glob(input_glob))
    smashlet_mtime = smashlet_path.stat().st_mtime

    return any(f.stat().st_mtime > smashlet_mtime for f in input_files)


def run_smashlet(path, project_root):
    mod = load_smashlet_module(path)
    if not mod:
        return False

    run_func = getattr(mod, "run", None)
    if not callable(run_func):
        print(f"⚠️  Skipping {path}: run() is not callable")
        return False

    try:
        result = run_func()
        update_runlog(project_root, path)
        return result == 1
    except Exception as e:
        print(f"❌ Error in {path}: {e}")
        return False


def touch(path):
    Path(path).touch(exist_ok=True)
