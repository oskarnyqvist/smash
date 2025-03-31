# 🔧 Smash Task Workflow Primer

This guide documents the step-by-step workflow we follow when implementing and verifying tasks in the Smash project — whether you’re a developer or an LLM.

It's designed to:

- Keep your headspace focused and tight
- Avoid rework and broken assumptions
- Make each feature addition safe, testable, and clearly explained

This document is your jumpstart checklist for working on new features or fixes in Smash.

---

## ✅ Step 1: Pick and Understand a Task

Start with a task written in the `tasks/` or `content/todo/backlog/` directory. These follow a structured format with:

- **What it does**
- **Why it matters**
- **Hints or examples**

### ✅ Before continuing:

Ask yourself:

- Is the task **atomic** and **clear**?
- Does it align with **Smash’s philosophy**? (Local-first, predictable, LLM-editable)
- Does the example or spec show expected **behavior**?

If it’s unclear — split, refine, or ask before coding.

---

## 🧠 Step 2: Implement the Core Behavior

Start in the core logic first — this usually means modifying a file in `smash_core/` like `smashlets.py`, `project.py`, or `commands.py`.

### Principles:

- Make it **opt-in** unless stated otherwise (don’t break existing smashlets)
- Handle bad input or missing config gracefully
- Keep things **local and deterministic**

### Example pattern:

- Add support for an optional `get_outputs()` function
- Update `should_run()` logic to respect it
- Do **not** write any tests or docs yet — focus on getting the logic correct

Use `print()` or logging if needed to debug behavior interactively before writing tests.

---

## 🧪 Step 3: Add Unit Tests (or Fix Them)

Add a new test (or update an existing one) in `tests/unit/`.

You don’t need to cover every edge case — but confirm the behavior you just built works **end-to-end**, ideally in:

- The happy path ✅
- One or two failure/missing-data scenarios ❌

### Testing conventions:

- Use `tmp_path` + `os.chdir()` to simulate real project dirs
- Smashlets are usually written to disk as `.write_text(""" ... """)`
- Always create `.smash/` when testing `run_smashlet()`

If your feature injects context, builds files, or adds outputs — test that too.

---

## 📚 Step 4: Update the README or Code Comments

If your change affects what users or LLMs need to know:

- Add a new section or subheading in the `README.md`
- Document **what changed**, **how it works**, and any **optional behavior**
- Use tables and examples if helpful

For core files like `smashlets.py`, make sure your function/docstring matches the new behavior and intention.

---

## 💬 Step 5: Write a Clear Git Commit Message

Follow this format:

```
[Type] Summary of the feature or fix

Expanded description of:
- What was added or changed
- Why it matters
- Any notes about optional behavior, fallback, etc.
- Mention of added tests or README updates
```

### Example:

```
[Core] Add support for context.json and context/ injection

Smashlets can now receive structured context from:
- context/ or context.json in the project root
- context/ or context.json next to each smashlet

Files are parsed into context["context"] or left as Path objects in context["context_files"].
Includes full test coverage and new README section.
```

---

## 🧭 Summary Workflow

```
🟢 1. Read and understand the task
🛠 2. Implement the feature in core logic
🧪 3. Add or update tests to confirm behavior
📚 4. Update README.md or inline comments if needed
✅ 5. Write a good commit message and push
```

Stay focused on **one feature at a time**. Keep things local and composable. If you’re working with an LLM, narrate the task, your intent, or what you're unsure about — and move one safe step at a time.

---

Let’s build Smash like it runs: local-first, deterministic, and readable by humans _and_ machines.

---

This file lives to serve you. Update it as the team evolves ✨
