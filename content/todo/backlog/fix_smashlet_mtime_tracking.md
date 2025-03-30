Here you go — full task story written in your project’s style:

---

## 📄 `[Core] Fix smashlet mtime tracking to avoid false skips during development`

### What it does

Updates how Smash determines whether a smashlet should run by using the **runlog timestamp** instead of relying on the smashlet file’s own `mtime`.

---

### Why it matters

Currently, Smash uses the `mtime` of the smashlet file to decide whether its inputs are “newer.” But during active development, a developer (or LLM) may edit the smashlet file repeatedly — which makes it look like the smashlet is always up-to-date, even though its logic just changed.

This causes confusing behavior:

- Smashlets silently skip when you're trying to test changes
- Developers need to manually touch inputs or delete the runlog
- This breaks the development feedback loop and undermines predictability

---

### Fix strategy

- Track the **last time the smashlet was successfully run** using the existing runlog (already done in `update_runlog`)
- Compare this `last_run` time against:
  - mtime of the smashlet file itself
  - mtimes of matching input files (via `INPUT_GLOB`)
- Rerun if **any** of those are newer than the runlog entry

---

### Pseudocode

```python
last_run = runlog.get(smashlet_path, 0)
needs_rerun = any(
    file.stat().st_mtime > last_run
    for file in [smashlet_file] + input_files
)
```

---

### Side benefits

- Clearer separation between smashlet edit time and execution time
- Works better with future features like dry runs or caching
- Avoids overloading file mtimes as semantic flags

---

### Verification

- Create a smashlet and some inputs
- Edit the smashlet → it should rerun even if inputs are unchanged
- Edit inputs → it should rerun as before
- After rerun, editing neither → it should be skipped

---

### Suggested filename

```
fix_smashlet_mtime_tracking.md
```

Let me know if you want a test case or implementation sketch for this too.
