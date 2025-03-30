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
