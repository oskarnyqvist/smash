## [Feature] `smash add` command

### What it does
Adds a CLI command to scaffold a new `smashlet_<name>.py` file with boilerplate: `INPUT_GLOB`, `OUTPUT_DIR`, and `run()`.

### Why it matters
Avoids copy-paste, encourages consistency, and speeds up onboarding for both developers and LLMs.

### Hints
- `smash add render` → creates `smashlet_render.py`
- Should support optional flags:
  - `--glob "*.md"`
  - `--output "dist/"`
  - `--context` (generate `run(context)` instead of `run()`)
- Prevent overwriting if file exists
