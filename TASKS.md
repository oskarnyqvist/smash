# TASKS

This is the format for writing tasks for Smash. It’s designed to be as effective as possible for both humans and LLMs — no red tape, no filler.

Each task is a markdown file inside the `tasks/` directory. Each file should define **a single task**.

---

## ✅ Task Format

```markdown
## [Category] Title

### What it does
A short, clear description of what the task should implement or change.

### Why it matters
Explain the purpose or benefit of this task — context helps prioritize.

### Hints
(Optional) Tips, edge cases, related functions, or links to look at.
```

---

## 📁 Example: `tasks/status.md`

```markdown
## [Feature] `smash status`

### What it does
Runs a dry scan of all smashlets and prints their run status — up to date, will run, or skipped.

### Why it matters
Helps users understand what Smash is going to do before it builds. Useful for debugging and CI.

### Hints
- Reuse `should_run()`, don’t duplicate logic
- Print one line per smashlet with a status icon
```

---

## 🧠 Guidelines

- Keep it short but specific
- Use one file per task (name it clearly)
- Use `[Feature]`, `[Core]`, `[Test]`, `[Infra]`, etc. as tags
- If unsure, leave off “Hints” — it’s optional

---

## 🧰 Optional Categories

- `[Feature]` — new user-facing capability
- `[Core]` — changes to internals or behavior
- `[Test]` — test coverage or fixtures
- `[Infra]` — CI, packaging, structure
- `[Docs]` — updates to README, examples, templates

---

That’s it. Tasks in this format can be picked up by a person or LLM and completed with minimal clarification.
