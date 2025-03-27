## add_default_helpers – Add default helpers

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

## add_smashlet_command – Add smashlet command

## 12. [Story] smash add: Create a new smashlet

Description
As a developer, I want to scaffold a new smashlet\_<name>.py file using a CLI command, so I can get started quickly without copy-pasting boilerplate.

Acceptance Criteria

smash add <name> creates a file like smashlet\_<name>.py in the current directory.

The file includes boilerplate: INPUT_GLOB, OUTPUT_DIR, and a stub run() function.

Optional flags for:

--glob "\*.md"

--output "dist/"

--context (if the user wants to pass context)

Prevents overwriting existing files.

Verification

Run smash add render → file created with expected contents.

Confirm contents and structure match expectations.

---

## basic_test_suite – Basic test suite

## [Test] Basic test suite for Smash

### What it does

Creates a minimal test suite to validate core Smash functionality using `pytest`.

### Why it matters

Ensures stability as Smash evolves. Makes it easier to refactor, extend, or onboard new contributors with confidence.

### Hints

Include tests for:

- `smash init` creates `.smash/`
- Detection of `smashlet.py` and `smashlet_*.py`
- Iterative build logic (runs until stable)
- `RUN = "always"` + timeout behavior
- Loading and using `smash.py` (`config`, `on_context()`)

Test structure should go under a top-level `tests/` folder.

### Verification

Run tests via:

```bash
pytest tests/
```

---

## centralized_logging – Centralized logging

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

## context_folder_support – Context folder support

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

## explicit_output_tracking – Explicit output tracking

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

## inject_inputs_in_context – Inject inputs in context

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

## replace_print_with_log – Replace print with log

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

## runlog_viewer_command – Runlog viewer command

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

## status_command – Status command

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
