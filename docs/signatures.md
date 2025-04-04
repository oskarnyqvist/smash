# 🔍 Function Signatures

This document is automatically generated from the Python source code in `smash_core/`.

It shows the **top-level public functions** for each file, along with:

- 🧾 Function signature (name, parameters, return type)
- 📘 Top 3 lines of the docstring (if present)
- 📏 Line count
- 🧠 Static complexity metrics:
  - Branches (`if` / `else`)
  - Loops (`for` / `while`)
  - Calls (other functions used)
  - Local variables (assignments)
  - Nesting depth
- ✅ Type hint usage

Functions starting with `_` are excluded by default.

This reference helps:

- Developers discover available helpers and APIs
- LLMs understand callable building blocks
- Contributors identify large, undocumented, or complex code

## smash_core/cli.py

```python
def main()
# Smash CLI dispatcher.
# Commands:
# smash init         → Initialize a new Smash project
# Lines: 53
# Type hints: ❌
# Branches: 5 | Loops: 0 | Returns: 0 | Calls: 21 | Vars: 5 | Nesting: 10
# Calls: ArgumentParser, add_argument, add_parser, add_subparsers, parse_args, print_help, run_add_smashlet, run_build, run_force, run_init, run_status

```

## smash_core/commands/add.py

```python
def run_add_smashlet(name = None, template = 'default', glob = '*', output = 'dist/', context_mode = False)
# Create a new smashlet file with boilerplate content.
# Args:
# name (str or None): If provided, creates `smashlet_<name>.py`; otherwise, uses template's default filename.
# Lines: 44
# Type hints: ❌
# Branches: 4 | Loops: 0 | Returns: 2 | Calls: 10 | Vars: 8 | Nesting: 10
# Calls: cwd, exists, format, get, keys, list, log, write_text

```

## smash_core/commands/build.py

```python
def run_build(force = False)
# Run the full Smash build loop.
# - Discovers all smashlets in the project
# - Runs each in mtime order
# Lines: 44
# Type hints: ❌
# Branches: 5 | Loops: 2 | Returns: 1 | Calls: 15 | Vars: 7 | Nesting: 11
# Calls: build_context, discover_smashlets, find_project_root, len, log, relative_to, run_smashlet, should_run, sorted, stat, touch

def run_force(smashlet_path = None)
# Force-run a specific smashlet, or all smashlets if none is given.
# Lines: 21
# Type hints: ❌
# Branches: 3 | Loops: 0 | Returns: 3 | Calls: 9 | Vars: 3 | Nesting: 8
# Calls: Path, build_context, exists, find_project_root, log, run_build, run_smashlet

```

## smash_core/commands/init.py

```python
def run_init()
# Initialize a new Smash project by creating a .smash/ directory.
# If the directory already exists, informs the user without modifying it.
# Lines: 18
# Type hints: ❌
# Branches: 1 | Loops: 0 | Returns: 1 | Calls: 6 | Vars: 2 | Nesting: 8
# Calls: cwd, exists, log, mkdir

```

## smash_core/commands/status.py

```python
def run_status()
# Analyze and print the status of each smashlet (dry run).
# Possible states:
# - ⚙️ will run (inputs changed)
# Lines: 85
# Type hints: ❌
# Branches: 14 | Loops: 1 | Returns: 1 | Calls: 43 | Vars: 19 | Nesting: 11
# Calls: Path, any, build_context, callable, discover_smashlets, exists, find_project_root, get, get_outputs, get_runlog, getattr, glob, hasattr, list, load_smashlet_module, log, max, relative_to, sorted, stat, str, time

```

## smash_core/context_loader.py

```python
def load_context_data(context_dir: Path)
# Load context values from a directory or context.json file.
# Returns:
# merged (dict): Parsed content from .json/.yaml/.txt files
# Lines: 45
# Type hints: ✅
# Branches: 7 | Loops: 1 | Returns: 3 | Calls: 14 | Vars: 8 | Nesting: 12
# Calls: endswith, exists, is_dir, is_file, iterdir, loads, read_text, safe_load, startswith

def build_context(project_root: Path) -> dict
# Construct the full build context for Smash execution.
# Includes:
# - Global context/ files (if any)
# Lines: 35
# Type hints: ✅
# Branches: 3 | Loops: 0 | Returns: 1 | Calls: 8 | Vars: 10 | Nesting: 8
# Calls: exec_module, exists, hasattr, load_context_data, module_from_spec, on_context, spec_from_file_location

```

## smash_core/files.py

```python
def resolve(relative_path, context)
# Resolve a file path for use inside a smashlet.
# - If `relative_path` starts with '/', it's resolved from the project root
# - Otherwise, from the smashlet's directory
# Lines: 21
# Type hints: ❌
# Branches: 3 | Loops: 0 | Returns: 2 | Calls: 11 | Vars: 3 | Nesting: 8
# Calls: Path, ValueError, get, resolve, startswith, str

def read(relative_path, context)
# Read a file's contents relative to the smashlet directory.
# Lines: 5
# Type hints: ❌
# Branches: 0 | Loops: 0 | Returns: 1 | Calls: 2 | Vars: 0 | Nesting: 6
# Calls: read_text, resolve

def write(relative_path, data, context)
# Write a string to a file relative to the smashlet directory.
# Lines: 7
# Type hints: ❌
# Branches: 0 | Loops: 0 | Returns: 0 | Calls: 3 | Vars: 1 | Nesting: 6
# Calls: mkdir, resolve, write_text

```

## smash_core/helpers.py

```python
def get_digest(content)
# ⚠️ No docstring
# Lines: 2
# Type hints: ❌
# Branches: 0 | Loops: 0 | Returns: 1 | Calls: 3 | Vars: 0 | Nesting: 8
# Calls: encode, hexdigest, sha1

def read_text_files(paths)
# Read a list of file paths and return their contents as strings.
# Lines: 5
# Type hints: ❌
# Branches: 0 | Loops: 0 | Returns: 1 | Calls: 2 | Vars: 0 | Nesting: 7
# Calls: Path, read_text

def write_output(path, content)
# Write string content to a file, creating parent directories if needed.
# Lines: 7
# Type hints: ❌
# Branches: 0 | Loops: 0 | Returns: 0 | Calls: 3 | Vars: 1 | Nesting: 6
# Calls: Path, mkdir, write_text

def smash_log(msg)
# Standardized log output for use in smashlets.
# Lines: 5
# Type hints: ❌
# Branches: 0 | Loops: 0 | Returns: 0 | Calls: 1 | Vars: 0 | Nesting: 6
# Calls: print

def ensure_dir(path)
# Ensure a directory exists (like mkdir -p).
# Lines: 5
# Type hints: ❌
# Branches: 0 | Loops: 0 | Returns: 0 | Calls: 2 | Vars: 0 | Nesting: 6
# Calls: Path, mkdir

def flatten_json_dir(path)
# Load and flatten all JSON files in a directory into a list of dicts.
# Ignores non-.json files. Returns list of parsed objects.
# Lines: 15
# Type hints: ❌
# Branches: 0 | Loops: 1 | Returns: 1 | Calls: 5 | Vars: 2 | Nesting: 8
# Calls: Path, append, glob, loads, read_text

def write_output_if_changed(path, content, context)
# Writes `content` to the resolved path only if it differs from what's already there.
# Returns True if a write occurred (content changed), else False.
# Lines: 14
# Type hints: ❌
# Branches: 3 | Loops: 0 | Returns: 2 | Calls: 6 | Vars: 2 | Nesting: 7
# Calls: exists, isinstance, mkdir, read_text, resolve, write_text

```

## smash_core/log.py

```python
def log(msg: str)
# Log a message with a standard prefix.
# Args:
# msg (str): The message to print
# Lines: 10
# Type hints: ✅
# Branches: 0 | Loops: 0 | Returns: 0 | Calls: 2 | Vars: 1 | Nesting: 6
# Calls: get, print

```

## smash_core/project.py

```python
def find_project_root()
# Locate the root of the Smash project by walking upward from the current directory.
# A project is identified by the presence of a `.smash/` directory.
# Returns None if no root is found.
# Lines: 13
# Type hints: ❌
# Branches: 1 | Loops: 1 | Returns: 2 | Calls: 2 | Vars: 2 | Nesting: 7
# Calls: cwd, is_dir

def get_runlog(project_root)
# Read and normalize the runlog from `.smash/runlog.json`.
# Requires entries to be structured dicts:
# {
# Lines: 53
# Type hints: ❌
# Branches: 5 | Loops: 2 | Returns: 3 | Calls: 14 | Vars: 7 | Nesting: 8
# Calls: append, exists, get, isinstance, items, len, loads, log, read_text

def update_runlog(project_root, smashlet_path, finished_on = None, duration = None)
# ⚠️ No docstring
# Lines: 22
# Type hints: ❌
# Branches: 2 | Loops: 0 | Returns: 0 | Calls: 11 | Vars: 12 | Nesting: 7
# Calls: append, dumps, get, get_runlog, int, isinstance, str, time, write_text

```

## smash_core/smashlets.py

```python
def discover_smashlets(root: Path)
# Discover all smashlet files in the project.
# Supports:
# - smashlet.py
# Lines: 19
# Type hints: ✅
# Branches: 0 | Loops: 0 | Returns: 1 | Calls: 2 | Vars: 0 | Nesting: 9
# Calls: rglob, startswith

def load_smashlet_module(smashlet_path: Path)
# Dynamically load a smashlet as a Python module.
# Ensures the project root is in sys.path so that smashlets can
# import modules from the root.
# Lines: 30
# Type hints: ✅
# Branches: 1 | Loops: 0 | Returns: 2 | Calls: 7 | Vars: 3 | Nesting: 8
# Calls: exec_module, insert, module_from_spec, smash_log, spec_from_file_location, str

def should_run(smashlet_path: Path, project_root: Path) -> bool
# Determine whether a smashlet should run.
# Decisions are based on:
# - Constants like RUN, INPUT_GLOB
# Lines: 100
# Type hints: ✅
# Branches: 10 | Loops: 2 | Returns: 10 | Calls: 36 | Vars: 18 | Nesting: 12
# Calls: Path, any, build_context, callable, exists, get, get_runlog, getattr, glob, list, load_smashlet_module, max, smash_log, stat, str, time, update

def run_smashlet(smashlet_path: Path, project_root: Path, global_context: dict) -> bool
# Execute a smashlet's run() function, injecting both global and local context.
# Automatically updates the runlog after successful execution.
# Args:
# Lines: 81
# Type hints: ✅
# Branches: 5 | Loops: 0 | Returns: 4 | Calls: 26 | Vars: 18 | Nesting: 8
# Calls: callable, dict, exists, getattr, glob, len, list, load_context_data, load_smashlet_module, round, run_func, setdefault, signature, smash_log, time, update, update_runlog

def touch(path: Path)
# Update the modified timestamp of a file or directory.
# Used to mark a file as changed without modifying contents.
# Args:
# Lines: 9
# Type hints: ✅
# Branches: 0 | Loops: 0 | Returns: 0 | Calls: 1 | Vars: 0 | Nesting: 5
# Calls: touch

```
