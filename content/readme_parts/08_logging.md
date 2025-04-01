### Logging from Smashlets

Use `smash.log()` for consistent, structured output instead of `print()`:

```python
import smash

def run():
    smash.log("Rendering markdown files...")
```

You can specify a log level:

```python
smash.log("Missing input file", level="warn")
smash.log("Build failed", level="error")
```

Supported levels:

- `"info"` (default)
- `"warn"`
- `"error"`
- `"debug"`

Logs are uniform across all smashlets and can support future features like timestamps, filtering, or redirection.
