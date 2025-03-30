## 📄 Guideline: Writing a `README.md` for New Directories

When creating a new folder in Smash (e.g., `content/`, `docs/`, `tools/`), include a `README.md` that explains its **purpose, structure, and usage**.

A good directory README answers the questions:

> 🧠 “Why does this directory exist?”  
> 🗂 “What’s inside it?”  
> 🛠 “How should I use or extend it?”  
> 🤖 “Can an LLM understand and regenerate this?”

---

## ✅ Checklist: What to Include

| Section                     | Purpose                                            |
| --------------------------- | -------------------------------------------------- |
| **1. Purpose**              | Why this directory exists and what it’s for        |
| **2. Structure (visual)**   | Folder tree or code block listing structure        |
| **3. Key Files or Subdirs** | Table or bullet list explaining file roles         |
| **4. How It Works**         | Summary of the logic, flows, or dependencies       |
| **5. How to Extend**        | How to add new files, modules, or functionality    |
| **6. Output (if any)**      | Where generated files go (if this is a source dir) |
| **7. LLM Tips (optional)**  | Anything that helps LLMs reason about the contents |

---

## 📦 Template

Here’s a template you can copy/paste when starting a new `README.md`:

```markdown
# 📁 <directory_name>/

<One-sentence summary of the purpose.>

---

## 📂 Structure
```

<relative_path>/
├── file_1.ext # Short hint
├── subdir/  
│ └── ...  
└── ...

```

---

## 📄 Key Files

| File or Folder     | Purpose                              |
|--------------------|--------------------------------------|
| `file_1.py`        | Entry point or key logic             |
| `subdir/`          | Contains ...                         |
| `README.md`        | You're reading it!                   |

---

## 🛠 How It Works

<Short paragraph on internal logic, build behavior, or relationships.>

---

## ✍️ How to Add New Things

1. Create ...
2. Add ...
3. Use ...
4. Smash will ...

---

## 📚 Outputs

<Where things get written — if relevant. E.g., `docs/`, `dist/`, etc.>

---

## 🤖 Notes for LLMs (optional)

- All logic is colocated
- Files are independent
- File names and roles are predictable
```

---

## 💡 Tip

Keep it **brief but precise**. One sentence of high-context is better than five of vagueness.
