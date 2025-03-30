# 📋 TODO

Generated from `todo/backlog/`

## Add context docs

Absolutely — here’s a complete task story for generating `docs/context.md` from a smashlet, ready for your backlog:

---

## 📄 `[Docs] Add smashlet to generate context documentation (docs/context.md)`

### What it does

Creates a smashlet that generates `docs/context.md`, explaining how the `context` object works in Smash. It covers project-level and smashlet-local context files, file formats, override rules, and usage examples.

---

### Why it matters

- `context` is one of the most important ideas in Smash
- Contributors and LLMs need a clear mental model for how data is injected into smashlets
- Makes workflows more predictable and configurable
- Aligns with Smash’s philosophy: **clear, local, explicit**

---

### Output

Generates a Markdown file like:

```markdown
# 🧠 Smash Context

The `context` object is passed to `run(context)`...

## Project-level context

...

## Smashlet-local context

...

## File types

...

## Example

...
```

---

### Source

The smashlet itself can be hardcoded — no dynamic scanning needed.

Later improvements might:

- Auto-document actual keys used by the project
- Detect presence of `context/` folders
- List `.json` files found in root and smashlet dirs

---

### Verification

- Run the smashlet → creates or updates `docs/context.md`
- Contents should include:
  - Description of `context`
  - Examples of usage
  - Table of supported file types
  - Notes on override behavior

---

### Suggested filename

```
generate_context_docs.md
```

Let me know if you want a companion smashlet that outputs this now.

---

## Add context file support

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

---

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

## Add run command for force

## 📄 `[Core] Add 'smash run' command to force re-running all smashlets`

### What it does

Adds a `run` subcommand to the Smash CLI that forces **all** smashlets to run, regardless of timestamp or skip logic.

Also supports `smash run path/to/smashlet.py` to run a **specific** smashlet.

---

### Why it matters

- Enables manual control when debugging or developing a smashlet
- Avoids needing to modify files or clear runlogs just to re-run logic
- Clear mental model: `smash = smart build`, `smash run = run everything`

---

### CLI Behavior

```bash
# Run only what's changed (default)
smash

# Force all smashlets to run
smash run

# Run a specific smashlet, regardless of input timestamps
smash run content/tasks/smashlet.py
```

---

### Implementation hints

- Add a `run` subcommand to `cli.py`
- In `commands.py`, add a new `run_force()` function:
  - If no path is given → force all smashlets
  - If a path is given → run that one smashlet directly
- Skip `should_run()` and call `run_smashlet()` directly

---

### Verification

- Create a smashlet with unchanged inputs
- Run `smash` → should be skipped
- Run `smash run` → should re-run
- Run `smash run path/to/file.py` → should re-run only that file

---

### Suggested filename

```
add_run_command_for_force.md
```

---

## Centralized logging

## [Core] Add `smash.log()` for consistent logging

### What it does

Adds a centralized logging function (`smash.log()`) to replace all `print()` usage across the CLI and smashlets.

### Why it matters

Standardizes output across Smash. Makes logs easier to style, parse, or redirect — and prepares for future features like timestamps, log levels, or structured output.

### Hints

- Define `log(msg, *, level="info")` in `smash/log.py`
- Expose it via `import smash`
- Replace all internal `print()` calls with `smash.log()`
- Support optional levels: `"info"`, `"warn"`, `"error"`, `"debug"`

### Example

```python
import smash

def run():
    smash.log("Rendering 5 markdown files...")
```

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

## Explicit output tracking

## [Core] Support explicit output file tracking

### What it does

Allows smashlets to define the exact output files they generate, so Smash can use this to determine if the smashlet needs to run.

### Why it matters

Currently, Smash only compares input file mtimes with the smashlet file. Explicit outputs would allow:

- More accurate dependency checking
- Better support for non-globbed outputs
- Future features like cleaning unused files or dry-run diffs

### Hints

- Add an optional `OUTPUT_FILES` or `get_outputs()` in the smashlet
- Compare input mtimes vs output mtimes
- Skip run if all outputs are newer than all inputs

### Example

```python
def get_outputs():
    return [Path("dist/index.html"), Path("dist/summary.json")]
```

---

## Fix smashlet mtime tracking

Here you go — full task story written in your project’s style:

---

## 📄 `[Core] Fix smashlet mtime tracking to avoid false skips during development`

### What it does

Updates how Smash determines whether a smashlet should run by using the **runlog timestamp** instead of relying on the smashlet file’s own `mtime`.

---

### Why it matters

Currently, Smash uses the `mtime` of the smashlet file to decide whether its inputs are “newer.” But during active development, a developer (or LLM) may edit the smashlet file repeatedly — which makes it look like the smashlet is always up-to-date, even though its logic just changed.

This causes confusing behavior:

- Smashlets silently skip when you're trying to test changes
- Developers need to manually touch inputs or delete the runlog
- This breaks the development feedback loop and undermines predictability

---

### Fix strategy

- Track the **last time the smashlet was successfully run** using the existing runlog (already done in `update_runlog`)
- Compare this `last_run` time against:
  - mtime of the smashlet file itself
  - mtimes of matching input files (via `INPUT_GLOB`)
- Rerun if **any** of those are newer than the runlog entry

---

### Pseudocode

```python
last_run = runlog.get(smashlet_path, 0)
needs_rerun = any(
    file.stat().st_mtime > last_run
    for file in [smashlet_file] + input_files
)
```

---

### Side benefits

- Clearer separation between smashlet edit time and execution time
- Works better with future features like dry runs or caching
- Avoids overloading file mtimes as semantic flags

---

### Verification

- Create a smashlet and some inputs
- Edit the smashlet → it should rerun even if inputs are unchanged
- Edit inputs → it should rerun as before
- After rerun, editing neither → it should be skipped

---

### Suggested filename

```
fix_smashlet_mtime_tracking.md
```

Let me know if you want a test case or implementation sketch for this too.

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

## Inject inputs in context

## [Core] Automatically pass glob-matched files to `run()`

### What it does

Automatically resolves `INPUT_GLOB` and provides the matched files to the smashlet via `context["inputs"]`.

### Why it matters

Removes repeated glob logic from every smashlet. Reduces boilerplate and makes smashlets easier to write — especially for LLMs.

### Hints

- Only resolve `INPUT_GLOB` if it's defined
- Inject `context["inputs"]` as a list of `Path` objects before calling `run(context)`
- Works seamlessly with both `run()` and `run(context)`

### Example

```python
def run(context):
    for f in context["inputs"]:
        ...
```

---

## Replace print with log

## [Infra] Replace raw `print()` with `smash.log()`

### What it does

Replaces all direct `print()` calls in Smash core with a centralized `smash.log()` function to standardize output.

### Why it matters

Centralized logging allows:

- Timestamps
- Log levels
- Styled or structured output
- Easier testing, filtering, or redirection

### Hints

- Add `log(msg, level="info")` in `smash/log.py`
- Replace all `print()` in `smash_core/` with `log(...)`
- Future support for flags like `--quiet`, `--debug`

### Example

```python
# Instead of this:
print("✅ Project initialized.")

# Do this:
import smash
smash.log("✅ Project initialized.")
```

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

## Status command

## [Feature] `smash status` command

### What it does

Adds a CLI command that performs a dry run of the build and shows whether each smashlet is up-to-date, will run, or be skipped (with reasons).

### Why it matters

Helps developers understand what Smash is about to do without actually running it. Improves trust, debugging, and automation workflows.

### Hints

- Reuse `should_run()` to determine status
- For each smashlet, print one line:
  - ✅ up-to-date
  - ⚙️ will run
  - ⏳ skipped (timeout)
  - ⚠️ skipped (missing INPUT_GLOB or run())
- Sort by path or timestamp

### Example output

```

⚙️ smashlet_compile.py — will run (inputs changed)
✅ smashlet_index.py — up to date
⏳ smashlet_fetch.py — skipped (timeout not reached)

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
