"""
This file runs all the `smashlet_*.py` files in the project.

It handles finding them, deciding if they need to run (based on inputs, outputs, and timestamps),
and executing their `run()` function with the right context.

Used by the build system. Not part of the public API.
"""

import importlib.util
import sys
import time
from pathlib import Path

from .context_loader import load_context_data
from .project import get_runlog, update_runlog
from .context_loader import build_context
from smash_core.log import log as smash_log

# Constants
ONE_MINUTE = 60  # Default RUN_TIMEOUT for "always" smashlets
RUN_NEVER = 0  # Default last-run timestamp if not yet run


def discover_smashlets(root: Path):
    """
    Discover all smashlet files in the project.

    Supports:
    - smashlet.py
    - smashlet_<name>.py

    Args:
        root (Path): Project root path

    Returns:
        List[Path]: A list of all matching smashlet files across the project
    """
    return [
        p
        for p in root.rglob("smashlet*.py")
        if p.name == "smashlet.py" or p.name.startswith("smashlet_")
    ]


def load_smashlet_module(smashlet_path: Path):
    """
    Dynamically load a smashlet as a Python module.

    Ensures the project root is in sys.path so that smashlets can
    import modules from the root.

    Args:
        smashlet_path (Path): Path to the smashlet file

    Returns:
        module or None: Loaded module object, or None if import fails
    """
    try:
        # Insert the parent of the smashlet's directory (i.e., two levels up)
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
        smash_log(f"Failed to load {smashlet_path}: {e}", "error")

        return None


def should_run(smashlet_path: Path, project_root: Path) -> bool:
    """
    Determine if a smashlet should run, based on:
      - RUN mode (default: 'if_changed')
      - Input file and smashlet modification timestamps
      - Optional explicit output file tracking
      - Runlog timestamp of last execution
      - RUN_TIMEOUT for 'always' smashlets

    Args:
        smashlet_path (Path): Path to the smashlet file
        project_root (Path): Root path of the project

    Returns:
        bool: True if the smashlet should be run, False otherwise
    """
    smashlet_mod = load_smashlet_module(smashlet_path)
    if not smashlet_mod:
        return False

    run_mode = getattr(smashlet_mod, "RUN", "if_changed")
    runlog = get_runlog(project_root)
    last_run = runlog.get(str(smashlet_path), RUN_NEVER)

    # Inject context early if custom should_run exists
    if hasattr(smashlet_mod, "should_run"):
        try:
            context = build_context(project_root)
            input_glob = getattr(smashlet_mod, "INPUT_GLOB", None)
            input_files = (
                list(smashlet_path.parent.glob(input_glob)) if input_glob else []
            )

            # Inject context fields
            context.update(
                {
                    "cwd": smashlet_path.parent,
                    "smashlet_mtime": smashlet_path.stat().st_mtime,
                    "last_run": last_run,
                    "latest_input_mtime": max(
                        [f.stat().st_mtime for f in input_files], default=0
                    ),
                    "inputs": input_files,
                }
            )

            return smashlet_mod.should_run(context)

        except Exception as e:
            smash_log(f"{smashlet_path.name}: using custom should_run()", level="debug")

            smash_log(
                f"Error in should_run() of {smashlet_path.name}: {e}", level="warning"
            )

            return False

    # Handle "RUN = 'always'" with optional RUN_TIMEOUT
    if run_mode == "always":
        timeout = getattr(smashlet_mod, "RUN_TIMEOUT", ONE_MINUTE)
        if timeout and (time.time() - last_run < timeout):
            smash_log(
                f"Skipping {smashlet_path.name}: RUN_TIMEOUT not reached", level="info"
            )

            return False
        return True

    # Must have a run() function
    if not hasattr(smashlet_mod, "run"):
        smash_log(f"Skipping {smashlet_path}: no run() function", level="info")

        return False

    # Must have an INPUT_GLOB
    input_glob = getattr(smashlet_mod, "INPUT_GLOB", None)
    if not input_glob:
        return False

    # Collect input files
    input_files = list(smashlet_path.parent.glob(input_glob))

    # Check for optional output tracking
    outputs = []
    if hasattr(smashlet_mod, "get_outputs"):
        outputs = smashlet_mod.get_outputs()
    elif hasattr(smashlet_mod, "OUTPUT_FILES"):
        outputs = [Path(p) for p in smashlet_mod.OUTPUT_FILES]

    # If outputs are declared, use them to decide if rerun is needed
    if outputs:
        # If any output doesn't exist, we must run
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


def run_smashlet(smashlet_path: Path, project_root: Path, global_context: dict) -> bool:
    """
    Execute a smashlet's run() function, injecting both global and local context.
    Automatically updates the runlog after successful execution.

    Args:
        smashlet_path (Path): Path to the smashlet file
        project_root (Path): Project root path
        global_context (dict): The global (project-level) context to merge with local

    Returns:
        bool: True if the smashlet indicates an output change (returns 1), else False
    """
    smashlet_mod = load_smashlet_module(smashlet_path)
    if not smashlet_mod:
        return False

    run_func = getattr(smashlet_mod, "run", None)
    if not callable(run_func):
        smash_log(f"Skipping {smashlet_path}: run() is not callable", level="info")

        return False

    import inspect

    # The smashlet directory is the parent of the smashlet file
    smashlet_dir = smashlet_path.parent

    # Make a fresh copy of the global context so each smashlet can modify it safely
    context = dict(global_context)

    # Provide the smashlet directory
    context["cwd"] = smashlet_dir  # New standard key
    context["smashlet_dir"] = smashlet_dir  # Backward compatibility

    # Auto-inject glob-matched input files for convenience
    input_glob = getattr(smashlet_mod, "INPUT_GLOB", None)
    if input_glob:
        context["inputs"] = list(smashlet_dir.glob(input_glob))

    # Merge local context from 'context/' folder or 'context.json' in the smashlet dir
    local_context_dir = smashlet_dir / "context"
    local_context_json = smashlet_dir / "context.json"

    # Load the directory-based local context
    loaded_local_context, loaded_local_files = load_context_data(local_context_dir)

    # If there's a separate context.json, load that too and merge
    if local_context_json.exists():
        json_context, json_files = load_context_data(local_context_json)
        loaded_local_context.update(json_context)
        loaded_local_files.update(json_files)

    # Ensure 'context' and 'context_files' exist in the final dict
    context.setdefault("context", {}).update(loaded_local_context)
    context.setdefault("context_files", {}).update(loaded_local_files)

    try:
        sig = inspect.signature(run_func)
        # If run(context) is expected
        if len(sig.parameters) == 1:
            result = run_func(context)
        else:
            # Otherwise run() with no args
            result = run_func()

        # Mark it as run in the runlog
        update_runlog(project_root, smashlet_path)

        return result == 1

    except Exception as e:
        smash_log(f"Error in {smashlet_path}: {e}", level="error")

        return False


def touch(path: Path):
    """
    Update the modified timestamp of a file or directory.
    Used to mark a file as changed without modifying contents.

    Args:
        path (Path): The file or directory to 'touch'
    """
    path.touch(exist_ok=True)
