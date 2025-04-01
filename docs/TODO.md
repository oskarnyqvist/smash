# 📋 TODO

Generated from `todo/backlog/`

## Add default helpers

## [Core] Add default helper functions (`smash.helpers`)

### What it does

Adds a small set of reusable utility functions to `smash.helpers`, available to all smashlets via `from smash.helpers import ...`.

### Why it matters

Encourages consistent, clean patterns in user code. Reduces boilerplate and improves LLM compatibility.

### Hints

Include helpers like:

- `read_text_files(paths)`
- `write_output(path, content)`
- `log_step(msg)` or `smash_log(msg)`
- `flatten_json_dir(path)`
- `ensure_dir(path)`

Helpers should work out of the box and require no project configuration.

### Example usage

```python
from smash.helpers import read_text_files

def run():
    for text in read_text_files(context["inputs"]):
        ...
```

---

## Add file helpers for context

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

---

## Add pypi publish script

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

## Context folder support

## [Core] Support `context/` folder injection

### What it does

Adds support for a `context/` folder at the project root. All files inside are made available in the smashlet `context`.

### Why it matters

Allows colocated config, prompts, or metadata to be used in smashlets or `smash.py`. Useful for LLM workflows, reusable configs, and automation.

### Hints

- Inject files as `context["context_files"]`
  - Keys = filenames (e.g. `"config.json"`)
  - Values = `Path` objects or content (e.g. `str`, `dict`)
- Hook into this from `on_context()` if needed
- Add helper in `smash.py` to access these easily

### Example

```python
config = json.loads(context["context_files"]["config.json"].read_text())
```

---

## Generate file overview

## 📄 `[Docs] Add file overview smashlet to generate docs/files.md`

### What it does

Creates a smashlet that walks the project directory tree and generates a human- and LLM-readable `docs/files.md`. Each file is listed with a brief purpose or hint, allowing fast onboarding and exploration.

---

### Why it matters

- Makes it easy to understand the project structure at a glance
- Helps LLMs identify the right file to read or edit
- Aids contributors in locating logic, smashlets, tests, or docs
- Improves transparency and discoverability for unfamiliar users

---

### Output

```markdown
# 🗂 File Overview

## smash_core/

- `cli.py` – CLI entry point with subcommands
- `commands.py` – High-level build/init logic
- `project.py` – Runlog + project root detection

## content/todo/backlog/

- `status_command.md` – Add `smash status` to show run state
  ...
```

---

### How it works

- Walk the project using `Path().rglob("*")`
- Filter out `__pycache__`, `.git`, `*.pyc`, etc.
- For each `.py` or `.md` file, grab the first comment or heading
- Render results grouped by directory, alphabetically

---

### Considerations

- Could optionally support `docs/files.html` for rendered output
- Could be run automatically as part of `smash build`
- Can pull file hints from the first comment block or markdown title

---

### Verification

- Run smashlet → `docs/files.md` should appear
- Should include every `.py`, `.md`, `.toml`, `.cfg`, etc.
- Each file should include a short purpose/hint if possible

---

### Suggested filename

```
generate_file_overview.md
```

---

## Generate function signatures

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

---

## Refactor docs quality review

## [Docs] Documentation clarity & cleanup pass

### What it does

Reviews and refines all existing documentation files:

- `README.md`
- Files in `docs/` (GUIDE, CODE, TASKS, etc.)

Focus is on improving clarity, reducing redundancy, and removing anything that isn’t up-to-date or essential. We should treat tokens as precious — only say what matters.

Also identifies gaps where examples, behavior, or principles are missing.

### Why it matters

Smash’s philosophy is built on clear thinking and local reasoning.  
The docs should reflect that: no fluff, no outdated examples, no redundant explanations. Just the right amount of guidance to empower users, contributors, and LLMs.

High-quality docs make Smash easier to adopt, extend, and trust.

### Hints

- Start with `README.md` — is everything relevant and current?
- Review each `docs/*.md` file:
  - Does it explain intent, not just implementation?
  - Is anything repeated or unnecessary?
  - Could it be broken up, renamed, or merged?
- Are the examples simple and meaningful?
- Is terminology consistent? (smashlet, context, runlog, etc.)

This task can be done in parts — even identifying what needs changing is valuable.

---

## Runlog viewer command

## [Feature] `smash runlog` command

### What it does

Adds a CLI command to display when each smashlet last ran, along with a reason for its current state.

### Why it matters

Improves visibility into Smash’s internal logic. Helps developers and LLMs understand when and why each smashlet is triggered — especially useful for debugging or automation.

### Hints

- Use the `runlog.json` file as source of truth
- For each smashlet, print:
  - File name
  - Last run timestamp
  - Reason: "up to date", "inputs changed", "timeout not reached", etc.
- Consider emoji or colors for clarity

### Example output

```

✅ smashlet_clean.py — last run 2025-03-27 08:03
⏳ smashlet_download.py — skipped (timeout not reached)
⚙️ smashlet_compile.py — will run (inputs changed)

```

---

## Tests cli

### Title:

**[Test] Integration test suite for Smash CLI**

### What it does:

Adds a **minimal set of integration tests** that simulate user behavior by running the `smash` CLI and verifying file outputs or printed logs.

### Why it matters:

Ensures real-world usage works as expected, from initializing a project to running builds. Especially valuable once CLI gets more features or `click` support.

### Options for implementation:

#### A. **Use `subprocess` + `shutil.copy` CLI**

- Works now
- Tests real CLI script
- More brittle

#### B. **Switch to `click` and use `CliRunner`**

- More elegant and testable
- Allows in-process CLI tests without subprocesses
- Requires small refactor of CLI code

### Scope:

- `smash init` creates `.smash/`
- `smash add` creates `smashlet_<name>.py`
- `smash build` runs logic
- Failures, help messages, invalid args, etc.

### Structure:

- `tests/integration/`
  - `test_cli_init.py`
  - `test_cli_add.py`
  - `test_cli_build.py`

### Verification:

```bash
pytest tests/integration/
```

or

```bash
python tests/integration/test_cli_init.py
```
