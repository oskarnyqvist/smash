# Smash

Smash is a build system for content. It enables you to define, using plain Python, how files in each directory should be transformed into outputs—without requiring global configuration, dependency graphs, or custom formats.

Each directory includes a `smashlet.py` file that specifies how files within that directory are processed. Smash automatically discovers and runs these smashlets.

---

### Why Smash?

Make is powerful but often unintuitive. A distributed approach lets you understand individual parts of the system without needing to read and comprehend the entire build.

Workflow engines like Luigi or Airflow excel at orchestrating complex pipelines. Smash takes a simpler, directory-based approach that doesn't rely on global scheduling or dependency management.

Static site generators primarily target websites and often enforce templating or layout assumptions. Smash focuses purely on transforming and assembling content and data, free from layout or templating constraints.

Smash is useful when you prefer to colocate build logic alongside the files it operates on—using plain Python, without central configuration or intricate dependency tracking.

---

### How it Works

Smash locates `smashlet.py` files within your project's directories. Each smashlet defines how the files in its own directory are transformed.

A `smashlet.py` contains:

- `INPUT_GLOB`: a glob pattern specifying input files (e.g., `"*.md"`)
- `OUTPUT_DIR`: the directory where output files are placed
- `run()`: a Python function that performs the file transformation

Smash traverses the project directories, finds all smashlets, and executes them in order based on their modification times (oldest first). After executing a smashlet, Smash automatically updates its timestamp. This process repeats until all smashlets are up-to-date.

Each smashlet operates independently. There is no central build configuration or dependency graph—every smashlet contains the entirety of the information it requires.

---

### Basic Usage

Initialize a new Smash project:

```bash
smash init
```

This command creates a `.smash/` directory, marking the root of your project.

Add a `smashlet.py` file in each directory you want to define transformations.

Run Smash:

```bash
smash
```

Smash searches for all `smashlet.py` files from the project root, sorts them by modification time, and executes them in sequence. If any smashlet runs, the process repeats until no further transformations are needed.

---

### Smashlet Structure

A `smashlet.py` file defines how files in its directory should be processed. The structure is straightforward:

- `INPUT_GLOB`: selects input files using glob patterns
- `OUTPUT_DIR`: specifies where output files will be stored
- `run()`: defines the transformation logic

Example:

```python
INPUT_GLOB = "*.md"
OUTPUT_DIR = "dist/"

def run():
    from pathlib import Path

    inputs = list(Path(".").glob(INPUT_GLOB))
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    for f in inputs:
        content = f.read_text()
        html = f"<h1>{f.stem}</h1>\n<p>{content}</p>"

        out_path = Path(OUTPUT_DIR) / f.with_suffix(".html").name
        out_path.write_text(html)
```

Smash determines if a smashlet should run by comparing the modification times of its input files to the smashlet itself. After the `run()` function completes, Smash updates the smashlet's timestamp automatically.

---

### Project Layout Example

```
myproject/
├── .smash/                  # Created by `smash init`
├── content/
│   ├── pages/
│   │   ├── 001.md
│   │   ├── 002.md
│   │   └── smashlet.py      # Transforms .md files into HTML
│   └── data/
│       ├── part1.json
│       ├── part2.json
│       └── smashlet.py      # Combines JSON files
└── smash                    # CLI executable
```

Each directory with a `smashlet.py` independently defines its transformation logic. Smash identifies and executes these smashlets automatically.

---

### Use Cases

Smash is designed for structured content workflows where build logic benefits from colocation with the content itself. Common scenarios include:

- Generating structured documentation from multiple source fragments
- Rendering diagrams from `.dot` or `.plantuml` files stored across directories
- Merging content files into language-specific or region-specific outputs
- Creating structured data files for API endpoints or LLM input pipelines

---

### Contributing and Philosophy

Smash prioritizes simplicity and clarity. Every directory describes its own build logic independently, eliminating reliance on global configuration or shared state.

Key principles:

- No central dependency management
- No global build configuration
- No assumptions about content structure or output
- No enforced metadata formats or naming conventions

Contributions are welcome, particularly improvements to CLI usability, handling of edge cases, and reusable utilities for common transformations.

---

### License

MIT

