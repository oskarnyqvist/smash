# content/signatures/smashlet.py
#
# Generates `docs/signatures.md` — an API reference for public functions.
# Now includes:
# - Function signature
# - First 3 lines of docstring (non-empty)
# - Estimated line count (Lines: X)

import smash
import ast
from pathlib import Path

INPUT_GLOB = "*"
OUTPUT_FILE = "/../docs/signatures.md"

TARGET_DIR = "smash_core"


def format_signature(fn: ast.FunctionDef) -> str:
    args = []
    defaults = [None] * (len(fn.args.args) - len(fn.args.defaults)) + fn.args.defaults

    for arg, default in zip(fn.args.args, defaults):
        arg_str = arg.arg
        if arg.annotation:
            arg_str += f": {ast.unparse(arg.annotation)}"
        if default:
            arg_str += f" = {ast.unparse(default)}"
        args.append(arg_str)

    if fn.args.vararg:
        args.append(f"*{fn.args.vararg.arg}")
    if fn.args.kwarg:
        args.append(f"**{fn.args.kwarg.arg}")

    signature = f"def {fn.name}({', '.join(args)})"
    if fn.returns:
        signature += f" -> {ast.unparse(fn.returns)}"
    return signature


def extract_signatures(path: Path) -> list[tuple[str, list[str]]]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except Exception:
        return []

    sigs = []

    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
            continue

        sig = format_signature(node)
        notes = []

        # Docstring
        doc = ast.get_docstring(node)
        if doc:
            doc_lines = [line.strip() for line in doc.splitlines() if line.strip()]
            notes.extend(doc_lines[:3])
        else:
            notes.append("⚠️ No docstring")

        # Line count
        if hasattr(node, "end_lineno"):
            span = node.end_lineno - node.lineno + 1
            notes.append(f"Lines: {span}")

        # Type hint coverage
        has_type_hints = bool(
            node.returns or any(arg.annotation for arg in node.args.args)
        )
        notes.append(f"Type hints: {'✅' if has_type_hints else '❌'}")

        # Complexity metrics
        branches = loops = returns = calls = assigns = 0
        max_depth = 0
        call_names = set()

        def walk(n, depth=0):
            nonlocal branches, loops, returns, calls, assigns, max_depth
            max_depth = max(max_depth, depth)

            for child in ast.iter_child_nodes(n):
                if isinstance(child, (ast.If, ast.IfExp)):
                    branches += 1
                elif isinstance(child, (ast.For, ast.While)):
                    loops += 1
                elif isinstance(child, ast.Return):
                    returns += 1
                elif isinstance(child, ast.Assign):
                    assigns += 1
                elif isinstance(child, ast.Call):
                    calls += 1
                    if isinstance(child.func, ast.Name):
                        call_names.add(child.func.id)
                    elif isinstance(child.func, ast.Attribute):
                        call_names.add(child.func.attr)
                walk(child, depth + 1)

        walk(node)

        notes.append(
            f"Branches: {branches} | Loops: {loops} | Returns: {returns} | Calls: {calls} | Vars: {assigns} | Nesting: {max_depth}"
        )

        if call_names:
            sorted_names = sorted(call_names)
            notes.append(f"Calls: {', '.join(sorted_names)}")

        sigs.append((sig, notes))

    return sigs


def run(context):
    header = smash.resolve("header.md", context)

    root = smash.resolve("/..", context)

    target_dir = root / TARGET_DIR
    if not target_dir.exists():
        smash.log(f"Missing {TARGET_DIR}/ directory", level="error")
        return 1

    grouped = {}

    for path in target_dir.rglob("*.py"):
        if not path.is_file():
            continue
        items = extract_signatures(path)
        if items:
            rel_path = path.relative_to(root)
            grouped[str(rel_path)] = items

    lines = [header.read_text()]
    for file in sorted(grouped):
        lines.append(f"## {file}\n")
        lines.append("```python")
        for sig, notes in grouped[file]:
            lines.append(sig)
            for note in notes:
                lines.append(f"# {note}")
            lines.append("")  # Spacing
        lines.append("```")
        lines.append("")  # File spacing

    result = "\n".join(lines).strip() + "\n"
    dest = smash.resolve(OUTPUT_FILE, context)
    if smash.write_output_if_changed(dest, result, context):
        print(f"✅ Wrote function signature reference to {dest}")
        return 1

    print("ℹ️ Signature reference already up to date.")
    return 0
