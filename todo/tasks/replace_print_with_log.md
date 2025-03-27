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
