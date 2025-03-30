## 📄 `[Core] Support contextual overrides via context/ and context.json`

### What it does

Adds support for contextual files located at two levels:

1. **Project-level context**

   - `context/` folder or `context.json` at the project root
   - Injected into every smashlet’s `context["context_files"]` or `context["context"]`

2. **Smashlet-local context**
   - A `context/` folder or `context.json` in the **same directory** as a smashlet
   - Injected _only when that smashlet runs_

Both are available in the `context` dict passed to `run(context)`.

---

### Why it matters

- Smashlets should not have to hardcode config or metadata
- Locality is a core Smash principle — this makes context injection _local-first_
- Enables flexible workflows:
  - Project-wide config
  - Smashlet-specific prompts, inputs, tokens, etc.

---

### How it works

```python
# Directory: project_root/content/tasks/
# Files: smashlet.py, context/config.json

def run(context):
    config = context["context"]["config"]
```

Smash walks:

- `project_root/context/*.json` or `.txt`, `.yaml`, etc.
- `smashlet_dir/context/`
- `smashlet_dir/context.json`

Injects as:

```python
context["context"]         # dict of loaded data (JSON)
context["context_files"]   # raw Path objects keyed by filename
```

---

### Precedence and merging

- Project context is loaded first
- Smashlet-local context can override keys
- If multiple JSON files exist, they are shallow-merged

---

### File support

| Extension | Behavior                                   |
| --------- | ------------------------------------------ |
| `.json`   | `json.loads()`                             |
| `.yaml`   | if PyYAML is available                     |
| `.txt`    | `.read_text()`                             |
| other     | included as `Path` in `context_files` only |

---

### Verification

- Put a `context/config.json` in project root → available to all
- Put a `context.json` next to a smashlet → available only to that one
- Combine both → smashlet-local overrides project-level

---

### Suggested filename

```
add_context_file_support.md
```
