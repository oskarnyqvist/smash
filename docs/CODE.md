# Smash Code Guidelines

## Purpose & Style

These guidelines are designed to help both **developers and LLMs** understand and modify Smash code confidently.

Smash is not just for humans — it's built to be safe for automation. That means:

- Minimal, local, and predictable code
- Reasonable defaults and naming
- Structure that allows any file to be understood and rewritten in isolation

## These guidelines do **not** repeat generic Python best practices. Instead, they capture what’s special about **how Smash works**, and how to contribute to it without breaking that simplicity.

## 🔍 Working on a Task?

Before starting any implementation, review the [Task Analysis Protocol](STORY_CHECKLIST.md).

This checklist helps both humans and LLMs:

- Evaluate whether a task is clear, scoped, and aligned
- Decide whether to continue, refine, split, or reject
- Prevent wasted effort on vague or broken specs

→ [See STORY_CHECKLIST.md 🧭](STORY_CHECKLIST.md)

---

## 1. Project Principles

Smash is built to be:

- 🧱 **Local**: logic lives next to the files it transforms
- ✨ **Predictable**: no hidden magic, no dynamic registries
- 🤖 **LLM-friendly**: files are self-contained and regenerable
- ⚡ **Fast**: clear skip logic, short feedback loops

These values guide how we write code, comments, and structure.

---

## 2. Smashlet File Conventions

Smashlets are the units of transformation in a Smash project.

### ✅ Supported file patterns

Smash discovers any file named:

- `smashlet.py` — the classic default
- `smashlet_<name>.py` — for multiple steps per directory

Each file must define:

- `INPUT_GLOB` — selects inputs relative to the smashlet’s dir
- `OUTPUT_DIR` — where to put results
- `run()` — function that performs the transformation

Smash treats each file as an isolated unit:

- They are executed independently
- Tracked separately in the runlog
- Sorted and run by modification time (oldest first)

---

## 3. Commenting & Documentation

Smash files are written for **humans and LLMs** to understand and regenerate. Focus on:

- Explaining _intent_, not syntax
- Keeping each file self-contained
- Making the “why” behind decisions obvious

### 🧱 File-Level Header

Every core file should start with a 2-3 line block explaining its role.

**Example:**

```python
# smashlets.py
#
# Responsible for discovering, loading, and executing `smashlet_*.py` files.
# Supports multiple smashlets per directory.
```

### 🔧 Function-Level Docstrings

Every public function (especially in core Smash logic) should include:

- What it does
- Why it exists
- What inputs/outputs it expects

**Good example:**

```python
def update_runlog(project_root, smashlet_path):
    """
    Update the runlog with the current timestamp for a given smashlet.

    This function is called after a smashlet has been successfully run.
    """
```

No need to repeat obvious code — just explain the reasoning.

### 💬 Inline Comments

Use them where logic might be misunderstood or not immediately obvious. Prioritize “why” over “what”.

✅ Good:

```python
# Skip if timeout hasn’t passed since last run
```

❌ Bad:

```python
# Add 1 to counter
counter += 1
```

---

## 4. Naming & Structure

### 📄 Smashlet file names

Use `smashlet_<name>.py` to organize related transformations.  
Avoid generic names like `process.py`, `build.py`, etc.

Good:

```plaintext
smashlet_render.py
smashlet_embed.py
smashlet_tokenize.py
```

Bad:

```plaintext
do_things.py
pipeline.py
```

### 📦 Core project files

These power the Smash CLI:

- `cli.py` — entry point and CLI argument parsing
- `commands.py` — high-level logic for `smash init`, `smash`
- `project.py` — handles runlog and project root detection
- `smashlets.py` — discovers and runs smashlets

Keep logic grouped by behavior, not by abstraction layer.

---

## 5. Constants and Magic Values

Use named constants to avoid magic numbers and improve clarity — especially around timing, run modes, or config.

✅ Good:

```python
time.sleep(ONE_MINUTE)
```

❌ Bad:

```python
time.sleep(60)
```

Put constants at the top of the module. Keep them near usage context unless they’re shared across files.

---

## 6. LLM-Friendliness Checklist

Smash is designed to be safely edited by language models. This means each file should:

- ✅ Start with a clear file-level comment
- ✅ Define any transformation logic inline
- ✅ Avoid unnecessary imports or indirection
- ✅ Include docstrings for all public functions
- ✅ Use consistent terminology (`smashlet`, `runlog`, `context`, etc.)
- ✅ Not assume global state or config
- ✅ Be able to run in isolation with just `smashlet_<name>.py`

If any of the above is missing, the file should be flagged for documentation or structure improvement.

---

## 7. Context Handling

Smashlets can accept a `context` dictionary, which is injected when calling `run(context)`.

Context includes:

- `cwd`: Path to the smashlet’s directory
- `project_root`: Root path of the project
- `config`: From `smash.py` (if defined)
- Any additional fields added by `on_context(context)` in `smash.py`

When writing smashlets or helpers, always prefer pulling from `context` instead of hardcoding paths or values.

---

## 8. `smash.py` Conventions

This optional file at the project root can define:

- `config = {...}` — injected into `context["config"]`
- `on_context(context)` — used to mutate context before build
- Helper functions — importable from smashlets

**Example:**

```python
# smash.py

def on_context(context):
    context["locale"] = "sv-SE"
    return context

def read_yaml(path):
    import yaml
    return yaml.safe_load(path.read_text())
```

Smashlets can safely import this:

```python
from smash import read_yaml
```

---

## 9. `smash` vs `smash_core` — Public API vs Internals

Smash uses a clear split between public and internal code:

- `smash_core/` → internal logic (not for direct use in smashlets)
- `smash/` → public API that your smashlets should import from

### ✅ Always import from `smash`

If you're writing a smashlet or example code, use:

```python
from smash import read, write, resolve
```

This keeps the code portable, stable, and independent of internal structure.

### ❌ Don't import from `smash_core`

Even though helpers like `files.py` live in `smash_core/`, they are **exposed through** `smash/` for safe usage.

This design prevents breakage if internal modules move or change — and keeps smashlets friendly to LLMs and humans alike.

## Summary

- One file = one transformation unit
- Prefer `smashlet_<name>.py` for complex directories
- Keep logic local and obvious
- Document intention, not implementation
- Help LLMs and devs reason about what they see — and rewrite it safely

Clarity isn't just for maintainability.  
It's what makes automation possible.
