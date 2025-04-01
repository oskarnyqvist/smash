# 🗂 File Overview

## smash/
- `smash/__init__.py`
     Lines of code: 20
     (Imports: smash_core.files, smash_core.helpers, smash_core.log)

## smash_core/
- `smash_core/__init__.py`
     Lines of code: 7
     (Imports: smash_core.helpers)
- `smash_core/cli.py`
    Smash CLI entry point.
    Dispatches commands for init, build, add, run (force), and status.
     Functions: main
     Lines of code: 55
     (Imports: argparse, smash_core.commands, smash_core.commands.status)
- `smash_core/commands/__init__.py`
     Lines of code: 3
     (Imports: add, build, init)
- `smash_core/commands/add.py`
    Implements the `add` command for creating new smashlet files.
    Supports multiple templates via the `template` argument.
     Functions: run_add_smashlet
     Lines of code: 89
     (Imports: pathlib, smash_core.log)
- `smash_core/commands/build.py`
    Implements the main Smash build loop and the `run` (force) command.
     Functions: run_build, run_force
     Lines of code: 63
     (Imports: pathlib, smash_core.context_loader, smash_core.log, smash_core.project, smash_core.smashlets)
- `smash_core/commands/init.py`
    Handles project initialization for Smash.
    Creates a new .smash/ directory in the project root if it doesn't exist.
     Functions: run_init
     Lines of code: 22
     (Imports: pathlib, smash_core.log)
- `smash_core/commands/status.py`
    Implements the `smash status` command for dry-run build status reporting.
     Functions: run_status
     Lines of code: 84
     (Imports: pathlib, smash_core.context_loader, smash_core.log, smash_core.project, smash_core.smashlets, time)
- `smash_core/context_loader.py`
    Loads and builds the full execution context for Smash builds and smashlets.
    Merges global context, local context, and optional `smash.py` logic.
     Functions: load_context_data, build_context
     Lines of code: 71
     (Imports: json, pathlib)
- `smash_core/files.py`
    Path-safe helpers for reading, writing,
    and resolving files using context["cwd"]
     Functions: resolve, read, write
     Lines of code: 36
     (Imports: pathlib)
- `smash_core/helpers.py`
    Built-in utility functions for smashlets.
    These are exposed via `from smash.helpers import ...`
     Functions: get_digest, read_text_files, write_output, smash_log, ensure_dir, flatten_json_dir, write_output_if_changed
     Lines of code: 58
     (Imports: hashlib, pathlib, smash_core.files)
- `smash_core/log.py`
    Provides a consistent logging function used across Smash.
    Supports future extensions like timestamps, log levels, or formatting.
     Functions: log
     Lines of code: 20
- `smash_core/project.py`
    Handles project-level state and metadata.
    Includes logic for locating the project root and managing the runlog.
     Functions: find_project_root, get_runlog, update_runlog
     Lines of code: 39
     (Imports: json, pathlib, time)
- `smash_core/smashlets.py`
    Responsible for discovering, loading, and executing `smashlet_*.py` files.
    Supports multiple smashlets per directory. Each file defines its own transformation logic.
     Functions: discover_smashlets, load_smashlet_module, should_run, run_smashlet, touch
     Lines of code: 175
     (Imports: context_loader, importlib.util, pathlib, project, sys, time)

## tests/
- `tests/unit/test_commands.py`
     Functions: test_add_creates_named_smashlet, test_add_creates_default_smashlet_py, test_add_smashlet_with_context, test_add_skips_if_file_exists, test_run_force_executes_all_or_one
     Lines of code: 68
     (Imports: os, smash_core.commands)
- `tests/unit/test_files.py`
     Functions: test_resolve_and_read_write
     Lines of code: 18
     (Imports: os, smash_core.files)
- `tests/unit/test_log.py`
     Functions: test_log_output_prefix
     Lines of code: 28
     (Imports: io, pytest, smash_core.log, sys)
- `tests/unit/test_project.py`
     Functions: test_find_project_root_detects_smash_dir, test_find_project_root_returns_none_if_missing, test_get_runlog_returns_empty_if_missing, test_get_runlog_parses_existing_json, test_update_runlog_adds_or_updates_entry
     Lines of code: 40
     (Imports: json, os, smash_core.project, time)
- `tests/unit/test_public_api.py`
     Functions: test_public_api_exports
     Lines of code: 7
     (Imports: smash)
- `tests/unit/test_smashlets.py`
     Functions: write, test_discover_smashlets_finds_expected_files, test_touch_updates_mtime, test_should_run_when_input_is_newer, test_should_not_run_if_run_missing, test_should_run_if_output_missing, test_should_not_run_if_outputs_up_to_date, test_should_run_if_input_newer_than_output, test_project_context_json_is_loaded, test_local_context_overrides_project_context, test_txt_file_is_loaded_into_context, test_unsupported_file_is_in_context_files_only, test_inputs_are_injected
     Lines of code: 220
     (Imports: json, os, smash_core.smashlets, time)
- `tests/unit/test_status.py`
     Functions: test_status_output
     Lines of code: 53
     (Imports: os, smash_core.commands.status)
