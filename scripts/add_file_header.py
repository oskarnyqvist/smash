# add_file_header.py

# FILE: add_file_header.py

from pathlib import Path

HEADER_TEMPLATE = "# {filename}"


def should_skip(path):
    # Skip virtual envs, hidden dirs, build output, dist
    return any(
        part.startswith(".") or part in {"dist", "build", "__pycache__", "venv", "env"}
        for part in path.parts
    )


def add_header_to_file(py_file: Path):
    lines = py_file.read_text(encoding="utf-8").splitlines()

    header_line = HEADER_TEMPLATE.format(filename=py_file.name)

    # Already has correct header?
    if lines and lines[0].strip() == header_line:
        return False  # no change

    # Determine if there's a docstring
    if lines and lines[0].startswith(('"""', "'''")):
        # Find where the docstring ends
        end_idx = 0
        quote = lines[0][:3]
        for i, line in enumerate(lines[1:], 1):
            if line.strip().endswith(quote):
                end_idx = i
                break
        # Insert header above docstring
        new_lines = [header_line, ""] + lines
    else:
        # Insert header at top
        new_lines = [header_line, ""] + lines

    py_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return True


def main():
    project_root = Path(__file__).resolve().parents[1]
    py_files = list(project_root.rglob("*.py"))

    changed = 0
    for py_file in py_files:
        if should_skip(py_file.relative_to(project_root)):
            continue

        if add_header_to_file(py_file):
            print(f"📝 Updated header: {py_file}")
            changed += 1

    print(f"\n✅ Done. Updated {changed} file(s).")


if __name__ == "__main__":
    main()
