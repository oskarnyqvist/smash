## 📚 API Layers in Smash

Smash has three distinct API layers — each designed for a specific purpose and audience.

This clear separation makes the system simple to use, safe to extend, and easy to regenerate.

---

### 🟩 1. Public CLI API

> Used from the terminal via commands like `smash build`, `smash add`

This is the main interface for using Smash as a tool. It includes:

- `smash init`
- `smash build`
- `smash add <name>`
- `smash run`
- `smash status`

These commands are implemented internally but form a stable, user-facing interface.

---

### 🟨 2. Public Smashlet API

> Used inside `smashlet_*.py` files via `from smash import ...`

This API is the safe, supported way to write logic inside smashlets.

It includes:

- File I/O: `read`, `write`, `resolve`
- Context-aware output: `write_output`, `write_output_if_changed`
- Logging: `log`, `log_step`
- Helpers: `read_text_files`, `flatten_json_dir`, etc.

Smashlets should **only** import from `smash` — never from `smash_core`.

---

### 🟥 3. Internal Core API

> Used by contributors building or extending Smash itself

Implemented in `smash_core/`, this layer includes:

- CLI command logic (`commands/*.py`)
- Build engine logic (`smashlets.py`, `context_loader.py`)
- Core utilities (`project.py`, `files.py`, `log.py`)

This code is for internal use only — it’s **not part of the public interface** and may change at any time.

---

✅ This separation keeps user code clean and safe,  
🧠 while making the system easy to evolve, debug, and extend.
