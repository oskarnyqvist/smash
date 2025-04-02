"""
Runs the main Smash build loop and powers the `smash run` command.

Discovers all smashlets, checks if they should run, and executes them in modification-time order.
Used by the public CLI, but not part of the importable API.
"""

from pathlib import Path
from smash_core.project import find_project_root
from smash_core.smashlets import discover_smashlets, should_run, run_smashlet, touch
from smash_core.context_loader import build_context
from smash_core.log import log

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
        log("❌ Not inside a Smash project (missing .smash/)", level="error")
        return

    context = build_context(project_root)
    smashlets = discover_smashlets(project_root)

    log(f"🔍 Found {len(smashlets)} smashlet(s)")

    iterations = 0
    while True:
        ran_any = False

        for smashlet in sorted(smashlets, key=lambda p: p.stat().st_mtime):
            if force or should_run(smashlet, project_root):
                log(f"⚙️  Running: {smashlet.relative_to(project_root)}")
                changed = run_smashlet(smashlet, project_root, context)

                if changed:
                    touch(smashlet)
                    ran_any = True

        iterations += 1

        if not ran_any:
            log(f"✅ Build complete in {iterations} pass(es)")
            break

        if iterations >= MAX_ITERATIONS:
            log(
                "❌ Build exceeded max iterations. Possible infinite loop.",
                level="error",
            )
            break


def run_force(smashlet_path=None):
    """
    Force-run a specific smashlet, or all smashlets if none is given.
    """
    project_root = find_project_root()
    if not project_root:
        log("❌ Not inside a Smash project (missing .smash/)", level="error")
        return

    context = build_context(project_root)

    if smashlet_path:
        target = Path(smashlet_path)
        if not target.exists():
            log(f"❌ Smashlet not found: {smashlet_path}", level="error")
            return
        log(f"⚙️  Force running: {target}")
        run_smashlet(target, project_root, context)
        return

    run_build(force=True)
