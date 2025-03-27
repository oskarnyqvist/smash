## [Core] Support `context/` folder injection

### What it does

Adds support for a `context/` folder at the project root. All files inside are made available in the smashlet `context`.

### Why it matters

Allows colocated config, prompts, or metadata to be used in smashlets or `smash.py`. Useful for LLM workflows, reusable configs, and automation.

### Hints

- Inject files as `context["context_files"]`
  - Keys = filenames (e.g. `"config.json"`)
  - Values = `Path` objects or content (e.g. `str`, `dict`)
- Hook into this from `on_context()` if needed
- Add helper in `smash.py` to access these easily

### Example

```python
config = json.loads(context["context_files"]["config.json"].read_text())
```
