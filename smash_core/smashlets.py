# smash_core/smashlets.py

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
    Finds all valid smashlet files in the project.

    Matches files like `smashlet.py` and `smashlet_<name>.py` under the given root.
    """

    return [
        p
        for p in root.rglob("smashlet*.py")
        if p.name == "smashlet.py" or p.name.startswith("smashlet_")
    ]


def load_smashlet_module(smashlet_path: Path):
    """
    Dynamically loads a smashlet module so it can be executed.

    Ensures the project root is added to `sys.path` so imports work as expected.
    Returns the loaded module or None if loading fails.
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


SMASHLET_CONSTANT_DEFAULTS = [
    {
        "name": "RUN",
        "default": "if_changed",
        "allowed": ["if_changed", "always"],
    },
    {
        "name": "RUN_TIMEOUT",
        "default": 60,
        "allowed": [],
    },
    {
        "name": "INPUT_GLOB",
        "default": None,
        "allowed": [],
    },
    {
        "name": "OUTPUT_FILES",
        "default": [],
        "allowed": [],
    },
]

SMASHLET_REQUIRED_FUNCTIONS = [
    {"name": "run", "required": True},
    {"name": "should_run", "required": False},
    {"name": "get_outputs", "required": False},
]


def should_run(smashlet_path: Path, project_root: Path) -> bool:
    """
    Determines whether a smashlet should run based on timestamps, constants, and optional logic.

    Respects `RUN`, `RUN_TIMEOUT`, and `INPUT_GLOB` constants.
    Calls `should_run(context)` if defined in the smashlet.
    Falls back to comparing input/output timestamps and last run time.
    """

    # Load the smashlet module
    smashlet_mod = load_smashlet_module(smashlet_path)
    if not smashlet_mod:
        smash_log(f"{smashlet_path.name}: could not be loaded", level="warn")
        return False

    # Validate required functions
    smashlet_functions = {}
    for entry in SMASHLET_REQUIRED_FUNCTIONS:
        func = getattr(smashlet_mod, entry["name"], None)
        if entry["required"] and not callable(func):
            smash_log(
                f"{smashlet_path.name}: missing required function '{entry['name']}'",
                level="warn",
            )
            return False
        smashlet_functions[entry["name"]] = func

    # Load and validate constants
    smashlet_constants = {}
    for const in SMASHLET_CONSTANT_DEFAULTS:
        value = getattr(smashlet_mod, const["name"], const["default"])
        if const["allowed"] and value not in const["allowed"]:
            smash_log(
                f"{smashlet_path.name}: invalid constant {const['name']}={value}. Allowed: {const['allowed']}",
                level="warn",
            )
            return False
        smashlet_constants[const["name"]] = value

    # Load runlog info
    runlog = get_runlog(project_root)
    last_run = runlog.get(str(smashlet_path), {}).get("last_run", 0)

    # Handle RUN = 'always'
    if smashlet_constants["RUN"] == "always":
        timeout = smashlet_constants["RUN_TIMEOUT"]
        if (time.time() - last_run) >= timeout:
            return True
        else:
            smash_log(f"{smashlet_path.name}: RUN_TIMEOUT not reached", level="debug")
            return False

    # Load inputs (optional)
    input_glob = smashlet_constants["INPUT_GLOB"]
    inputs = list(smashlet_path.parent.glob(input_glob)) if input_glob else []

    # Load outputs (optional)
    if smashlet_functions.get("get_outputs"):
        outputs = smashlet_functions["get_outputs"]()
    else:
        outputs = [Path(p) for p in smashlet_constants.get("OUTPUT_FILES", [])]

    # should_run(context) override
    if smashlet_functions.get("should_run"):
        try:
            context = build_context(project_root)
            context.update(
                {
                    "cwd": smashlet_path.parent,
                    "inputs": inputs,
                    "smashlet_mtime": smashlet_path.stat().st_mtime,
                    "last_run": last_run,
                    "latest_input_mtime": max(
                        (f.stat().st_mtime for f in inputs), default=0
                    ),
                }
            )
            return smashlet_functions["should_run"](context)
        except Exception as e:
            smash_log(
                f"{smashlet_path.name}: error in should_run(context): {e}",
                level="error",
            )
            return False

    # Inputs vs outputs comparison
    if outputs:
        if any(not out.exists() for out in outputs):
            return True

        latest_output_mtime = max(out.stat().st_mtime for out in outputs)
        latest_input_mtime = max(
            [f.stat().st_mtime for f in inputs] + [smashlet_path.stat().st_mtime]
        )
        return latest_input_mtime > latest_output_mtime

    # Fallback: any input newer than last run
    files_to_check = inputs + [smashlet_path]
    return any(f.stat().st_mtime > last_run for f in files_to_check)


def run_smashlet(smashlet_path: Path, project_root: Path, global_context: dict) -> bool:
    """
    Executes a smashlet’s `run()` function with injected context.

    Combines global, local, and auto-generated context, including inputs.
    After execution, updates the runlog and returns True if the smashlet signals a change.
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
        start_time = time.time()

        # If run(context) is expected
        if len(sig.parameters) == 1:
            result = run_func(context)
        else:
            # Otherwise run() with no args
            result = run_func()

        end_time = time.time()
        duration = round(end_time - start_time, 3)

        # Mark it as run in the runlog
        update_runlog(project_root, smashlet_path, duration)

        return result == 1

    except Exception as e:
        smash_log(f"Error in {smashlet_path}: {e}", level="error")

        return False


def touch(path: Path):
    """
    Updates the modification time of a file or directory, like `touch` in Unix.

    Used to mark outputs as changed without modifying their contents.
    """
    path.touch(exist_ok=True)
