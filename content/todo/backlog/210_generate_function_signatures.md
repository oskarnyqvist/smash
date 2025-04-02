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
