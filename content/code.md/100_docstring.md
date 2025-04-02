## 🧾 Docstring Standard (for Humans & LLMs)

Smash uses short, structured, **natural-language docstrings** to make each file understandable in isolation — for developers, contributors, and language models.

File-level docstrings are especially important because they power the auto-generated `FILES.md`, and guide both **code understanding** and **automated reasoning**.

### ✅ Goals

- Help a reader (or LLM) quickly understand:
  - What the file does
  - How it fits into the system
  - Whether it's public-facing or internal
- Keep docs brief but dense — **2–4 lines max**
- Use plain English, not YAML-style metadata

---

### 📁 File-Level Docstrings

Start each `.py` file with a short natural-language summary.

**Structure:**

```python
"""
[What this file does — 1 line]

[How or where it's used — 1 line]

[Optional: Clarifies public/private, special patterns, or key relationships]
"""
```

#### ✅ Examples

**Internal CLI logic:**

```python
"""
Implements the `smash add` command for generating new smashlet files from templates.

Used by the public CLI. Supports multiple templates like 'default', 'minimal', and 'pandas'.
"""
```

**Public API module:**

```python
"""
Provides path-safe `read`, `write`, and `resolve` functions for use in smashlets.

These helpers resolve paths relative to `context["cwd"]` and are exposed via `from smash import ...`.
"""
```

**Internal core logic:**

```python
"""
Handles project-level state, including root detection and the runlog.

Used internally by the build system. Not part of the public API.
"""
```

---

### 🔧 Function-Level Docstrings

Use **only where helpful**, especially for public functions or anything with non-obvious behavior.

Focus on:

- What the function does
- Why it exists (if it’s not obvious)
- Any side effects (e.g. writes files, modifies context)
- Don't repeat obvious things (e.g., “adds 1 to counter”)

**Example:**

```python
def update_runlog(project_root, smashlet_path):
    """
    Record the current timestamp for a successfully executed smashlet.

    Called after `run()` completes. Writes back to `.smash/runlog.json`.
    """
```

---

### 🧪 Test File Docstrings

Each test module should start with a comment or docstring describing:

- What functionality is being tested
- Any notable behaviors, edge cases, or features covered

**Example:**

```python
"""
Tests core smashlet behavior: discovery, execution, context injection, and run conditions.

Covers `should_run()`, `run_smashlet()`, `INPUT_GLOB`, output tracking, and context merging.
"""
```

---

### 🧠 Tips for LLM-Friendly Structure

- Use plain, consistent phrasing — avoid custom formats or excessive abstraction
- Prefer “what + why” explanations over code-like syntax
- Be clear about public vs internal files:
  - Public smashlet API: `from smash import ...`
  - CLI: `smash <command>`
  - Internal: `smash_core/`, not user-facing
