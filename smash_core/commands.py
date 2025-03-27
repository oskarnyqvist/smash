# commands.py
#
# High-level Smash commands used by the CLI.
# Handles project initialization and the build loop.

from pathlib import Path
from .project import find_project_root
from .smashlets import (
    discover_smashlets,
    should_run,
    run_smashlet,
    touch,
)


# Optional helper for accessing JSON configs in context/
def read_context_json(context, filename):
    import json

    return json.loads(context["context_files"][filename].read_text())


def run_init():
    """
    Create a new Smash project by making a `.smash/` directory.

    This directory marks the project root and stores metadata like the runlog.
    Does nothing if `.smash/` already exists.
    """
    project_root = Path.cwd()
    smash_dir = project_root / ".smash"

    if smash_dir.exists():
        print("✅ Project already initialized.")
        return

    try:
        smash_dir.mkdir()
        print("✅ Initialized new Smash project.")
    except Exception as e:
        print(f"❌ Failed to create .smash/: {e}")


def run_build():
    """
    Execute the Smash build loop.

    Discovers all `smashlet.py` files and runs them in timestamp order.
    Repeats until no smashlet makes further changes.
    """

    project_root = find_project_root()
    if not project_root:
        print("❌ Not inside a Smash project (missing .smash/)")
        return

    context = {
        "project_root": project_root,
    }

    # 📁 Inject context/ files if they exist
    context_dir = project_root / "context"
    if context_dir.exists() and context_dir.is_dir():
        context_files = {
            f.name: f
            for f in context_dir.iterdir()
            if f.is_file() and not f.name.startswith(".")
        }
        context["context_files"] = context_files

    # 📦 Optional: Load smash.py if present
    smash_py = project_root / "smash.py"
    # Try to import smash.py if it exists
    smash_py = project_root / "smash.py"
    if smash_py.exists():
        import importlib.util

        spec = importlib.util.spec_from_file_location("smash", smash_py)
        smash_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(smash_mod)

        if hasattr(smash_mod, "config"):
            context["config"] = smash_mod.config

        if hasattr(smash_mod, "on_context"):
            context = smash_mod.on_context(context) or context

    smashlets = discover_smashlets(project_root)
    print(f"🔍 Found {len(smashlets)} smashlet(s)")

    iterations = 0

    while True:
        ran_any = False

        for smashlet in sorted(smashlets, key=lambda p: p.stat().st_mtime):
            if should_run(smashlet, project_root):
                print(f"⚙️  Running: {smashlet.relative_to(project_root)}")
                changed = run_smashlet(smashlet, project_root, context)

                if changed:
                    touch(smashlet)
                    ran_any = True

        iterations += 1

        if not ran_any:
            print(f"✅ Build complete in {iterations} pass(es)")
            break
