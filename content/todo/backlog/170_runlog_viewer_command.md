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
