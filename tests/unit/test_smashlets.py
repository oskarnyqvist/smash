# tests/unit/test_smashlets.py

import json
import os
import time

from smash_core.smashlets import discover_smashlets, run_smashlet, should_run, touch

SLEEP_TIME = 0.1


def write(ctx_path, name, content):
    path = ctx_path / name
    path.write_text(content)
    return path


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
    time.sleep(SLEEP_TIME)

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
    time.sleep(SLEEP_TIME)
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
    time.sleep(SLEEP_TIME)

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
    time.sleep(SLEEP_TIME)
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
    time.sleep(SLEEP_TIME)
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


def test_project_context_json_is_loaded(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / ".smash").mkdir()

    ctx_dir = tmp_path / "context"
    ctx_dir.mkdir()
    write(ctx_dir, "config.json", json.dumps({"version": "1.0"}))

    smashlet = tmp_path / "smashlet_check.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "out"

def run(context):
    assert context["context"]["config"]["version"] == "1.0"
    return 1
""")
    (tmp_path / "file.txt").write_text("data")

    assert run_smashlet(smashlet, tmp_path, {"project_root": tmp_path}) is True


def test_local_context_overrides_project_context(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / ".smash").mkdir()

    root_ctx = tmp_path / "context"
    root_ctx.mkdir()
    write(root_ctx, "config.json", json.dumps({"env": "prod"}))

    smashlet_dir = tmp_path / "nested"
    smashlet_dir.mkdir()
    local_ctx = smashlet_dir / "context"
    local_ctx.mkdir()
    write(local_ctx, "config.json", json.dumps({"env": "local"}))

    smashlet = smashlet_dir / "smashlet_override.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "out"

def run(context):
    assert context["context"]["config"]["env"] == "local"
    return 1
""")
    (smashlet_dir / "file.txt").write_text("content")

    assert run_smashlet(smashlet, tmp_path, {"project_root": tmp_path}) is True


def test_txt_file_is_loaded_into_context(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / ".smash").mkdir()

    ctx_dir = tmp_path / "context"
    ctx_dir.mkdir()
    write(ctx_dir, "note.txt", "hello world")

    smashlet = tmp_path / "smashlet_note.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "out"

def run(context):
    assert context["context"]["note"] == "hello world"
    return 1
""")
    (tmp_path / "file.txt").write_text("ok")

    assert run_smashlet(smashlet, tmp_path, {"project_root": tmp_path}) is True


def test_unsupported_file_is_in_context_files_only(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / ".smash").mkdir()

    ctx_dir = tmp_path / "context"
    ctx_dir.mkdir()
    unsupported = write(ctx_dir, "binary.dat", b"1234".decode("utf-8"))

    smashlet = tmp_path / "smashlet_bin.py"
    smashlet.write_text("""\
from pathlib import Path
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "out"

def run(context):
    assert "binary.dat" in context["context_files"]
    assert isinstance(context["context_files"]["binary.dat"], Path)
    return 1
""")

    (tmp_path / "file.txt").write_text("trigger")

    assert run_smashlet(smashlet, tmp_path, {"project_root": tmp_path}) is True


def test_inputs_are_injected(tmp_path):
    # Simulate a Smash project
    project_root = tmp_path
    os.chdir(project_root)
    (project_root / ".smash").mkdir()

    # Create input files
    (project_root / "foo.txt").write_text("hello")
    (project_root / "bar.txt").write_text("world")
    (project_root / "ignore.md").write_text("nope")

    # Create a smashlet that captures injected inputs
    smashlet_path = project_root / "smashlet.py"
    smashlet_path.write_text(
        """
from pathlib import Path        
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist/"

def run(context):
    matched = sorted(f.name for f in context["inputs"])
    out = "\\n".join(matched)
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    Path(OUTPUT_DIR + "/out.txt").write_text(out)
    return 1
"""
    )

    # Run the smashlet
    result = run_smashlet(smashlet_path, project_root, {"project_root": project_root})

    # Check it ran
    assert result is True

    # Check the output file was created and is correct
    out_file = project_root / "dist" / "out.txt"
    assert out_file.exists()
    lines = out_file.read_text().splitlines()
    assert "foo.txt" in lines
    assert "bar.txt" in lines
    assert "ignore.md" not in lines


def test_should_run_with_custom_logic_returns_true(tmp_path):
    smashlet = tmp_path / "smashlet_true.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
def should_run(context):
    return True
def run(context):
    return 1
""")
    (tmp_path / "file.txt").write_text("data")
    assert should_run(smashlet, tmp_path) is True


def test_should_run_with_custom_logic_returns_false(tmp_path):
    smashlet = tmp_path / "smashlet_false.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
def should_run(context):
    return False
def run(context):
    return 1
""")
    (tmp_path / "file.txt").write_text("data")
    assert should_run(smashlet, tmp_path) is False


def test_should_run_custom_logic_with_context_values(tmp_path):
    smashlet = tmp_path / "smashlet_context.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
def should_run(context):
    assert "last_run" in context
    assert "smashlet_mtime" in context
    assert "latest_input_mtime" in context
    return True
def run(context):
    return 1
""")
    (tmp_path / "file.txt").write_text("data")
    assert should_run(smashlet, tmp_path) is True


def test_should_run_with_broken_custom_logic(tmp_path):
    smashlet = tmp_path / "smashlet_broken_logic.py"
    smashlet.write_text("""
INPUT_GLOB = "*.txt"
def should_run(context):
    raise RuntimeError("fail!")
def run(context):
    return 1
""")
    (tmp_path / "file.txt").write_text("data")
    assert should_run(smashlet, tmp_path) is False
