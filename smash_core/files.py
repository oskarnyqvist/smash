"""
Provides path-safe `read`, `write`, and `resolve` functions for use in smashlets.

These functions interpret paths relative to the smashlet's directory (`context["cwd"]`) or project root.
Exposed to users via the public `smash` API.
"""

from pathlib import Path


def resolve(relative_path, context):
    """
    Resolve a file path for use inside a smashlet.

    - If `relative_path` starts with '/', it's resolved from the project root
    - Otherwise, from the smashlet's directory

    `..` and other parts are automatically normalized.
    """
    relative_path = str(relative_path)

    if relative_path.startswith("/"):
        root = context.get("project_root")
        if not root:
            raise ValueError("Context missing 'project_root'")
        return (Path(root) / relative_path[1:]).resolve()
    else:
        cwd = context.get("cwd") or context.get("smashlet_dir")
        if not cwd:
            raise ValueError("Context missing 'cwd' or 'smashlet_dir'")
        return (Path(cwd) / relative_path).resolve()


def read(relative_path, context):
    """
    Read a file's contents relative to the smashlet directory.
    """
    return resolve(relative_path, context).read_text()


def write(relative_path, data, context):
    """
    Write a string to a file relative to the smashlet directory.
    """
    path = resolve(relative_path, context)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
