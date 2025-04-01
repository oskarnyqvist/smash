# add.py
#
# Implements the `add` command for creating new smashlet files.
# Supports multiple templates via the `template` argument.
# Currently defaults to a basic template, but is designed to be extended.

from pathlib import Path

# Template definitions (can be moved to separate files or modules later)
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
    # Example for future template expansion
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
        print(
            f"❌ Template '{template}' not found. Available templates: {list(TEMPLATES.keys())}"
        )
        return

    if name:
        filename = f"smashlet_{name}.py"
        display_name = name
    else:
        filename = tmpl["filename"]
        display_name = "unnamed"

    # Determine the run function signature based on context_mode.
    context_signature = "context" if context_mode else ""

    # Format the template content.
    content = tmpl["content"].format(
        filename=filename,
        display_name=display_name,
        glob=glob,
        output=output,
        context_signature=context_signature,
    )

    path = Path.cwd() / filename
    if path.exists():
        print(f"⚠️  {filename} already exists. Aborting.")
        return

    path.write_text(content)
    print(f"✅ Created {filename} using template '{template}'.")
