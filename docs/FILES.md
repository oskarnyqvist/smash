# 🗂 File Overview

## smash/
- `smash/__init__.py`
    Public API for writing smashlets.
    Exposes helper functions like `read`, `write`, `log`, and `write_output_if_changed`,
    so that smashlets don't need to import from internal modules.
     Lines of code: 22
     (Imports: smash_core.files, smash_core.helpers, smash_core.log)

## smash_core/
- `smash_core/__init__.py`
     Lines of code: 7
     (Imports: smash_core.helpers)
- `smash_core/cli.py`
    Command-line entry point for Smash.
    Parses arguments and dispatches to subcommands like `init`, `build`, `add`, `run`, and `status`.
    This is the main script run when you type `smash` in the terminal.
     Functions: main
     Lines of code: 55
     (Imports: argparse, smash_core.commands, smash_core.commands.status)
- `smash_core/commands/__init__.py`
     Lines of code: 3
     (Imports: add, build, init)
- `smash_core/commands/add.py`
    Creates new smashlet files from templates, used by the `smash add` CLI command.
    Implements the logic behind `smash add`, with support for multiple boilerplate templates.
     Functions: run_add_smashlet
     Lines of code: 89
     (Imports: pathlib, smash_core.log)
- `smash_core/commands/build.py`
    Runs the main Smash build loop and powers the `smash run` command.
    Discovers all smashlets, checks if they should run, and executes them in modification-time order.
    Used by the public CLI, but not part of the importable API.
     Functions: run_build, run_force
     Lines of code: 64
     (Imports: pathlib, smash_core.context_loader, smash_core.log, smash_core.project, smash_core.smashlets)
- `smash_core/commands/init.py`
    Handles the `smash init` command by creating a new `.smash/` directory.
    Used by the public CLI to initialize a Smash project. Not part of the importable API.
     Functions: run_init
     Lines of code: 21
     (Imports: pathlib, smash_core.log)
- `smash_core/commands/status.py`
    Implements the `smash status` command to preview which smashlets would run (dry run only).
    Used by the public CLI to show up-to-date, outdated, or skipped smashlets without executing them.
     Functions: run_status
     Lines of code: 85
     (Imports: pathlib, smash_core.context_loader, smash_core.log, smash_core.project, smash_core.smashlets, time)
- `smash_core/context_loader.py`
    Loads the full context dictionary used during a Smash build or smashlet run.
    It merges project-level context files, local override files, and optional logic from `smash.py`.
    This context is injected into each smashlet’s `run()` function.
     Functions: load_context_data, build_context
     Lines of code: 71
     (Imports: json, pathlib)
- `smash_core/files.py`
    Provides path-safe `read`, `write`, and `resolve` functions for use in smashlets.
    These functions interpret paths relative to the smashlet's directory (`context["cwd"]`) or project root.
    Exposed to users via the public `smash` API.
     Functions: resolve, read, write
     Lines of code: 36
     (Imports: pathlib)
- `smash_core/helpers.py`
    Reusable helper functions for writing smashlets.
    Includes logging, directory setup, safe writes, and batch file reading.
    Exposed to users via the public `smash` API.
     Functions: get_digest, read_text_files, write_output, smash_log, ensure_dir, flatten_json_dir, write_output_if_changed
     Lines of code: 58
     (Imports: hashlib, pathlib, smash_core.files)
- `smash_core/log.py`
    Standard logging utility used across Smash and in smashlets.
    Adds consistent emoji prefixes for log levels like info, warn, error, and debug.
    Part of the public smashlet API via `from smash import log`.
     Functions: log
     Lines of code: 20
- `smash_core/project.py`
    Manages project-level state, including project root detection and runlog persistence.
    - Locates the Smash project root (identified by a `.smash/` directory)
    - Reads and writes `.smash/runlog.json` with structured per-smashlet metadata
    Note: This module is internal and not part of the public Smash API.
     Functions: find_project_root, get_runlog, update_runlog
     Lines of code: 83
     (Imports: json, pathlib, smash_core.log, time)
- `smash_core/smashlets.py`
    This file runs all the `smashlet_*.py` files in the project.
    It handles finding them, deciding if they need to run (based on inputs, outputs, and timestamps),
    and executing their `run()` function with the right context.
    Used by the build system. Not part of the public API.
     Functions: discover_smashlets, load_smashlet_module, should_run, run_smashlet, touch
     Lines of code: 240
     (Imports: context_loader, importlib.util, pathlib, project, smash_core.log, sys, time)

## tests/
- `tests/unit/test_commands.py`
    Tests the behavior of CLI commands like `smash add`, `smash run`, and `smash build`.
    Verifies smashlet generation, input glob handling, file overwrite protection, and force-run logic.
     Functions: test_add_creates_named_smashlet, test_add_creates_default_smashlet_py, test_add_smashlet_with_context, test_add_skips_if_file_exists, test_run_force_executes_all_or_one
     Lines of code: 71
     (Imports: os, smash_core.commands)
- `tests/unit/test_files.py`
    Tests file I/O helpers used in smashlets: `read`, `write`, and `resolve`.
    Verifies that paths are correctly resolved relative to `context["cwd"]`
    and that basic reading and writing behaves as expected.
     Functions: test_resolve_and_read_write
     Lines of code: 20
     (Imports: os, smash_core.files)
- `tests/unit/test_log.py`
    Tests the `log()` function's output formatting for different log levels.
    Ensures correct emoji prefixes for "info", "warn", "error", "debug", and fallback cases.
     Functions: test_log_output_prefix
     Lines of code: 29
     (Imports: io, pytest, smash_core.log, sys)
- `tests/unit/test_project.py`
    Tests project-level helpers for root detection and runlog tracking.
    Covers `find_project_root()`, `get_runlog()`, and `update_runlog()` in typical project setups.
     Functions: test_find_project_root_detects_smash_dir, test_find_project_root_returns_none_if_missing, test_get_runlog_returns_empty_if_missing, test_get_runlog_parses_existing_json, test_update_runlog_adds_or_updates_entry
     Lines of code: 62
     (Imports: json, os, smash_core.project, time)
- `tests/unit/test_public_api.py`
    Tests that key helper functions are exposed via the public `smash` API.
    Checks for presence of `read`, `write`, `log_step`, and `read_text_files`.
     Functions: test_public_api_exports
     Lines of code: 10
     (Imports: smash)
- `tests/unit/test_should_run_behavior.py`
     Functions: test_should_run_with_custom_logic_returns_true, test_should_run_with_custom_logic_returns_false, test_should_run_custom_logic_with_context_values, test_should_run_with_broken_custom_logic, test_run_always_triggers_after_timeout, test_run_always_skips_if_timeout_not_reached, test_smashlet_without_input_glob_can_still_run, test_invalid_run_value_causes_failure, test_should_run_when_input_is_newer, test_should_not_run_if_run_missing, test_should_run_if_output_missing, test_should_not_run_if_outputs_up_to_date, test_should_run_if_input_newer_than_output, test_update_runlog_adds_history
     Lines of code: 188
     (Imports: json, os, smash_core.project, smash_core.smashlets, time)
- `tests/unit/test_smashlets.py`
     Functions: write, test_discover_smashlets_finds_expected_files, test_touch_updates_mtime, test_project_context_json_is_loaded, test_local_context_overrides_project_context, test_txt_file_is_loaded_into_context, test_unsupported_file_is_in_context_files_only, test_inputs_are_injected
     Lines of code: 140
     (Imports: json, os, smash_core.smashlets, time)
- `tests/unit/test_status.py`
    Tests the `smash status` command for dry-run build state reporting.
    Verifies that output reflects correct smashlet states: up to date, needs run, or skipped due to timeout.
     Functions: test_status_output
     Lines of code: 87
     (Imports: json, os, smash_core.commands.status, time)
