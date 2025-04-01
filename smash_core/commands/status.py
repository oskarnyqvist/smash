# status.py
#
# Implements the `smash status` command for dry-run build status reporting.

from smash_core.project import find_project_root
from smash_core.context_loader import build_context
from smash_core.smashlets import discover_smashlets, load_smashlet_module, get_runlog
from pathlib import Path
import time

ONE_MINUTE = 60
RUN_NEVER = 0


def run_status():
    """
    Analyze and print the status of each smashlet (dry run).

    Possible states:
    - ⚙️ will run (inputs changed)
    - ✅ up to date
    - ⏳ skipped (timeout not reached)
    - ⚠️ skipped (invalid or missing config)
    """
    project_root = find_project_root()
    if not project_root:
        print("❌ Not inside a Smash project (missing .smash/)")
        return

    context = build_context(project_root)
    runlog = get_runlog(project_root)
    smashlets = discover_smashlets(project_root)

    for path in sorted(smashlets):
        rel_path = path.relative_to(project_root)
        mod = load_smashlet_module(path)

        if not mod:
            print(f"⚠️ {rel_path} — skipped (failed to load)")
            continue

        run_func = getattr(mod, "run", None)
        if not callable(run_func):
            print(f"⚠️ {rel_path} — skipped (no run() function)")
            continue

        input_glob = getattr(mod, "INPUT_GLOB", None)
        if not input_glob:
            print(f"⚠️ {rel_path} — skipped (missing INPUT_GLOB)")
            continue

        run_mode = getattr(mod, "RUN", "if_changed")
        last_run = runlog.get(str(path), RUN_NEVER)

        if run_mode == "always":
            timeout = getattr(mod, "RUN_TIMEOUT", ONE_MINUTE)
            if timeout and (time.time() - last_run < timeout):
                print(f"⏳ {rel_path} — skipped (timeout not reached)")
                continue
            else:
                print(f"⚙️ {rel_path} — will run (RUN = 'always')")
                continue

        input_files = list(path.parent.glob(input_glob))

        if not input_files:
            print(f"⚙️ {rel_path} — will run (no matching inputs)")
            continue

        outputs = []
        if hasattr(mod, "get_outputs"):
            try:
                outputs = mod.get_outputs()
            except Exception:
                pass
        elif hasattr(mod, "OUTPUT_FILES"):
            outputs = [Path(p) for p in mod.OUTPUT_FILES]

        if outputs:
            if any(not o.exists() for o in outputs):
                print(f"⚙️ {rel_path} — will run (missing outputs)")
                continue
            latest_output = max(o.stat().st_mtime for o in outputs)
            latest_input = max(
                [f.stat().st_mtime for f in input_files] + [path.stat().st_mtime]
            )
            if latest_input > latest_output:
                print(f"⚙️ {rel_path} — will run (inputs changed)")
            else:
                print(f"✅ {rel_path} — up to date")
        else:
            latest = max(
                [f.stat().st_mtime for f in input_files] + [path.stat().st_mtime]
            )
            if latest > last_run:
                print(f"⚙️ {rel_path} — will run (inputs changed)")
            else:
                print(f"✅ {rel_path} — up to date")
