## [Core] Support explicit output file tracking

### What it does

Allows smashlets to define the exact output files they generate, so Smash can use this to determine if the smashlet needs to run.

### Why it matters

Currently, Smash only compares input file mtimes with the smashlet file. Explicit outputs would allow:

- More accurate dependency checking
- Better support for non-globbed outputs
- Future features like cleaning unused files or dry-run diffs

### Hints

- Add an optional `OUTPUT_FILES` or `get_outputs()` in the smashlet
- Compare input mtimes vs output mtimes
- Skip run if all outputs are newer than all inputs

### Example

```python
def get_outputs():
    return [Path("dist/index.html"), Path("dist/summary.json")]
```
