# Smash

Smash is a build system for content. It enables you to define, using plain Python, how files in each directory should be transformed into outputs — without requiring global configuration, dependency graphs, or custom formats.

Each directory can include one or more `smashlet_*.py` files that describe how files within that directory should be processed. Smash automatically discovers and runs these smashlets in a predictable and isolated way.

---

### Problem

Make is powerful but often unintuitive. A distributed approach lets you understand individual parts of the system without needing to read and comprehend the entire build.

Workflow engines like Luigi or Airflow excel at orchestrating complex pipelines. Smash takes a simpler, directory-based approach that doesn't rely on global scheduling or dependency management.

Static site generators primarily target websites and often enforce templating or layout assumptions. Smash focuses purely on transforming and assembling content and data, free from layout or templating constraints.

Smash is useful when you prefer to colocate build logic alongside the files it operates on — using plain Python, without central configuration or intricate dependency tracking.

---

### How Smash Works

Smash locates one or more `smashlet_*.py` files within your project's directories. Each smashlet defines how the files in its own directory should be transformed.

A smashlet file contains:

- `INPUT_GLOB`: a glob pattern specifying input files (e.g., `"*.md"`)
- `OUTPUT_DIR`: the directory where output files are placed
- `run()`: a Python function that performs the transformation
- If using `run(context)`, matching input files are passed via `context["inputs"]`.

Smash traverses the project directories, finds all smashlets, and executes them in order based on modification time (oldest first). After executing a smashlet, Smash updates its timestamp. This process repeats until all smashlets are up-to-date.

Each smashlet operates independently. There is no central build configuration or dependency graph — every smashlet contains the entirety of the information it requires.

---

### Why not Make, Luigi, or others?

Smash isn't trying to replace existing tools — it's addressing a different kind of problem. Here's how it compares:

#### 🛠️ Make

- Global logic in Makefiles
- Hard to reason about in large projects
- Small changes can have wide ripple effects

Smash: Distributed, explicit, file-scoped logic.

#### 🔁 Luigi / Airflow

- Ideal for scheduled DAGs and complex pipelines
- Heavyweight for si````mple local builds
- Requires lots of boilerplate and infra

Smash: Lightweight, local-first, no orchestrator.

#### 🌐 Static Site Generators

- Great for websites, less so for general content workflows
- Built-in assumptions about routing, layout, templates

Smash: No assumptions. Just code and files.

---

### Basic Usage

Start a new Smash project:

```bash
smash init
```

This creates a `.smash/` directory at the root of your project.

Then create one or more smashlets in a content directory:

```bash
touch content/smashlet_render.py
```

Run Smash:

```bash
smash
```

Smash scans for all `smashlet*.py` files and runs them in modification order. It repeats until no further changes are detected.

---

### 🛠 Force Re-running Smashlets

Smash normally skips any smashlet that hasn’t changed since the last build.  
You can override this with the `smash run` command:

```bash
# Default: only run smashlets with changed inputs
smash

# Force all smashlets to run, regardless of timestamps
smash run

# Run a specific smashlet directly
smash run path/to/smashlet_render.py
```

This is useful when:

- You're actively debugging a smashlet
- You want to reprocess all data without touching inputs
- You need full control over what runs

The behavior is always deterministic — no DAG, no hidden order. Just local files, running in modification time order.

````

---

### ✅ Insert under: `### Smashlet Structure` (near the `run()` explanation)

Add this sentence after:

> - `run()`: a Python function that performs the transformation

```md
The `run()` function can return:

- `1` → to indicate that outputs changed (triggers a rebuild loop)
- `0` or `None` → to indicate no changes (smashlet will be skipped next time)

⚠️ If a smashlet always returns `1`, Smash will re-run it repeatedly.
To prevent infinite loops, the build will stop after 10 iterations with an error.
````

---

### Smashlet Structure

Each smashlet file defines how files in its directory are processed. You can use a single `smashlet.py` for simple cases, or define multiple named files like `smashlet_clean.py`, `smashlet_render.py`, etc.

Example:

```python
# smashlet_render.py
INPUT_GLOB = "*.md"
OUTPUT_DIR = "dist/"

def run():
    from pathlib import Path

    inputs = list(Path(".").glob(INPUT_GLOB))
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    for f in inputs:
        content = f.read_text()
        html = f"<h1>{f.stem}</h1>\n<p>{content}</p>"

        out_path = Path(OUTPUT_DIR) / f.with_suffix(".html").name
        out_path.write_text(html)
```

Smash will automatically resolve `INPUT_GLOB` and inject a list of matching files as `context["inputs"]` (if using `run(context)`):

```python
def run(context):
    for f in context["inputs"]:
        print(f.name)
```

This eliminates boilerplate in your smashlet and makes it easier to write LLM-friendly or reusable logic.

Perfect — you're now officially on the clean path to a **stable public API** for your smashlets. Here's your next move, step-by-step:

---

## ✅ 1. Fill in `smash/__init__.py` with Public Helpers

Let’s start by re-exporting the useful smashlet-facing utilities. Add this to your new `smash/__init__.py`:

```python
# smash/__init__.py
#
# Public API for smashlets. Use `import smash` inside your smashlets.

from smash_core.helpers import (
    read_text_files,
    write_output,
    smash_log,
    ensure_dir,
    flatten_json_dir,
)

from smash_core.files import (
    read,
    write,
    resolve,
)

from smash_core.log import log as log_raw

# Aliases for consistent naming in smashlets
log_step = smash_log
log = log_raw
```

Now, inside any smashlet, you can:

```python
import smash

smash.log_step("Starting transformation")
text = smash.read("input.md", context)
smash.write("out/output.md", text.upper(), context)
```

---

## ✅ 2. Test It Locally (Editable Install)

Install your project in **editable mode** so that Python will pick up the `smash/` package you just created:

```bash
pip install -e .
```

Then open a Python shell and verify:

```python
import smash

smash.read_text_files  # Should work
smash.log_step("Test")  # Should print something
```

---

## ✅ 3. Update `setup.cfg` (optional if you're using `find:` correctly)

If `packages = find:` in `setup.cfg` is working, Setuptools will already pick up `smash/` and `smash_core/`.

You can double-check by running:

```bash
python -m pip list
```

Or inspecting the `.whl` with:

```bash
python setup.py sdist bdist_wheel
```

You should see both `smash` and `smash_core` packages in the `.tar.gz` or `.whl`.

---

### 📦 Public API: `import smash`

When writing smashlets, use `import smash` to access helpful utility functions:

```python
import smash

smash.log_step("Reading input...")
text = smash.read("input.md", context)
smash.write("out/output.md", text.upper(), context)
```

These are safe, portable, and context-aware. They work regardless of where your smashlet is run from.

Available functions include:

- `smash.read(path, context)`
- `smash.write(path, data, context)`
- `smash.resolve(path, context)`
- `smash.log_step(msg)`
- `smash.read_text_files(paths)`
- `smash.ensure_dir(path)`

### 🧠 Explicit Output Tracking (Optional)

Smashlets can optionally define the exact output files they generate. This allows Smash to skip the smashlet more intelligently by comparing input vs. output modification times.

This is useful when:

- Outputs don’t follow a predictable naming pattern
- You want precise rebuild logic
- You plan to use future features like `smash clean` or dry-run diffs

You can declare outputs in two ways:

#### 1. `get_outputs()`: preferred for dynamic or computed outputs

```python
from pathlib import Path

def get_outputs():
    return [
        Path("dist/index.html"),
        Path("dist/data.json"),
    ]
```

#### 2. `OUTPUT_FILES`: simple list of paths

```python
OUTPUT_FILES = [
    "dist/index.html",
    "dist/data.json",
]
```

### 🧠 Local and Project-Level Context Support

Smashlets can automatically receive config or metadata from JSON, YAML, or TXT files.

Smash scans two locations for contextual data:

1. `context/` or `context.json` in the **project root**
2. `context/` or `context.json` in the **smashlet’s directory**

All found data is injected into:

- `context["context"]` → a merged dictionary of loaded values
- `context["context_files"]` → raw `Path` objects for each file

---

#### Supported Files

| Extension | Behavior                         |
| --------- | -------------------------------- |
| `.json`   | Parsed with `json.loads()`       |
| `.yaml`   | Parsed if PyYAML is available    |
| `.txt`    | Read as plain text               |
| other     | Included in `context_files` only |

---

#### Precedence & Merging

- Project context is loaded first
- Smashlet-local context overrides any conflicting keys
- Multiple files are shallow-merged by filename stem

---

#### Example

```python
def run(context):
    config = context["context"]["config"]
    prompt = context["context_files"]["prompt.txt"].read_text()
```

This allows colocated prompts, configs, keys, or any metadata without manual file parsing.

### Multiple Smashlets in One Directory

You can define multiple independent transformation steps in a single directory using the `smashlet_<name>.py` naming convention:

```plaintext
docs/
├── smashlet_clean.py     # Removes comments or metadata
├── smashlet_render.py    # Converts cleaned content to HTML
```

Each smashlet is:

- Executed independently
- Tracked in the runlog separately
- Re-run only when inputs change or `RUN = "always"` is set

This makes it easy to compose and layer transformations locally, without needing global configuration or DAGs.

---

### Shared Project Logic with `smash.py`

Smash supports an optional `smash.py` file in your project root.

This file can:

- Store project-wide `config` values (available via context)
- Provide an `on_context()` hook to modify context before execution
- Export helper functions to import in your smashlets

Example `smash.py`:

```python
config = {
    "env": "production",
    "default_output": "dist/",
}

def on_context(context):
    context["version"] = "1.2.3"
    return context

def glob_from_root(pattern):
    from pathlib import Path
    return list((Path(__file__).parent / "").glob(pattern))

def read_json(path):
    import json
    return json.loads(path.read_text())
```

In a smashlet:

```python
from smash import glob_from_root, read_json

def run(context):
    files = glob_from_root("data/**/*.json")
    for f in files:
        data = read_json(f)
        # ... transform or merge content
```

---

### 📢 Logging from Smashlets with `smash.log()`

Instead of using `print()`, smashlets can call `smash.log()` for standardized output:

```python
import smash

def run():
    smash.log("Generating pages from markdown...")
```

This ensures all output uses the same style and can support future features like:

- Timestamps
- Log levels (info, warn, error, debug)
- Redirected or filtered output

Optional log level:

```python
smash.log("Missing input file", level="warn")
smash.log("Build failed", level="error")
```

This works both in smashlets and helper functions imported from `smash.py`.

````



---
## Project Layout Example

```plaintext
myproject/
├── .smash/                 # Created by `smash init`
├── content/
│   ├── pages/
│   │   ├── 001.md
│   │   ├── 002.md
│   │   ├── smashlet_clean.py
│   │   └── smashlet_render.py
│   └── data/
│       ├── part1.json
│       ├── part2.json
│       └── smashlet.py     # Still supported for single-step
├── smash.py                # Project-wide config + helpers
└── smash                   # CLI entry point
````

Each smashlet is discoverable, isolated, and self-contained.

---

Perfect — that’s the correct place for the update, and your snippet looks great. ✅

Now that the code is in place, let’s move to:

---

### Using `smash.files` for Safe File Access

Smash includes a helper module for safely reading, writing, and resolving file paths using the `context` object.

Instead of writing fragile relative paths like:

```python
Path("backlog/my_task.md").read_text()
```

You can use:

```python
from smash.files import read, write, resolve

def run(context):
    content = read("backlog/my_task.md", context)
    write("out/summary.md", f"Processed:\n{content}", context)

    full_path = resolve("data/stats.json", context)
```

This makes your smashlets:

- Safe to run from any working directory
- Easier for LLMs and devs to understand
- More portable and testable

All paths are automatically resolved relative to `context["cwd"]`, which always points to the smashlet’s directory.

---

### 🧭 `smash` vs `smash_core`: Which should I import?

If you're writing a **smashlet**, always import from `smash`, not `smash_core`.

Smash separates internal code from public helpers:

| Import From  | Purpose                           |
| ------------ | --------------------------------- |
| `smash`      | ✅ Safe, public API for smashlets |
| `smash_core` | ❌ Internal-only implementation   |

For example:

```python
# ✅ Do this in your smashlet:
from smash import read, write, resolve

# ❌ Avoid importing from smash_core directly
```

Even though many helpers live in `smash_core/` internally, they are exposed through `smash/` to keep your code clean and stable.

This design ensures your smashlets are portable, future-proof, and easy to understand — even if the internals change.

---

### ✅ Step 4: Add to `docs/CODE.md`

Let’s put this under a new section header:

---

````md
## 🔧 `smash.files` Helpers

Use the built-in `smash.files` module to safely access files relative to the smashlet’s directory:

```python
from smash.files import read, write, resolve
```
````

These functions resolve paths using `context["cwd"]`:

- `resolve(path, context)` → absolute `Path` to the file
- `read(path, context)` → string contents of the file
- `write(path, data, context)` → writes a string, creating parent folders

### Why this matters

- Smashlets are often run from outside their folder (e.g. via `smash`)
- This ensures file I/O works consistently and portably
- It improves testability and LLM understanding

Prefer these helpers over raw `Path("...")` calls.

`````


### 🪄 **📁 Injecting a `context/` Folder**

Add this new section under **"Shared Project Logic with `smash.py`"**:

---

````md
### Injecting a `context/` Folder

If your project root includes a `context/` folder, all files inside are automatically made available in the build `context`.

These are injected as:

```python
context["context_files"]  # dict[str, Path]
`````

````

Each key is the filename, and the value is a `Path` object you can read or parse. This is useful for colocated prompts, configs, or metadata.

Example usage in a smashlet:

```python
import json

def run(context):
    config = json.loads(context["context_files"]["config.json"].read_text())
    ...
```

Or define a helper in `smash.py`:

```python
def read_context_json(context, filename):
    import json
    return json.loads(context["context_files"][filename].read_text())
```

Only files (not subdirectories) are included, and hidden files are skipped.

### Use Cases

Smash is designed for structured content workflows, such as:

- Generating documentation from markdown and code
- Rendering diagrams from `.dot`, `.svg`, or `.plantuml` sources
- Merging data files into language- or region-specific outputs
- Producing LLM-ready prompts, datasets, or embeddings
- Collocating content logic with the content it transforms

---

### Philosophy and Contributing

Smash prioritizes:

- 📦 Locality over global config
- ✨ Predictability over cleverness
- 🤖 Clarity for humans and LLMs
- 💡 Self-contained transformation units
- 🧱 Build logic that lives with the content it serves

No DAGs. No YAMLs. No runtime magic.

Contributions are welcome — especially around CLI UX, new helper utilities, and plugins for other file types or workflows.

---

### 🧭 Contributing Tasks or Features?

Before starting work on a task or story, check out the [Task Analysis Protocol](STORY_CHECKLIST.md).

It helps ensure every feature or fix is:

- Clear in purpose
- Minimal in scope
- Aligned with Smash values

Whether you're a developer or an LLM, this guide helps you ship the right thing.

---

### License

MIT
````
