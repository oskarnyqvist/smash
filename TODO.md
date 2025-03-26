## 1. [Story] Create a Python Package Structure

**Description**  
As a developer, I want the Smash codebase to be structured as a Python package so that it can be installed from PyPI.

**Acceptance Criteria**

- A `setup.py` or `pyproject.toml` is present.
- The package is named `smash-cli` (or similar) and can be installed locally with `pip install .`.
- A basic folder structure (`smash/`, `tests/`, etc.) is set up.

**Verification**

- Run `pip install -e .` (editable install) in a virtual environment, confirm `import smash` succeeds.

---

## 2. [Task] Define `smash` CLI Entry Point

**Description**  
As a developer, I want a console script named `smash` so users can run it from the command line after installing.

**Acceptance Criteria**

- The package’s `setup.py` or `pyproject.toml` has an `entry_points` section for a `smash` console script.
- Running `smash` in a terminal displays a help message or usage info.

**Verification**

- After installing, type `smash --help` → usage/help is displayed.

---

## 3. [Story] Implement `smash init`

**Description**  
As a user, I want to initialize a new Smash project so that `.smash/` is created and recognized as the project root.

**Acceptance Criteria**

- Running `smash init` in an empty directory creates a `.smash/` folder.
- If `.smash/` already exists, `smash init` does nothing or prints a warning.
- `smash init` does not overwrite existing files in `.smash/`.

**Verification**

- `ls -a` shows `.smash/`.
- Rerunning `smash init` does not corrupt existing content.

---

## 4. [Story] Implement Smashlet Discovery & Iterative Build

**Description**  
As a user, I want Smash to find `smashlet.py` files recursively, determine which need to run, and iterate until no further changes are detected.

**Acceptance Criteria**

- On `smash` command, code scans all subfolders for `smashlet.py`.
- Sort them by file modification time (oldest first).
- Compare each smashlet’s `INPUT_GLOB` with the smashlet’s own mtime.
  - If any input file is newer, run its `run()` function.
  - Then update the smashlet’s timestamp.
- Repeat until no smashlet runs.

**Verification**

- Test with a folder containing multiple smashlets:
  1. Changing input files triggers a re-run.
  2. Unchanged input does not trigger repeated runs.
  3. The iteration stops in a stable state.

---

## 5. [Task] Add `INPUT_GLOB`, `OUTPUT_DIR`, and `run()` Conventions

**Description**  
As a developer, I need to enforce or read the variables `INPUT_GLOB`, `OUTPUT_DIR`, and the `run()` function in each smashlet.

**Acceptance Criteria**

- In each `smashlet.py`, `INPUT_GLOB` (string) and `OUTPUT_DIR` (string) are optional but recognized if present.
- `run()` is mandatory; if missing, ignore that smashlet or raise a warning.
- The code reads these attributes/variables using Python introspection or `importlib`.

**Verification**

- Smash can load a smashlet that has these attributes and a `run()` function without error.
- If missing `run()`, either skip or raise a user-friendly message.

---

## 6. [Story] Support `RUN = \"always\"` Logic

**Description**  
As a user, I need to mark certain smashlets as “always-run” so they run once per `smash` invocation even without local input files.

**Acceptance Criteria**

- If `RUN = \"always\"` is present in the smashlet, it runs exactly once per `smash` command.
- Implement optional `RUN_TIMEOUT` in seconds, preventing re-runs if the last run is too recent (to avoid infinite loops).
- `run()` can return `0` if nothing changed or `1` if it changed output. If `1`, the system does another pass.

**Verification**

- A test smashlet with `RUN = \"always\"` runs each time `smash` is invoked.
- If `RUN_TIMEOUT = 3600`, calling `smash` twice within an hour doesn’t re-run that smashlet.

---

## 7. [Story] Provide `context` to `run(context)`

**Description**  
As a developer, I want each `run()` function to optionally receive a context dictionary with project info, CLI args, etc.

**Acceptance Criteria**

- A default `context` is constructed when Smash starts.
- `run(context)` is called if the smashlet has a matching signature; otherwise call `run()`.
- `context` includes:
  - `cwd` (Path to the smashlet’s directory)
  - `project_root`
  - Possibly `cli_args` or a config map if we have those implemented

**Verification**

- A test smashlet that prints `context["cwd"]` shows the correct path.
- No error if a smashlet lacks `run(context)` and just has `run()`.

---

## 8. [Epic] `smash.py` Root-Level Module

### 8a. [Story] Load `smash.py` if present

**Description**  
As a developer, I want Smash to look for a `smash.py` in the project root, load it, and optionally apply its `config` and `on_context()` hook.

**Acceptance Criteria**

- If `smash.py` is present, import it.
- If `config` is defined, pass that into `context["config"]`.
- If `on_context(context)` is defined, call it to finalize the context before running smashlets.

**Verification**

- A test with `smash.py` that prints a message on import runs successfully.
- `context["config"]` is set if `config` is in `smash.py`.

### 8b. [Task] Allow smashlets to `import smash`

**Description**  
As a developer, I want smashlets to import functions from `smash.py` at the project root, e.g. `from smash import my_helper`.

**Acceptance Criteria**

- The root `smash.py` is recognized as a module named `smash`.
- The user can define e.g. `def my_helper(): ...` and import it in their smashlets.
- If `smash.py` is missing, it’s simply not importable.

**Verification**

- A smashlet that does `from smash import my_helper` can successfully call `my_helper()`.

---

## 9. [Story] Packaging and Publishing to PyPI

**Description**  
As a maintainer, I want to publish Smash to PyPI so users can install it via `pip install smash-cli`.

**Acceptance Criteria**

- The `version` is set in `pyproject.toml` or `setup.py`.
- A valid `twine upload` or GitHub Actions workflow can publish the package to TestPyPI or real PyPI.
- The README and license are included in the distribution.

**Verification**

- `pip install smash-cli` (from TestPyPI) succeeds and installs the console script.
- `smash --help` works after install.

---

## 10. [Story] Basic Test Suite

**Description**  
As a developer, I want a minimal automated test suite to verify each major feature of Smash.

**Acceptance Criteria**

- Use `pytest` or similar framework.
- Tests for:
  - `smash init`
  - detection of `smashlet.py`
  - the iterative build logic (timestamps)
  - always-run smashlets
  - `smash.py` import
- All tests pass with `pytest`.

**Verification**

- CI or local environment: `pytest tests/` → all green.

---

## 11. [Story] Documentation & Examples

**Description**  
As a user, I want examples that match the README to guide me in typical use cases.

**Acceptance Criteria**

- An `examples/` folder or section with at least two scenarios (e.g., “Markdown -> HTML,” “Merging JSON,” “Always-run for downloads”).
- The README references these examples.

**Verification**

- Each example is self-contained and can be run with `smash` to demonstrate the feature.
