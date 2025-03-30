# smashlet.py
#
# Renders all task markdown files in `backlog/*.md` into a combined TODO.md.
# Output is written to the root-level `docs/TODO.md`.

from pathlib import Path

INPUT_GLOB = "backlog/*.md"
OUTPUT_DIR = "../../docs"


def run(context={}):
    cwd = Path(context.get("cwd", "."))
    out_path = cwd / OUTPUT_DIR / "TODO.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    task_dir = cwd / "backlog"
    task_files = sorted(task_dir.glob("*.md"))

    if not task_files:
        print("No task files found.")
        return 0

    sections = []
    for f in task_files:
        content = f.read_text().strip()
        if not content:
            continue

        title = f.stem.replace("_", " ").strip().capitalize()
        header = f"## {title}"
        sections.append(f"{header}\n\n{content}")

    result = (
        "# 📋 TODO\n\nGenerated from `todo/backlog/`\n\n"
        + "\n\n---\n\n".join(sections)
        + "\n"
    )
    out_path.write_text(result)

    print(f"✅ Wrote {len(sections)} tasks to {out_path.resolve()}")
    return 1
