### Helpers and Context Access

Smash includes utility functions and automatic context injection to simplify common tasks in your smashlets.

---

### File Access with `smash.files`

Use `read()`, `write()`, and `resolve()` for path-safe file operations:

```python
from smash import read, write, resolve

def run(context):
    content = read("data/input.txt", context)
    write("out/output.txt", content.upper(), context)
```

These functions:

- Resolve paths based on the smashlet’s location (`context["cwd"]`)
- Work regardless of current working directory
- Make smashlets easier to debug, refactor, and reuse

---

### Context Folder Injection

If your project or smashlet includes a `context/` folder, all its files are automatically available:

```python
context["context"]        # Parsed JSON/YAML/TXT files
context["context_files"]  # Raw Path objects for each file
```

Example:

```python
def run(context):
    prompt = context["context_files"]["prompt.txt"].read_text()
    config = context["context"]["config"]
```

Supports:

| Extension | Behavior           |
| --------- | ------------------ |
| `.json`   | Parsed with `json` |
| `.yaml`   | Parsed if `pyyaml` |
| `.txt`    | Plain text         |
| others    | Available as Paths |

Smashlet-local context overrides project-level context. Only files (not folders) are included.
