# 📋 TODO

Generated from `todo/backlog/`

## 190 add pypi publish script

## 📄 `[Infra] Add script for deploying Smash to PyPI`

### What it does

Adds a simple, reproducible script that builds and uploads the current version of Smash to [PyPI](https://pypi.org/), making it installable via `pip install smash`.

---

### Why it matters

- Simplifies publishing new versions
- Makes versioning and releases consistent
- Encourages safer, repeatable releases
- Allows LLMs (and humans) to trace version history more easily

---

### What to include

✅ A script like `scripts/publish.sh`:

```bash
#!/bin/bash
set -e

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python3 -m build

# Upload to PyPI (requires `twine`)
twine upload dist/*
```

✅ Optionally add `scripts/publish_test.sh` for TestPyPI.

---

### Requirements

Make sure these are added to `dev-dependencies` (e.g., in `pyproject.toml` or `requirements-dev.txt`):

```toml
[tool.poetry.dev-dependencies]
build = "*"
twine = "*"
```

Or for pip-based workflows:

```
pip install build twine
```

---

### Verification

Run:

```bash
./scripts/publish.sh
```

You should see:

- A wheel + tarball in `dist/`
- Upload success message from Twine

---

---

## 210 generate function signatures

## 📄 `[Docs] Add smashlet to generate function signature reference`

### What it does

Creates a smashlet that scans Python source files and extracts top-level function signatures into a structured markdown document:  
📄 `docs/signatures.md`

This file serves as a **public API reference** for both contributors and LLMs — showing how to call core functions across the codebase.

---

### Why it matters

- Helps developers and LLMs understand the available building blocks
- Reduces the need to scan through source files for parameter info
- Complements `docs/files.md` by answering _“how do I use this?”_
- Prepares for smarter LLM-based refactors and feature work

---

### Output example

````markdown
# 🔍 Function Signatures

## smash_core/commands.py

```python
def run_add_smashlet(name, glob="*", output="dist/", context_mode=False)
def run_build()
def run_init()
```
````

## smash_core/project.py

```python
def find_project_root() → Path | None
def get_runlog(project_root: Path) → dict
def update_runlog(project_root: Path, smashlet_path: Path)
```

```

---

### How it works

- Use Python’s `ast` module or `inspect` to:
  - Parse each `.py` file under `smash_core/`
  - Collect top-level `def` names, parameters, return annotations (if present)
- Group results by file
- Format in Markdown with fenced code blocks

---

### Considerations

- Should ignore private functions (`_name`) unless explicitly exported
- Optional: extract and include 1-line docstrings under each function
- Future: support module-level `__all__` export filtering

---

### Verification

- Generated `docs/signatures.md` contains:
  - All public `def` signatures from `smash_core/`
  - Grouped by file
  - Sorted by function name

---

### Suggested filename

```

generate_function_signatures.md

```

```
