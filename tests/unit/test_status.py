"""
Tests the `smash status` command for dry-run build state reporting.

Verifies that output reflects correct smashlet states: up to date, needs run, or skipped due to timeout.
"""

import os
from smash_core.commands.status import run_status


def test_status_output(tmp_path, capsys):
    os.chdir(tmp_path)

    # Simulate a Smash project
    (tmp_path / ".smash").mkdir()

    # ✅ smashlet_up_to_date
    smashlet_1 = tmp_path / "smashlet_up.py"
    smashlet_1.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist/"

def run(context):
    return 0
""")

    # ⚙️ smashlet_changed — its input is newer
    smashlet_2 = tmp_path / "smashlet_changed.py"
    smashlet_2.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist_changed/"

def run(context):
    return 1
""")

    # ⏳ smashlet_timeout — RUN = always, but timeout not reached
    smashlet_3 = tmp_path / "smashlet_timeout.py"
    smashlet_3.write_text("""
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist_timeout/"
RUN = "always"
RUN_TIMEOUT = 1000

def run(context):
    return 0
""")

    # create an input file
    input_file = tmp_path / "input.txt"
    input_file.write_text("test")

    # simulate runlog with timestamps
    runlog_path = tmp_path / ".smash" / "runlog.json"
    runlog_path.write_text(f"""{{
        "{smashlet_1}": 9999999999,
        "{smashlet_2}": 0,
        "{smashlet_3}": 9999999999
    }}""")

    # Execute dry-run status check
    run_status()

    # Capture the printed output
    output = capsys.readouterr().out

    assert "✅ smashlet_up.py — up to date" in output
    assert "⚙️ smashlet_changed.py — will run" in output
    assert "⏳ smashlet_timeout.py — skipped (timeout not reached)" in output
