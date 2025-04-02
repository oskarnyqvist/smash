### Basic Usage

Initialize a new project:

```bash
smash init
```

This creates a `.smash/` directory in your project root.

Add a smashlet:

```bash
touch content/smashlet_render.py
```

Run the build:

```bash
smash
```

Smash finds all `smashlet*.py` files, runs them in modification time order, and repeats until nothing changes.

---

### 🛠 Re-running Smashlets

By default, Smash skips smashlets that haven’t changed.

Use `smash run` to override this:

```bash
# Run all smashlets, even if unchanged
smash run

# Run just one smashlet
smash run content/smashlet_render.py
```

Useful when:

- Debugging
- Reprocessing all outputs
- Forcing rebuilds without changing inputs

Builds are deterministic: no DAGs, no surprises.
