### Helper Functions

Smash includes reusable helpers to reduce boilerplate and promote consistency in smashlets.

Import them with:

```python
from smash import read_text_files, write_output, ensure_dir, flatten_json_dir, smash_log
```

---

### Included Helpers

- `read_text_files(paths)`
  → Reads and returns the content of each file in `paths` as a list of strings.

- `write_output(path, content)`
  → Writes `content` to a file. Creates parent directories if needed.

- `write_output_if_changed(path, content, context)`
  → Writes only if content has changed. Prevents unnecessary rebuilds.

- `ensure_dir(path)`
  → Ensures that a directory exists. Creates it if missing.

- `flatten_json_dir(path)`
  → Reads all `.json` files in a directory and returns a flat dict: `{filename_stem: parsed_json}`

- `smash_log(msg)`
  → Consistent log output for smashlets. Equivalent to `smash.log()`.

---

### Example

```python
from smash import read_text_files, write_output_if_changed

def run(context):
    contents = read_text_files(context["inputs"])
    result = "\n\n---\n\n".join(contents)

    write_output_if_changed("dist/combined.md", result, context)
    return 1
```
