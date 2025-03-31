# smashlets.py
#
# Responsible for discovering, loading, and executing `smashlet_*.py` files.
# Supports multiple smashlets per directory. Each file defines its own transformation logic.

import importlib.util
import sys
import time
import json
from pathlib import Path
from .project import get_runlog, update_runlog

# Constants
ONE_MINUTE = 60  # Default RUN_TIMEOUT for "always" smashlets
RUN_NEVER = 0  # Default last-run timestamp if not yet run


def discover_smashlets(root):
    """
    Discover all smashlet files in the project.

    Supports:
    - smashlet.py
    - smashlet_<name>.py
    Returns a list of all matching files across the project.
    """
    return [
        p
        for p in root.rglob("smashlet*.py")
        if p.name == "smashlet.py" or p.name.startswith("smashlet_")
    ]


def load_smashlet_module(path):
    """
    Dynamically load a smashlet as a Python module.

    Ensures the project root is in sys.path so that smashlets can
    import `smash_helpers` or other root-level modules.

    Returns:
        module or None: Loaded module object, or None if import fails.
    """
    try:
        project_root = path.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        spec = importlib.util.spec_from_file_location(f"smashlet_{path.stem}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        return None


def load_context_data(context_dir):
    """
    Load context files from a directory or context.json file.
    Returns a tuple: (merged_dict, raw_path_dict)
    """
    merged = {}
    paths = {}

    if context_dir.is_file() and context_dir.name.endswith(".json"):
        try:
            merged = json.loads(context_dir.read_text())
            paths[context_dir.name] = context_dir
        except Exception:
            pass
        return merged, paths

    if not context_dir.exists():
        return merged, paths

    if context_dir.is_dir():
        for f in context_dir.iterdir():
            if f.name.startswith(".") or not f.is_file():
                continue

            paths[f.name] = f

            try:
                if f.suffix == ".json":
                    merged[f.stem] = json.loads(f.read_text())
                elif f.suffix in [".yml", ".yaml"]:
                    try:
                        import yaml

                        merged[f.stem] = yaml.safe_load(f.read_text())
                    except ImportError:
                        pass
                elif f.suffix == ".txt":
                    merged[f.stem] = f.read_text()
            except Exception:
                continue

    return merged, paths


def should_run(smashlet_path, project_root):
    """
    Determine if a smashlet should run.

    Based on:
    - RUN mode (default: if_changed)
    - File and input modification timestamps
    - Optional explicit output file tracking
    - Runlog tracking of last successful execution
    - Optional RUN_TIMEOUT for "always" smashlets
    """
    mod = load_smashlet_module(smashlet_path)
    if not mod:
        return False

    run_mode = getattr(mod, "RUN", "if_changed")
    runlog = get_runlog(project_root)
    last_run = runlog.get(str(smashlet_path), RUN_NEVER)

    if run_mode == "always":
        timeout = getattr(mod, "RUN_TIMEOUT", ONE_MINUTE)
        if timeout and (time.time() - last_run < timeout):
            print(f"⏳ Skipping {smashlet_path.name}: RUN_TIMEOUT not reached")
            return False
        return True

    if not hasattr(mod, "run"):
        print(f"⚠️  Skipping {smashlet_path}: no run() function")
        return False

    input_glob = getattr(mod, "INPUT_GLOB", None)
    if not input_glob:
        return False

    input_files = list(smashlet_path.parent.glob(input_glob))

    # --- Optional output tracking ---
    outputs = []
    if hasattr(mod, "get_outputs"):
        outputs = mod.get_outputs()
    elif hasattr(mod, "OUTPUT_FILES"):
        outputs = [Path(p) for p in mod.OUTPUT_FILES]

    if outputs:
        # Rerun if any output is missing
        if any(not out.exists() for out in outputs):
            return True

        latest_output_mtime = max(out.stat().st_mtime for out in outputs)
        latest_input_mtime = max(
            [f.stat().st_mtime for f in input_files] + [smashlet_path.stat().st_mtime]
        )

        return latest_input_mtime > latest_output_mtime

    # Fallback to runlog-based logic
    files_to_check = input_files + [smashlet_path]
    return any(f.stat().st_mtime > last_run for f in files_to_check)


def run_smashlet(path, project_root, base_context):
    """
    Execute a smashlet's run() function, with optional context injection.

    Automatically updates the runlog after successful execution.
    Returns True if the smashlet reports a change (returns 1).
    """
    mod = load_smashlet_module(path)
    if not mod:
        return False

    run_func = getattr(mod, "run", None)
    if not callable(run_func):
        print(f"⚠️  Skipping {path}: run() is not callable")
        return False

    try:
        import inspect

        cwd = path.parent
        context = dict(base_context)
        context["cwd"] = cwd

        # ✅ Auto-inject glob-matched input files
        input_glob = getattr(mod, "INPUT_GLOB", None)
        if input_glob:
            context["inputs"] = list(cwd.glob(input_glob))

        local_ctx_dir = cwd / "context"
        local_ctx_json = cwd / "context.json"

        local_context, local_files = load_context_data(local_ctx_dir)
        if local_ctx_json.exists():
            ctx_json, files_json = load_context_data(local_ctx_json)
            local_context.update(ctx_json)
            local_files.update(files_json)

        context.setdefault("context", {}).update(local_context)
        context.setdefault("context_files", {}).update(local_files)

        sig = inspect.signature(run_func)
        if len(sig.parameters) == 1:
            result = run_func(context)
        else:
            result = run_func()

        update_runlog(project_root, path)
        return result == 1
    except Exception as e:
        print(f"❌ Error in {path}: {e}")
        return False


def touch(path):
    """
    Update the modified timestamp of a file or directory.

    Used to mark a file as changed without modifying contents.
    """
    Path(path).touch(exist_ok=True)
