# ✅ TASK STORY: Add `should_run(context)` override for smashlets

## 📌 What are we changing or introducing?

We're adding support for **custom run condition logic** inside individual smashlets by allowing them to define a `should_run(context)` function.

If present, this function takes precedence over the default timestamp/input/output/runlog comparison logic.

Add extra context to should_run(context),
context["last_run"] # timestamp (float) from runlog
context["smashlet_mtime"] # float: mtime of the smashlet file itself
context["latest_input_mtime"] # latest mtime among input files
Or something similar.

---

## ❓ Why does it matter — what pain is it solving?

Right now, all smashlets rely on automatic rules to determine when to run. This works well for simple cases, but breaks down in edge cases like:

- Rebuilds triggered by _external_ data not tracked as inputs
- Complex domain logic (e.g. “only run on Mondays” or “skip if DB already has rows”)
- Conditional rebuilds that depend on environment, auth, API responses, etc.

By giving smashlets the ability to define their own `should_run(context)` logic, we:

- Increase **flexibility** without increasing **complexity** for most users
- Stay true to Smash’s **colocated logic** and **Python over config** philosophy
- Let power users manage their own invalidation strategy in a fully opt-in way

---

## 🧱 What’s the best interface or design?

- If a smashlet defines a top-level function called `should_run(context)`, Smash will call it instead of using the default mtime/runlog logic.
- If the function raises an error, Smash logs a warning and skips that smashlet.
- This is entirely optional — most users won’t need it.

Example:

```python
def should_run(context):
    return datetime.today().weekday() == 0  # Only run on Mondays
```

---

## ✅ How will this be validated or tested?

- Add a test to `tests/unit/test_smashlets.py` for a smashlet that defines `should_run(context)`
- Assert that it runs or skips based on its logic
- Add one test for a broken `should_run(context)` that throws an exception and verify it logs a warning and skips the smashlet
- Also test fallback behavior when `should_run()` is not defined

---

## 🌱 Does this fit Smash’s core philosophy?

Yes, perfectly:

- **Local-first:** logic lives in the smashlet itself
- **Predictable:** users opt into full control; fallback remains unchanged
- **Python-native:** no new config DSL or YAML-based rule sets
- **Minimal magic:** clear interface, no hidden hooks

---

## 🧪 Could it break anything? Is it backward compatible?

- Fully backward-compatible: existing smashlets are unaffected
- Only triggered if `should_run()` is defined
- Existing logic remains the fallback

---

## 🧭 Final Checklist

- [x] Clear and actionable?
- [x] Scoped and atomic?
- [x] Aligns with Smash architecture and values?
- [x] Includes test plan?
- [x] Resilient to failure modes?

✅ **Ready to implement in a single focused commit.**
