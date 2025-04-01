# 📋 TODO

Generated from `todo/backlog/`

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
