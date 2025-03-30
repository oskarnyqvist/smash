## ✅ Cleaned Up Version of `content/README.md`

```markdown
# 🧱 content/

This folder contains the **structured source files** for generating documentation using Smash.

Smashlets in this folder transform local content into markdown files written to `docs/`.

---

## 📂 Structure
```

content/
└── todo/
├── backlog/ # Story and task candidates
├── done/ # Completed stories
├── to_be_created.md # Brain dump / vague ideas
└── smashlet.py # Generates docs/TODO.md

```

---

## 📄 Files you’ll find here

| Path                        | Purpose                                      |
|-----------------------------|----------------------------------------------|
| `backlog/*.md`              | Stories, features, improvements, fixes       |
| `done/*.md`                 | Tasks that have been implemented             |
| `to_be_created.md`          | Brainstorm dump or unstructured backlog      |
| `smashlet.py`               | Renders `docs/TODO.md` from backlog          |

---

## 🧠 Why it's structured this way

- All content lives **next to the smashlet** that renders it
- Smashlets define their own transformation logic
- Output paths are always relative: `../../docs/*.md`

This keeps docs **local, predictable, and editable by LLMs**.

---

## ✍️ How to add a new doc

1. Create a new folder under `content/`
2. Add markdown files as needed
3. Add a `smashlet.py` with:
   - `INPUT_GLOB` to match your source files
   - `OUTPUT_DIR = "../../docs"`
   - A `run(context)` function that writes the output

Smash will discover and run the smashlet automatically.

---

## 📦 Example

```

content/context/
├── context_docs.md
└── smashlet.py # → writes docs/context.md

```

---

## 📚 Output Location

All generated files are written to:

```

/docs/

```

This folder is the final destination for all documentation outputs.

```
