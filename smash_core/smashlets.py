# smashlets.py
#
# Responsible for discovering, loading, and executing `smashlet_*.py` files.
# Supports multiple smashlets per directory. Each file defines its own transformation logic.

import importlib.util
import sys
import time
from pathlib import Path
import inspect

from smash_core.log import log
from .context_loader import load_context_data
from .project import get_runlog, update_runlog

ONE_MINUTE = 60
RUN_NEVER = 0


def discover_smashlets(root: Path):
    return [
        p
        for p in root.rglob("smashlet*.py")
        if p.name == "smashlet.py" or p.name.startswith("smashlet_")
    ]


def load_smashlet_module(smashlet_path: Path):
    try:
        project_root_candidate = smashlet_path.parent.parent
        if str(project_root_candidate) not in sys.path:
            sys.path.insert(0, str(project_root_candidate))

        spec = importlib.util.spec_from_file_location(
            f"smashlet_{smashlet_path.stem}", smashlet_path
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    except Exception as e:
        log(f"❌ Failed to load {smashlet_path}: {e}", level="error")
        return None


def should_run(smashlet_path: Path, project_root: Path) -> bool:
    smashlet_mod = load_smashlet_module(smashlet_path)
    if not smashlet_mod:
        return False

    run_mode = getattr(smashlet_mod, "RUN", "if_changed")
    runlog = get_runlog(project_root)
    last_run = runlog.get(str(smashlet_path), RUN_NEVER)

    if run_mode == "always":
        timeout = getattr(smashlet_mod, "RUN_TIMEOUT", ONE_MINUTE)
        if timeout and (time.time() - last_run < timeout):
            log(f"⏳ Skipping {smashlet_path.name}: RUN_TIMEOUT not reached")
            return False
        return True

    if not hasattr(smashlet_mod, "run"):
        log(f"⚠️  Skipping {smashlet_path}: no run() function", level="warn")
        return False

    input_glob = getattr(smashlet_mod, "INPUT_GLOB", None)
    if not input_glob:
        return False

    input_files = list(smashlet_path.parent.glob(input_glob))

    outputs = []
    if hasattr(smashlet_mod, "get_outputs"):
        outputs = smashlet_mod.get_outputs()
    elif hasattr(smashlet_mod, "OUTPUT_FILES"):
        outputs = [Path(p) for p in smashlet_mod.OUTPUT_FILES]

    if outputs:
        if any(not out.exists() for out in outputs):
            return True

        latest_output_mtime = max(out.stat().st_mtime for out in outputs)
        latest_input_mtime = max(
            [f.stat().st_mtime for f in input_files] + [smashlet_path.stat().st_mtime]
        )
        return latest_input_mtime > latest_output_mtime

    files_to_check = input_files + [smashlet_path]
    return any(f.stat().st_mtime > last_run for f in files_to_check)


def run_smashlet(smashlet_path: Path, project_root: Path, global_context: dict) -> bool:
    smashlet_mod = load_smashlet_module(smashlet_path)
    if not smashlet_mod:
        return False

    run_func = getattr(smashlet_mod, "run", None)
    if not callable(run_func):
        log(f"⚠️  Skipping {smashlet_path}: run() is not callable", level="warn")
        return False

    smashlet_dir = smashlet_path.parent
    context = dict(global_context)
    context["smashlet_dir"] = smashlet_dir

    input_glob = getattr(smashlet_mod, "INPUT_GLOB", None)
    if input_glob:
        context["inputs"] = list(smashlet_dir.glob(input_glob))

    local_context_dir = smashlet_dir / "context"
    local_context_json = smashlet_dir / "context.json"

    loaded_local_context, loaded_local_files = load_context_data(local_context_dir)

    if local_context_json.exists():
        json_context, json_files = load_context_data(local_context_json)
        loaded_local_context.update(json_context)
        loaded_local_files.update(json_files)

    context.setdefault("context", {}).update(loaded_local_context)
    context.setdefault("context_files", {}).update(loaded_local_files)

    try:
        sig = inspect.signature(run_func)
        result = run_func(context) if len(sig.parameters) == 1 else run_func()
        update_runlog(project_root, smashlet_path)
        return result == 1

    except Exception as e:
        log(f"❌ Error in {smashlet_path}: {e}", level="error")
        return False


def touch(path: Path):
    path.touch(exist_ok=True)
