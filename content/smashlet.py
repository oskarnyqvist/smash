from pathlib import Path

INPUT_GLOB = "tasks/*.md"
OUTPUT_DIR = "."


def run(context={}):
    out_path = Path(OUTPUT_DIR) / "TODO.md"
    task_files = sorted(Path(".").glob(INPUT_GLOB))

    if not task_files:
        print("No task files found.")
        return 0

    sections = []

    for f in task_files:
        content = f.read_text().strip()
        if not content:
            continue

        # Extract stem and reformat heading
        title = f.stem.replace("_", " ")
        header = f"## {f.stem} – {title.capitalize()}"
        sections.append(f"{header}\n\n{content}")

    result = "\n\n---\n\n".join(sections) + "\n"
    out_path.write_text(result)

    print(f"✅ Wrote {len(sections)} tasks to {out_path}")
    return 1
