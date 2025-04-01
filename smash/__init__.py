# smash/__init__.py
#
# Public API for smashlets. Use `import smash` inside your smashlets.

from smash_core.helpers import (
    read_text_files,
    write_output,
    smash_log,
    ensure_dir,
    flatten_json_dir,
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
