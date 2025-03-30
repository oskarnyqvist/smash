## [Core] Add default helper functions (`smash.helpers`)

### What it does

Adds a small set of reusable utility functions to `smash.helpers`, available to all smashlets via `from smash.helpers import ...`.

### Why it matters

Encourages consistent, clean patterns in user code. Reduces boilerplate and improves LLM compatibility.

### Hints

Include helpers like:

- `read_text_files(paths)`
- `write_output(path, content)`
- `log_step(msg)` or `smash_log(msg)`
- `flatten_json_dir(path)`
- `ensure_dir(path)`

Helpers should work out of the box and require no project configuration.

### Example usage

```python
from smash.helpers import read_text_files

def run():
    for text in read_text_files(context["inputs"]):
        ...
```
