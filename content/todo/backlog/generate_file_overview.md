## 📄 `[Docs] Add file overview smashlet to generate docs/files.md`

### What it does

Creates a smashlet that walks the project directory tree and generates a human- and LLM-readable `docs/files.md`. Each file is listed with a brief purpose or hint, allowing fast onboarding and exploration.

---

### Why it matters

- Makes it easy to understand the project structure at a glance
- Helps LLMs identify the right file to read or edit
- Aids contributors in locating logic, smashlets, tests, or docs
- Improves transparency and discoverability for unfamiliar users

---

### Output

```markdown
# 🗂 File Overview

## smash_core/

- `cli.py` – CLI entry point with subcommands
- `commands.py` – High-level build/init logic
- `project.py` – Runlog + project root detection

## content/todo/backlog/

- `status_command.md` – Add `smash status` to show run state
  ...
```

---

### How it works

- Walk the project using `Path().rglob("*")`
- Filter out `__pycache__`, `.git`, `*.pyc`, etc.
- For each `.py` or `.md` file, grab the first comment or heading
- Render results grouped by directory, alphabetically

---

### Considerations

- Could optionally support `docs/files.html` for rendered output
- Could be run automatically as part of `smash build`
- Can pull file hints from the first comment block or markdown title

---

### Verification

- Run smashlet → `docs/files.md` should appear
- Should include every `.py`, `.md`, `.toml`, `.cfg`, etc.
- Each file should include a short purpose/hint if possible

---

### Suggested filename

```
generate_file_overview.md
```
