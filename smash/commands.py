from pathlib import Path
from .project import find_project_root
from .smashlets import (
    discover_smashlets,
    should_run,
    run_smashlet,
    touch,
)


def run_init():
    project_root = Path.cwd()
    smash_dir = project_root / ".smash"

    if smash_dir.exists():
        print("✅ .smash/ already exists. Nothing to do.")
        return

    try:
        smash_dir.mkdir()
        print("✅ Created .smash/ directory.")
    except Exception as e:
        print(f"❌ Failed to create .smash/: {e}")


def run_build():
    project_root = find_project_root()
    if not project_root:
        print("❌ Not inside a Smash project (missing .smash/)")
        return

    smashlets = discover_smashlets(project_root)
    print(f"🔍 Found {len(smashlets)} smashlets")

    iterations = 0
    while True:
        ran_any = False
        for smashlet in sorted(smashlets, key=lambda p: p.stat().st_mtime):
            if should_run(smashlet, project_root):
                print(f"⚙️  Running: {smashlet.relative_to(project_root)}")
                changed = run_smashlet(smashlet, project_root)
                if changed:
                    touch(smashlet)
                    ran_any = True
        iterations += 1
        if not ran_any:
            print(f"✅ Build complete in {iterations} pass(es)")
            break
