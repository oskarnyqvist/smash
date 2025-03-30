# tests/unit/test_smashlets.py

import os
import time

from smash_core.smashlets import discover_smashlets, touch, should_run


def test_discover_smashlets_finds_expected_files(tmp_path):
    os.chdir(tmp_path)

    # Valid smashlets
    (tmp_path / "smashlet.py").write_text(
        "INPUT_GLOB = '*'\nOUTPUT_DIR = 'out/'\ndef run(): pass"
    )
    (tmp_path / "smashlet_foo.py").write_text(
        "INPUT_GLOB = '*'\nOUTPUT_DIR = 'out/'\ndef run(): pass"
    )

    # Should NOT be picked up
    (tmp_path / "not_a_smashlet.py").write_text("")

    found = discover_smashlets(tmp_path)
    found_names = sorted(f.name for f in found)

    assert "smashlet.py" in found_names
    assert "smashlet_foo.py" in found_names
    assert "not_a_smashlet.py" not in found_names


def test_touch_updates_mtime(tmp_path):
    target = tmp_path / "file.txt"
    target.write_text("hello")

    original_mtime = target.stat().st_mtime
    time.sleep(1)

    touch(target)
    new_mtime = target.stat().st_mtime

    assert new_mtime > original_mtime


def test_should_run_when_input_is_newer(tmp_path):
    os.chdir(tmp_path)

    # Create an input file
    input_file = tmp_path / "file.md"
    input_file.write_text("hello")

    # Smashlet with glob and run()
    smashlet = tmp_path / "smashlet_test.py"
    smashlet.write_text("""
INPUT_GLOB = "*.md"
OUTPUT_DIR = "dist/"

def run():
    return 1
""")

    time.sleep(1)  # ensure the input is newer
    input_file.touch()

    assert should_run(smashlet, tmp_path) is True


def test_should_not_run_if_input_is_older(tmp_path):
    os.chdir(tmp_path)

    # Create input + smashlet
    input_file = tmp_path / "file.md"
    input_file.write_text("old")

    smashlet = tmp_path / "smashlet_test.py"
    smashlet.write_text("""
INPUT_GLOB = "*.md"
OUTPUT_DIR = "dist/"
def run(): return 1
""")

    # Make sure their mtimes are in the past
    time.sleep(1)

    # Simulate a prior successful run AFTER both files
    from smash_core.project import update_runlog

    smash_dir = tmp_path / ".smash"
    smash_dir.mkdir()
    update_runlog(tmp_path, smashlet)

    assert should_run(smashlet, tmp_path) is False


def test_should_not_run_if_run_missing(tmp_path):
    os.chdir(tmp_path)

    smashlet = tmp_path / "smashlet_broken.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "out/"
# No run() defined
""")

    assert should_run(smashlet, tmp_path) is False
