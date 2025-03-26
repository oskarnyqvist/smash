# Smash

Smash is a lightweight build system for content. It uses plain Python to transform and assemble files at the directory level—without global configuration, large dependency graphs, or templating assumptions.

---

## Problem

Many projects involve piecing together content or data: merging JSON fragments, converting Markdown, or generating diagrams from `.dot` files. Commonly, tools like Make or large pipeline frameworks feel too heavy for these tasks, while static site generators focus on web output and layout.

Smash addresses this gap by letting each directory define its own build logic in a simple Python file, keeping transformations localized and easy to maintain.

---

## Why Smash

- **Local Build Logic:** Every directory has a `smashlet.py` that lives alongside the files it processes. There’s no central Makefile or config to keep track of.
- **Plain Python:** No specialized syntax or templates—just Python code. If you can write a script, you can write a smashlet.
- **Iterative Execution:** Smash checks timestamps to see what’s changed, runs the necessary smashlets, and updates their modification times so it won’t rerun them unnecessarily.

---

## Why not Make, Luigi, or Others?

### Make
Powerful for compiling code, but Makefiles can become unintuitive over time. Centralizing logic in one file means understanding one part may require scanning the entire build system. Smash keeps logic distributed, letting you work on a directory without touching everything else.

### Luigi / Airflow
Excellent for orchestrating large pipelines with complex dependencies. However, they’re overkill for small, file-based tasks. Smash handles simpler transformations without imposing scheduling frameworks or DAG concepts.

### Static Site Generators
Ideal if you’re producing a full website with routing and layout. Smash, however, is content-agnostic—it just transforms inputs into outputs without assuming you want HTML or a static site structure.

---

## How Smash Works

1. **Locate smashlets:** Smash scans your project for `smashlet.py` files.  
2. **Determine order:** It sorts them by modification time (oldest first).  
3. **Run and update:** If the input files for a smashlet are newer than the smashlet itself, Smash runs its `run()` function. Then it updates the smashlet’s timestamp.  
4. **Repeat:** The process continues until no further smashlets need to run.

There’s no global configuration or dependency graph: each directory contains the full logic for its own content.

---

## Basic Usage

1. **Initialize** a project:
   ```bash
   smash init
   ```
   This creates a hidden `.smash/` directory, marking the project root.

2. **Add smashlets** wherever you need transformations.  
   Each directory can have a `smashlet.py` describing how to process files.

3. **Build**:
   ```bash
   smash
   ```
   Smash repeatedly runs smashlets until everything is up-to-date.

---

## Smashlet Structure

A `smashlet.py` typically has:

```python
INPUT_GLOB = "*.md"
OUTPUT_DIR = "dist/"

def run():
    from pathlib import Path
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    for f in Path(".").glob(INPUT_GLOB):
        content = f.read_text()
        html = f"<h1>{f.stem}</h1>\\n{content}"
        Path(OUTPUT_DIR, f.with_suffix(".html").name).write_text(html)
```

- **`INPUT_GLOB`** selects input files (e.g., `*.json`, `*.md`).
- **`OUTPUT_DIR`** is where you place your outputs.
- **`run()`** performs the actual transformation. Smash updates the smashlet’s timestamp afterward.

---

## Project Layout Example

```
myproject/
├── .smash/             # Created by 'smash init'
├── content/
│   ├── pages/
│   │   ├── intro.md
│   │   ├── about.md
│   │   └── smashlet.py   # Markdown -> HTML
│   └── data/
│       ├── part1.json
│       ├── part2.json
│       └── smashlet.py   # Merge JSON files
└── smash                # CLI tool
```

---

## Use Cases

- **Assembling documentation** from multiple partial files in Markdown.
- **Generating diagrams** from `.dot` or `.plantuml` files.
- **Localizing content** by merging language-specific data fragments.
- **Preparing data** for APIs, LLM input pipelines, or other downstream tasks.

---

## Philosophy and Contributing

Smash prioritizes simplicity and clarity. Every directory describes its own process independently, avoiding global configuration or forced conventions. A few guiding principles:

- **No central dependency graph**  
- **No single build file**  
- **No assumptions about file formats**  
- **No hidden magic**  

Contributions are welcome—especially for improving edge-case handling, CLI usability, or adding useful helpers for common file transformations.

---

## License

Choose an appropriate license, for example: **MIT**.

