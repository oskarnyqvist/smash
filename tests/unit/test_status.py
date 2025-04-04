# tests/unit/test_status.py

"""
Tests the `smash status` command for dry-run build state reporting.

Verifies that output reflects correct smashlet states: up to date, needs run, or skipped due to timeout.
"""

import os
from smash_core.commands.status import run_status
import json
import time


def test_status_output(tmp_path, capsys):
    os.chdir(tmp_path)

    # Simulate a Smash project
    (tmp_path / ".smash").mkdir()

    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    (smashlet_1_output := dist_dir / "output.txt").write_text("dummy")
    smashlet_1_output.touch()

    # ✅ smashlet_up_to_date
    smashlet_1 = tmp_path / "smashlet_up.py"
    smashlet_1.write_text("""
from pathlib import Path
INPUT_GLOB = "*.txt"
OUTPUT_DIR = "dist/"

def get_outputs():
    return [Path("dist/output.txt")]

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

    input_file = tmp_path / "input.txt"
    input_file.write_text("test")

    # Touch all smashlet files after inputs are created
    time.sleep(0.1)
    smashlet_1.touch()
    time.sleep(0.2)
    smashlet_1_output.touch()
    smashlet_2.touch()
    smashlet_3.touch()

    # Ensure mtime is definitely older than runlog
    time.sleep(0.2)
    now = int(time.time())

    runlog_path = tmp_path / ".smash" / "runlog.json"
    runlog_path.write_text(
        json.dumps(
            {
                str(smashlet_1): {
                    "last_run": now,
                    "runs": 1,
                    "history": [{"finished_on": now}],
                },
                str(smashlet_2): {
                    "last_run": 0,
                    "runs": 1,
                    "history": [{"finished_on": 0}],
                },
                str(smashlet_3): {
                    "last_run": now,
                    "runs": 1,
                    "history": [{"finished_on": now}],
                },
            }
        )
    )

    # Execute dry-run status check
    run_status()

    # Capture the printed output
    output = capsys.readouterr().out
    print(output)

    assert "✅ smashlet_up.py — up to date" in output
    assert "⚙️ smashlet_changed.py — will run" in output
    assert "⏳ smashlet_timeout.py — skipped (timeout not reached)" in output
