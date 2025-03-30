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
