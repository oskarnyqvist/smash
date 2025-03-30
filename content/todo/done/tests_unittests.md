### Title:

**[Test] Unit test suite for core Smash modules**

### What it does:

Adds a set of **unit tests** for the core logic in `smash_core`, such as `commands.py`, `project.py`, and `smashlets.py`. These tests validate functionality in isolation without relying on subprocesses or file structure.

### Why it matters:

Catches bugs early, ensures core logic works correctly, and allows confident refactoring — especially for logic like runlog tracking, file detection, or smashlet behavior.

### Scope:

- `run_add_smashlet()` in `commands.py`
- `find_project_root()` in `project.py`
- `discover_smashlets()`, `should_run()`, `touch()` in `smashlets.py`
- Mock file structures or use `tmp_path` when needed

### Structure:

- `tests/unit/`
  - `test_commands.py`
  - `test_project.py`
  - `test_smashlets.py`

### Verification:

Run with:

```bash
pytest tests/unit/
```
