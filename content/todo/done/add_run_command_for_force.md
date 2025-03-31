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
