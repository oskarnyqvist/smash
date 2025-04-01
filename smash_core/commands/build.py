# build.py
#
# Implements the main Smash build loop and the `run` (force) command.

from pathlib import Path
from smash_core.project import find_project_root
from smash_core.smashlets import discover_smashlets, should_run, run_smashlet, touch
from smash_core.context_loader import build_context

MAX_ITERATIONS = 10  # Prevent infinite build loops


def run_build(force=False):
    """
    Run the full Smash build loop.

    - Discovers all smashlets in the project
    - Runs each in mtime order
    - Repeats until no smashlet returns `1`
    - Stops after MAX_ITERATIONS to avoid infinite loops
    """
    project_root = find_project_root()
    if not project_root:
        print("❌ Not inside a Smash project (missing .smash/)")
        return

    context = build_context(project_root)
    smashlets = discover_smashlets(project_root)

    print(f"🔍 Found {len(smashlets)} smashlet(s)")

    iterations = 0
    while True:
        ran_any = False

        for smashlet in sorted(smashlets, key=lambda p: p.stat().st_mtime):
            if force or should_run(smashlet, project_root):
                print(f"⚙️  Running: {smashlet.relative_to(project_root)}")
                changed = run_smashlet(smashlet, project_root, context)

                if changed:
                    touch(smashlet)
                    ran_any = True

        iterations += 1

        if not ran_any:
            print(f"✅ Build complete in {iterations} pass(es)")
            break

        if iterations >= MAX_ITERATIONS:
            print("❌ Build exceeded max iterations. Possible infinite loop.")
            break


def run_force(smashlet_path=None):
    """
    Force-run a specific smashlet, or all smashlets if none is given.
    """
    project_root = find_project_root()
    if not project_root:
        print("❌ Not inside a Smash project (missing .smash/)")
        return

    context = build_context(project_root)

    if smashlet_path:
        target = Path(smashlet_path)
        if not target.exists():
            print(f"❌ Smashlet not found: {smashlet_path}")
            return
        print(f"⚙️  Force running: {target}")
        run_smashlet(target, project_root, context)
        return

    # Run all with --force
    run_build(force=True)
