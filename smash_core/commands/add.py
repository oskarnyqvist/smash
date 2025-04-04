# smash_core/commands/add.py
"""
Creates new smashlet files from templates, used by the `smash add` CLI command.

Implements the logic behind `smash add`, with support for multiple boilerplate templates.
"""

from pathlib import Path
from smash_core.log import log

TEMPLATES = {
    "default": {
        "filename": "smashlet.py",
        "content": """# {filename}
#
# Smashlet: {display_name}
# Auto-generated with `smash add`
#
INPUT_GLOB = "{glob}"
OUTPUT_DIR = "{output}"

def run({context_signature}):
    pass  # TODO: implement transformation logic
""",
    },
    "minimal": {
        "filename": "smashlet.py",
        "content": """# {filename}
#
# Minimal Smashlet: {display_name}
#
INPUT_GLOB = "{glob}"
OUTPUT_DIR = "{output}"

def run({context_signature}):
    # Minimal transformation logic
    pass
""",
    },
    "pandas": {
        "filename": "smashlet.py",
        "content": """# {filename}
#
# Pandas Smashlet: {display_name}
# Provides boilerplate for data processing with pandas.
#
INPUT_GLOB = "{glob}"
OUTPUT_DIR = "{output}"

def run({context_signature}):
    import pandas as pd
    # TODO: Load input files into DataFrames, process data, and output results.
    pass
""",
    },
}


def run_add_smashlet(
    name=None, template="default", glob="*", output="dist/", context_mode=False
):
    """
    Generates a new smashlet file from a template.

    Used by the `smash add` CLI command. Supports custom names, glob patterns, and optional `run(context)` mode.
    Skips file creation if the target already exists.
    """
    tmpl = TEMPLATES.get(template)
    if not tmpl:
        log(
            f"❌ Template '{template}' not found. Available templates: {list(TEMPLATES.keys())}",
            level="error",
        )
        return

    if name:
        filename = f"smashlet_{name}.py"
        display_name = name
    else:
        filename = tmpl["filename"]
        display_name = "unnamed"

    context_signature = "context" if context_mode else ""
    content = tmpl["content"].format(
        filename=filename,
        display_name=display_name,
        glob=glob,
        output=output,
        context_signature=context_signature,
    )

    path = Path.cwd() / filename
    if path.exists():
        log(f"⚠️  {filename} already exists. Aborting.", level="warn")
        return

    path.write_text(content)
    log(f"✅ Created {filename} using template '{template}'.")
