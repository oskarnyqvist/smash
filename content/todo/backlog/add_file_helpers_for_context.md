## 📄 `[Core] Add smash.files helper for path-safe, context-aware file handling`

### What it does

Introduces a `smash.files` module that provides helper functions for reading, writing, and resolving files **relative to the smashlet's directory** — using the injected `context`.

Smashlets often struggle with hardcoded relative paths or assumptions about where they're being run from. This helper eliminates that fragility.

---

### Why it matters

- Smashlets should be portable and relocatable — but relative paths break when run from outside the smashlet dir
- LLMs and devs should not need to reason about `"../../docs"` vs `Path(context["cwd"]) / ...`
- This makes content read/write safe, testable, and consistent
- Prepares for structured file handling: YAML, JSON, Markdown, rendered outputs, etc.

---

### Example Usage

```python
from smash.files import read, write, resolve

def run(context):
    content = read("backlog/my_task.md", context)
    write("out/summary.md", f"Processed:\n{content}", context)

    full_path = resolve("data/stats.json", context)
```

---

### Proposed API (in `smash/files.py`)

```python
def resolve(relative_path: str, context) -> Path:
    return Path(context["cwd"]) / relative_path

def read(relative_path: str, context) -> str:
    return resolve(relative_path, context).read_text()

def write(relative_path: str, data: str, context) -> None:
    path = resolve(relative_path, context)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
```

---

### Future ideas

- `read_json()`, `write_json()`
- `read_yaml()` if `pyyaml` is installed
- `render_markdown()`, `render_template()` for docs
- `list_inputs(glob, context)` as a wrapper for input discovery

---

### Verification

- Replace hardcoded paths in existing smashlets (like `TODO.md` generator)
- Write tests that run smashlets from outside their folders
- Validate that file I/O is consistent regardless of CWD
