# smashlet.py
#
# Generates `docs/FILES.md` — a human- and LLM-readable index of core code files.
# It focuses on Python files in key directories: smash_core, smash, and tests.
# Uses the AST module to extract module-level docstrings, function and class definitions,
# and line counts to provide richer file information.

import smash
import ast
import datetime

INPUT_GLOB = "*"  # Not used directly here.
OUTPUT_FILE = "/../docs/FILES.md"  # Adjust as needed.

INCLUDE_DIRS = {"smash_core", "smash", "tests"}
SKIP_EXTS = {".pyc", ".pyo", ".so", ".png", ".jpg", ".jpeg", ".svg"}


def analyze_python_file(path):
    """
    Parses the Python file at 'path' and returns a dict with:
      - 'path': the file's path as a string
      - 'lines': number of non-empty lines
      - 'docstring': the module-level docstring (if any)
      - 'functions': list of top-level function names
      - 'classes': list of top-level class names
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception:
        return None

    info = {
        "path": str(path),
        "lines": len([line for line in source.splitlines() if line.strip()]),
        "docstring": ast.get_docstring(tree),
        "functions": [],
        "classes": [],
        "size": path.stat().st_size,
        "modification_date": datetime.datetime.fromtimestamp(
            path.stat().st_mtime
        ).isoformat(),
        "dependencies": set(),
    }
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            info["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            info["classes"].append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                info["dependencies"].add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                info["dependencies"].add(node.module)
    info["dependencies"] = sorted(info["dependencies"])
    return info


def get_hint(path):
    """
    For Python files, returns a rich summary including:
      - The first line of the module docstring (if any)
      - The names of top-level functions and classes
      - The number of non-empty lines
    Returns an empty string for non-Python files or if no info is found.
    """
    if path.suffix != ".py":
        return ""
    info = analyze_python_file(path)
    if not info:
        return ""
    parts = []
    if info["docstring"]:
        lines = info["docstring"].splitlines()
        lines = [x for x in lines if x.strip()]
        name = str(path).split("/")[-1]
        lines = [x for x in lines if not x.endswith(name)]

        parts.extend(lines)
        # parts.append(f"{' '.join(info['docstring'].splitlines())}")
    if info["functions"]:
        parts.append(f" Functions: {', '.join(info['functions'])}")
    if info["classes"]:
        parts.append(f" Classes: {', '.join(info['classes'])}")
    parts.append(f" Lines of code: {info['lines']}")

    if info["dependencies"]:
        parts.append(f" (Imports: {', '.join(info['dependencies'])})")
    return parts


def run(context):
    # Determine project root: one level above the current 'content/' directory.
    root = smash.resolve("/..", context)
    grouped = {}

    # Walk only the INCLUDE_DIRS directories.
    for dir_name in INCLUDE_DIRS:
        target_dir = root / dir_name
        if not target_dir.exists():
            continue
        for path in target_dir.rglob("*"):
            if not path.is_file() or path.suffix not in {".py", ".md", ".toml", ".cfg"}:
                continue
            if path.suffix in SKIP_EXTS:
                continue
            rel = path.relative_to(root)
            parent = rel.parts[0] if len(rel.parts) > 1 else "."
            grouped.setdefault(parent, []).append(rel)

    # Build the file overview content.
    lines = ["# 🗂 File Overview", ""]
    for group in sorted(grouped):
        lines.append(f"## {group}/")
        for file in sorted(grouped[group]):
            full = root / file
            hint = get_hint(full)
            lines.append(f"- `{file}`")
            for h in hint:
                lines.append(f"    {h}")
        lines.append("")
    result = "\n".join(lines).strip() + "\n"

    dest = smash.resolve(OUTPUT_FILE, context)
    if smash.write_output_if_changed(dest, result, context):
        print(f"✅ Wrote file overview to {dest}")
        return 1

    print("ℹ️ File overview already up to date.")
    return 0
