## 📄 `[Infra] Add script for deploying Smash to PyPI`

### What it does

Adds a simple, reproducible script that builds and uploads the current version of Smash to [PyPI](https://pypi.org/), making it installable via `pip install smash`.

---

### Why it matters

- Simplifies publishing new versions
- Makes versioning and releases consistent
- Encourages safer, repeatable releases
- Allows LLMs (and humans) to trace version history more easily

---

### What to include

✅ A script like `scripts/publish.sh`:

```bash
#!/bin/bash
set -e

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python3 -m build

# Upload to PyPI (requires `twine`)
twine upload dist/*
```

✅ Optionally add `scripts/publish_test.sh` for TestPyPI.

---

### Requirements

Make sure these are added to `dev-dependencies` (e.g., in `pyproject.toml` or `requirements-dev.txt`):

```toml
[tool.poetry.dev-dependencies]
build = "*"
twine = "*"
```

Or for pip-based workflows:

```
pip install build twine
```

---

### Verification

Run:

```bash
./scripts/publish.sh
```

You should see:

- A wheel + tarball in `dist/`
- Upload success message from Twine

---
