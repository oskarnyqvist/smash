## [Core] Automatically pass glob-matched files to `run()`

### What it does

Automatically resolves `INPUT_GLOB` and provides the matched files to the smashlet via `context["inputs"]`.

### Why it matters

Removes repeated glob logic from every smashlet. Reduces boilerplate and makes smashlets easier to write — especially for LLMs.

### Hints

- Only resolve `INPUT_GLOB` if it's defined
- Inject `context["inputs"]` as a list of `Path` objects before calling `run(context)`
- Works seamlessly with both `run()` and `run(context)`

### Example

```python
def run(context):
    for f in context["inputs"]:
        ...
```
