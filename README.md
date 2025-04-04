<!-- AUTO-GENERATED BY content/readme_parts/smashlet.py -->

# Smash

Smash is a lightweight build system for content.

It lets you define, in plain Python, how files in a directory should be transformed — without global config, dependency graphs, or special formats.

Each directory contains its own `smashlet_*.py` files. These scripts declare what files to process and how. Smash runs them in order, automatically and predictably.

Built for developers who want local-first, scriptable workflows — not orchestration platforms or site engines.


### Why Smash?

Traditional tools make local content workflows harder than they should be.

- **Make** is powerful but brittle. One global file controls everything.
- **Luigi / Airflow** are great for orchestration, but overkill for local pipelines.
- **Static site generators** assume you're building a website.

Smash is different:

- No global config
- No DAGs
- No templating assumptions

Just plain Python files, colocated with the content they transform.


### How Smash Works

Smash scans your project for `smashlet_*.py` files. Each one defines a local transformation: which files to process, and how.

A smashlet declares:

- `INPUT_GLOB`: which files to match (e.g. `"*.md"`)
- `OUTPUT_DIR`: where to write results
- `run()` or `run(context)`: a function that does the work

Smash runs all smashlets in modification time order (oldest first). If any outputs change, it loops again — until everything is up to date.

Each smashlet is isolated. No global config. No dependency graph. No magic.


### Basic Usage

Initialize a new project:

```bash
smash init
```

This creates a `.smash/` directory in your project root.

Add a smashlet:

```bash
touch content/smashlet_render.py
```

Run the build:

```bash
smash
```

Smash finds all `smashlet*.py` files, runs them in modification time order, and repeats until nothing changes.

---

### 🛠 Re-running Smashlets

By default, Smash skips smashlets that haven’t changed.

Use `smash run` to override this:

```bash
# Run all smashlets, even if unchanged
smash run

# Run just one smashlet
smash run content/smashlet_render.py
```

Useful when:

- Debugging
- Reprocessing all outputs
- Forcing rebuilds without changing inputs

Builds are deterministic: no DAGs, no surprises.




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


### Helper Functions

Smash includes reusable helpers to reduce boilerplate and promote consistency in smashlets.

Import them with:

```python
from smash import read_text_files, write_output, ensure_dir, flatten_json_dir, smash_log
```

---

### Included Helpers

- `read_text_files(paths)`
  → Reads and returns the content of each file in `paths` as a list of strings.

- `write_output(path, content)`
  → Writes `content` to a file. Creates parent directories if needed.

- `write_output_if_changed(path, content, context)`
  → Writes only if content has changed. Prevents unnecessary rebuilds.

- `ensure_dir(path)`
  → Ensures that a directory exists. Creates it if missing.

- `flatten_json_dir(path)`
  → Reads all `.json` files in a directory and returns a flat dict: `{filename_stem: parsed_json}`

- `smash_log(msg)`
  → Consistent log output for smashlets. Equivalent to `smash.log()`.

---

### Example

```python
from smash import read_text_files, write_output_if_changed

def run(context):
    contents = read_text_files(context["inputs"])
    result = "\n\n---\n\n".join(contents)

    write_output_if_changed("dist/combined.md", result, context)
    return 1
```


### Logging from Smashlets

Use `smash.log()` for consistent, structured output instead of `print()`:

```python
import smash

def run():
    smash.log("Rendering markdown files...")
```

You can specify a log level:

```python
smash.log("Missing input file", level="warn")
smash.log("Build failed", level="error")
```

Supported levels:

- `"info"` (default)
- `"warn"`
- `"error"`
- `"debug"`

Logs are uniform across all smashlets and can support future features like timestamps, filtering, or redirection.


### Comparison

Smash solves a different problem than most build or pipeline tools.

#### 🛠️ Make

- Central Makefile controls everything
- Small changes can trigger large rebuilds
- Hard to scale with many inputs and rules

**Smash:** Local files define local logic. Easy to isolate and test.

---

#### 🔁 Luigi / Airflow

- Great for scheduled jobs and DAG orchestration
- Requires boilerplate, config, and a scheduler
- Not designed for lightweight, ad-hoc builds

**Smash:** Zero infra. Just run `smash` in your repo.

---

#### 🌐 Static Site Generators

- Assume you're building a website
- Force routing, layout, and template logic
- Hard to repurpose for other kinds of content

**Smash:** No layout engine. No site assumptions. Just Python and files.


### Philosophy

Smash is built around a few simple principles:

- 📦 Build logic should live with the files it transforms
- ✨ Behavior should be predictable and explicit
- 🤖 Everything should be understandable by both humans and LLMs
- 💡 Smashlets should be self-contained, portable units
- 🧱 No global state, no hidden dependencies

No DAGs. No YAMLs. No magic.

---

### Contributing

Contributions are welcome — especially:

- CLI improvements
- Helper utilities
- Plugins for new file types or workflows


## 📚 API Layers in Smash

Smash has three distinct API layers — each designed for a specific purpose and audience.

This clear separation makes the system simple to use, safe to extend, and easy to regenerate.

---

### 🟩 1. Public CLI API

> Used from the terminal via commands like `smash build`, `smash add`

This is the main interface for using Smash as a tool. It includes:

- `smash init`
- `smash build`
- `smash add <name>`
- `smash run`
- `smash status`

These commands are implemented internally but form a stable, user-facing interface.

---

### 🟨 2. Public Smashlet API

> Used inside `smashlet_*.py` files via `from smash import ...`

This API is the safe, supported way to write logic inside smashlets.

It includes:

- File I/O: `read`, `write`, `resolve`
- Context-aware output: `write_output`, `write_output_if_changed`
- Logging: `log`, `log_step`
- Helpers: `read_text_files`, `flatten_json_dir`, etc.

Smashlets should **only** import from `smash` — never from `smash_core`.

---

### 🟥 3. Internal Core API

> Used by contributors building or extending Smash itself

Implemented in `smash_core/`, this layer includes:

- CLI command logic (`commands/*.py`)
- Build engine logic (`smashlets.py`, `context_loader.py`)
- Core utilities (`project.py`, `files.py`, `log.py`)

This code is for internal use only — it’s **not part of the public interface** and may change at any time.

---

✅ This separation keeps user code clean and safe,  
🧠 while making the system easy to evolve, debug, and extend.


### License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.
