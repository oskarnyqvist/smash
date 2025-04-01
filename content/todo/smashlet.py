# smashlet.py
#
# Renders all task markdown files in `backlog/*.md` into a combined TODO.md.
# Output is written to the root-level `docs/TODO.md`.

from smash import write, resolve

INPUT_GLOB = "backlog/*.md"
OUTPUT_DIR = "../../docs"


def run(context):
    task_files = sorted(resolve("backlog", context).glob("*.md"))

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

    write(f"{OUTPUT_DIR}/TODO.md", result, context)
    print(f"✅ Wrote {len(sections)} tasks to {OUTPUT_DIR}/TODO.md")
    return 1
