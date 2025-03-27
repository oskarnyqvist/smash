## [Core] Add `smash.log()` for consistent logging

### What it does

Adds a centralized logging function (`smash.log()`) to replace all `print()` usage across the CLI and smashlets.

### Why it matters

Standardizes output across Smash. Makes logs easier to style, parse, or redirect — and prepares for future features like timestamps, log levels, or structured output.

### Hints

- Define `log(msg, *, level="info")` in `smash/log.py`
- Expose it via `import smash`
- Replace all internal `print()` calls with `smash.log()`
- Support optional levels: `"info"`, `"warn"`, `"error"`, `"debug"`

### Example

```python
import smash

def run():
    smash.log("Rendering 5 markdown files...")
```
