# add.py
"""
Implements the `add` command for creating new smashlet files.
Supports multiple templates via the `template` argument.
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
    Create a new smashlet file with boilerplate content.

    Args:
        name (str or None): If provided, creates `smashlet_<name>.py`; otherwise, uses template's default filename.
        template (str): Template name to use for boilerplate content.
        glob (str): Glob pattern for inputs (default: "*").
        output (str): Output directory for results (default: "dist/").
        context_mode (bool): If True, generate a run signature using `run(context)`, else `run()`.
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
