# scripts/add_file_header.py

# FILE: add_file_header.py

from pathlib import Path

HEADER_TEMPLATE = "# {filename}"


def should_skip(path):
    # Skip virtual envs, hidden dirs, build output, dist
    return any(
        part.startswith(".") or part in {"dist", "build", "__pycache__", "venv", "env"}
        for part in path.parts
    )


def add_header_to_file(py_file: Path, project_root: Path):
    rel_path = py_file.relative_to(project_root)
    correct_header = f"# {rel_path.as_posix()}"

    lines = py_file.read_text(encoding="utf-8").splitlines()

    changed = False

    # If file starts with a comment like "# somefile.py"
    if lines and lines[0].startswith("#"):
        stripped = lines[0].lstrip("#").strip()
        if stripped.endswith(py_file.name):
            # Replace old header if not correct
            if lines[0].strip() != correct_header:
                lines[0] = correct_header
                changed = True
            else:
                return False  # already correct
        else:
            # First line is a comment but not a file header → prepend
            lines = [correct_header, ""] + lines
            changed = True
    else:
        # No header at all → insert it
        lines = [correct_header, ""] + lines
        changed = True

    py_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def main():
    project_root = Path(__file__).resolve().parents[1]
    py_files = list(project_root.rglob("*.py"))

    changed = 0
    for py_file in py_files:
        if should_skip(py_file.relative_to(project_root)):
            continue

        if add_header_to_file(py_file, project_root):
            print(f"📝 Updated header: {py_file}")
            changed += 1

    print(f"\n✅ Done. Updated {changed} file(s).")


if __name__ == "__main__":
    main()
