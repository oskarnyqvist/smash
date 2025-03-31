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

MAX_ITERATIONS = 10  # Prevent infinite build loops


# Optional helper for accessing JSON configs in context/
def read_context_json(context, filename):
    import json

    return json.loads(context["context_files"][filename].read_text())


def build_context(project_root):
    """
    Build and return the full context dictionary for a project.

    Includes:
    - project_root
    - context/ files
    - optional smash.py config + on_context
    """
    context = {"project_root": project_root}

    # Inject context/ files
    context_dir = project_root / "context"
    if context_dir.exists() and context_dir.is_dir():
        context_files = {
            f.name: f
            for f in context_dir.iterdir()
            if f.is_file() and not f.name.startswith(".")
        }
        context["context_files"] = context_files

    # Optional smash.py
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

    return context


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


def run_build(force=False):
    """
    Execute the Smash build loop.

    Discovers all `smashlet.py` files and runs them in timestamp order.
    Repeats until no smashlet makes further changes.
    """

    project_root = find_project_root()
    if not project_root:
        print("❌ Not inside a Smash project (missing .smash/)")
        return

    context = context = build_context(project_root)
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
            print(
                "❌ Build exceeded max iterations. Possible infinite loop in smashlet(s)."
            )
            break


def run_add_smashlet(name=None, glob="*", output="dist/", context_mode=False):
    """
    Create a new smashlet file with boilerplate contents.

    Args:
        name (str or None): If provided, creates `smashlet_<name>.py`, else `smashlet.py`
    """
    from pathlib import Path

    if name:
        filename = f"smashlet_{name}.py"
        display_name = name
    else:
        filename = "smashlet.py"
        display_name = "(unnamed)"

    path = Path.cwd() / filename

    if path.exists():
        print(f"⚠️  {filename} already exists. Aborting.")
        return

    run_signature = "def run(context):" if context_mode else "def run():"
    run_body = "    pass  # TODO: implement transformation logic"

    template = f'''# {filename}
#
# Smashlet: {display_name}
# Auto-generated with `smash add`

INPUT_GLOB = "{glob}"
OUTPUT_DIR = "{output}"

{run_signature}
{run_body}
'''

    path.write_text(template)
    print(f"✅ Created {filename}")


def run_force(smashlet_path=None):
    """
    Force-run a single smashlet or all smashlets, bypassing skip logic.
    """
    from .smashlets import run_smashlet

    project_root = find_project_root()
    if not project_root:
        print("❌ Not inside a Smash project (missing .smash/)")
        return

    context = build_context(project_root)

    # Run one specific smashlet
    if smashlet_path:
        target = Path(smashlet_path)
        if not target.exists():
            print(f"❌ Smashlet not found: {smashlet_path}")
            return
        print(f"⚙️  Force running: {target}")
        run_smashlet(target, project_root, context)
        return

    # Run all smashlets with force
    run_build(force=True)
