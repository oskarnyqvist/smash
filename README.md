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
- Heavyweight for simple local builds
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

````

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

Smash determines whether to run a smashlet by comparing the modification times of its inputs to the smashlet file itself.

---

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
```

Each smashlet is discoverable, isolated, and self-contained.

---

### 🪄 **📁 Injecting a `context/` Folder**

Add this new section under **"Shared Project Logic with `smash.py`"**:

---

```md
### Injecting a `context/` Folder

If your project root includes a `context/` folder, all files inside are automatically made available in the build `context`.

These are injected as:

```python
context["context_files"]  # dict[str, Path]
```

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
```

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

### License

MIT

````
