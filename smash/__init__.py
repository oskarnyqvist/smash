# smash/__init__.py

"""
Public API for writing smashlets.

Exposes helper functions like `read`, `write`, `log`, and `write_output_if_changed`,
so that smashlets don't need to import from internal modules.
"""

from smash_core.helpers import (
    read_text_files,
    write_output,
    smash_log,
    ensure_dir,
    flatten_json_dir,
    write_output_if_changed,
)

from smash_core.files import (
    read,
    write,
    resolve,
)

from smash_core.log import log as log_raw

# Aliases for consistent naming in smashlets
log_step = smash_log
log = log_raw
