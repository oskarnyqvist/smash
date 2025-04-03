import json
import os
import time

from smash_core.project import get_runlog, update_runlog
from smash_core.smashlets import should_run

SLEEP_TIME = 0.1
# tests/unit/test_smashlets.py


SLEEP_TIME = 0.1


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


def test_run_always_triggers_after_timeout(tmp_path):
    smashlet = tmp_path / "smashlet_always.py"
    smashlet.write_text("""
RUN = "always"
RUN_TIMEOUT = 0
def run():
    return 1
""")
    assert should_run(smashlet, tmp_path) is True


def test_run_always_skips_if_timeout_not_reached(tmp_path):
    smashlet = tmp_path / "smashlet_wait.py"
    smashlet.write_text("""
RUN = "always"
RUN_TIMEOUT = 60
def run():
    return 1
""")

    # Write a fake runlog
    runlog_dir = tmp_path / ".smash"
    runlog_dir.mkdir()
    (runlog_dir / "runlog.json").write_text(
        json.dumps({str(smashlet): {"last_run": int(time.time()), "runs": 1}})
    )

    assert should_run(smashlet, tmp_path) is False


def test_smashlet_without_input_glob_can_still_run(tmp_path):
    smashlet = tmp_path / "smashlet_no_inputs.py"
    smashlet.write_text("""
RUN = "always"
RUN_TIMEOUT = 0
def run():
    return 1
""")
    assert should_run(smashlet, tmp_path) is True


def test_invalid_run_value_causes_failure(tmp_path):
    smashlet = tmp_path / "smashlet_bad_run.py"
    smashlet.write_text("""
RUN = "sometimes"
def run():
    return 1
""")
    assert should_run(smashlet, tmp_path) is False


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


def test_update_runlog_adds_history(tmp_path):
    (tmp_path / ".smash").mkdir()
    smashlet_path = tmp_path / "smashlet.py"
    smashlet_path.write_text("def run(): return 1")

    update_runlog(tmp_path, smashlet_path, finished_on=1234567890, duration=0.42)

    runlog = get_runlog(tmp_path)
    entry = runlog[str(smashlet_path)]

    assert entry["last_run"] == 1234567890
    assert entry["runs"] == 1
    assert len(entry["history"]) == 1
    assert entry["history"][0]["finished_on"] == 1234567890
    assert entry["history"][0]["duration"] == 0.42
