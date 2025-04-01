"""
context_loader.py

Loads and builds the full execution context for Smash builds and smashlets.
Merges global context, local context, and optional `smash.py` logic.
"""

import json
from pathlib import Path


def load_context_data(context_dir: Path):
    """
    Load context values from a directory or context.json file.

    Returns:
        merged (dict): Parsed content from .json/.yaml/.txt files
        paths (dict):   Raw Path objects keyed by filename
    """
    merged = {}
    paths = {}

    if context_dir.is_file() and context_dir.name.endswith(".json"):
        try:
            merged = json.loads(context_dir.read_text())
            paths[context_dir.name] = context_dir
        except Exception:
            pass
        return merged, paths

    if not context_dir.exists():
        return merged, paths

    if context_dir.is_dir():
        for f in context_dir.iterdir():
            if f.name.startswith(".") or not f.is_file():
                continue

            paths[f.name] = f

            try:
                if f.suffix == ".json":
                    merged[f.stem] = json.loads(f.read_text())
                elif f.suffix in [".yml", ".yaml"]:
                    try:
                        import yaml

                        merged[f.stem] = yaml.safe_load(f.read_text())
                    except ImportError:
                        pass
                elif f.suffix == ".txt":
                    merged[f.stem] = f.read_text()
            except Exception:
                continue

    return merged, paths


def build_context(project_root: Path) -> dict:
    """
    Construct the full build context for Smash execution.

    Includes:
    - Global context/ files (if any)
    - smash.py config and `on_context()` hook (if present)

    Returns:
        context (dict): Final merged context
    """
    context = {"project_root": project_root}

    # Inject top-level context/ files (if any)
    context_dir = project_root / "context"
    merged_ctx, ctx_paths = load_context_data(context_dir)
    context["context"] = merged_ctx
    context["context_files"] = ctx_paths

    # Optional: load smash.py
    smash_py = project_root / "smash.py"
    if smash_py.exists():
        import importlib.util

        spec = importlib.util.spec_from_file_location("smash", smash_py)
        smash_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(smash_mod)

        if hasattr(smash_mod, "config"):
            context["config"] = smash_mod.config

        if hasattr(smash_mod, "on_context"):
            context = smash_mod.on_context(context) or context

    return context
