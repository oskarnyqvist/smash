# test_commands.py

"""
Tests the behavior of CLI commands like `smash add`, `smash run`, and `smash build`.

Verifies smashlet generation, input glob handling, file overwrite protection, and force-run logic.
"""

import os

from smash_core.commands import run_add_smashlet, run_build, run_force

SLEEP_TIME = 0.2


def test_add_creates_named_smashlet(tmp_path):
    os.chdir(tmp_path)
    run_add_smashlet("demo")

    file = tmp_path / "smashlet_demo.py"
    assert file.exists()
    contents = file.read_text()

    assert "INPUT_GLOB" in contents
    assert "OUTPUT_DIR" in contents
    assert "def run()" in contents
    assert "smashlet_demo.py" in contents


def test_add_creates_default_smashlet_py(tmp_path):
    os.chdir(tmp_path)
    run_add_smashlet(name=None)

    file = tmp_path / "smashlet.py"
    assert file.exists()
    contents = file.read_text()
    assert "Smashlet: unnamed" in contents


def test_add_smashlet_with_context(tmp_path):
    os.chdir(tmp_path)
    run_add_smashlet("ctx", context_mode=True)

    file = tmp_path / "smashlet_ctx.py"
    contents = file.read_text()
    assert "def run(context):" in contents


def test_add_skips_if_file_exists(tmp_path):
    os.chdir(tmp_path)

    existing = tmp_path / "smashlet_skip.py"
    existing.write_text("# existing file")

    run_add_smashlet("skip")

    # Should NOT overwrite
    contents = existing.read_text()
    assert contents.strip() == "# existing file"


def test_run_force_executes_all_or_one(tmp_path):
    import os

    os.chdir(tmp_path)
    (tmp_path / ".smash").mkdir()

    # Shared log to track execution
    log_path = tmp_path / "log.txt"

    # Write two smashlets that append their name to the log when run
    for name in ["a", "b"]:
        (tmp_path / f"smashlet_{name}.py").write_text(f"""
from pathlib import Path

INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist_{name}/"

def run(context):
    with open("{log_path.name}", "a") as f:
        f.write("{name}\\n")
    return 0
""")

    # Create a dummy input file so INPUT_GLOB matches
    (tmp_path / "input.txt").write_text("test")

    # Run smart build — both should run
    run_build()
    assert log_path.read_text().splitlines() == ["a", "b"]

    # Clear log
    log_path.unlink()

    # Run force: only smashlet_b.py should run
    run_force(str(tmp_path / "smashlet_b.py"))
    assert log_path.read_text().splitlines() == ["b"]

    # Clear log again
    log_path.unlink()

    # Run force: all smashlets
    run_force()
    lines = log_path.read_text().splitlines()
    assert "a" in lines and "b" in lines
