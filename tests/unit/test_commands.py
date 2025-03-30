# tests/unit/test_commands.py

import os
from smash_core.commands import run_add_smashlet


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
    assert "Smashlet: (unnamed)" in contents


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
