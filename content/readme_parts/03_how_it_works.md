### How Smash Works

Smash scans your project for `smashlet_*.py` files. Each one defines a local transformation: which files to process, and how.

A smashlet declares:

- `INPUT_GLOB`: which files to match (e.g. `"*.md"`)
- `OUTPUT_DIR`: where to write results
- `run()` or `run(context)`: a function that does the work

Smash runs all smashlets in modification time order (oldest first). If any outputs change, it loops again — until everything is up to date.

Each smashlet is isolated. No global config. No dependency graph. No magic.
