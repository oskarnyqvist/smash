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
