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

    input_file = tmp_path / "file.md"
    input_file.write_text("hello")

    smashlet = tmp_path / "smashlet_test.py"
    smashlet.write_text("""
INPUT_GLOB = "*.md"
OUTPUT_DIR = "dist/"

def run():
    return 1
""")
    time.sleep(1)
    input_file.touch()

    assert should_run(smashlet, tmp_path) is True


def test_should_not_run_if_run_missing(tmp_path):
    os.chdir(tmp_path)

    smashlet = tmp_path / "smashlet_broken.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "out/"
""")
    assert should_run(smashlet, tmp_path) is False


def test_should_run_if_output_missing(tmp_path):
    os.chdir(tmp_path)

    input_file = tmp_path / "input.txt"
    input_file.write_text("data")

    smashlet = tmp_path / "smashlet_track.py"
    smashlet.write_text("""
from pathlib import Path
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist"

def get_outputs():
    return [Path("dist/out.html")]

def run():
    return 1
""")

    assert should_run(smashlet, tmp_path) is True


def test_should_not_run_if_outputs_up_to_date(tmp_path):
    os.chdir(tmp_path)

    input_file = tmp_path / "input.txt"
    input_file.write_text("data")
    time.sleep(1)

    out_file = tmp_path / "dist"
    out_file.mkdir()
    out_path = out_file / "out.html"
    out_path.write_text("old output")

    smashlet = tmp_path / "smashlet_static.py"
    smashlet.write_text("""
from pathlib import Path
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist"

def get_outputs():
    return [Path("dist/out.html")]

def run():
    return 1
""")
    time.sleep(1)
    out_path.touch()
    assert should_run(smashlet, tmp_path) is False


def test_should_run_if_input_newer_than_output(tmp_path):
    os.chdir(tmp_path)

    input_file = tmp_path / "input.txt"
    input_file.write_text("data")

    out_dir = tmp_path / "dist"
    out_dir.mkdir()
    out_file = out_dir / "out.html"
    out_file.write_text("old")
    time.sleep(1)
    input_file.touch()

    smashlet = tmp_path / "smashlet_input_newer.py"
    smashlet.write_text("""
from pathlib import Path
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist"

def get_outputs():
    return [Path("dist/out.html")]

def run():
    return 1
""")

    assert should_run(smashlet, tmp_path) is True
