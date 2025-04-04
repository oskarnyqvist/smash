# tests/unit/test_project.py

"""
Tests project-level helpers for root detection and runlog tracking.

Covers `find_project_root()`, `get_runlog()`, and `update_runlog()` in typical project setups.
"""

import os
import json
import time
from smash_core.project import find_project_root, get_runlog, update_runlog


def test_find_project_root_detects_smash_dir(tmp_path):
    smash_dir = tmp_path / ".smash"
    smash_dir.mkdir()

    os.chdir(tmp_path)
    root = find_project_root()

    assert root == tmp_path


def test_find_project_root_returns_none_if_missing(tmp_path):
    os.chdir(tmp_path)
    assert find_project_root() is None


def test_get_runlog_returns_empty_if_missing(tmp_path):
    smash_dir = tmp_path / ".smash"
    smash_dir.mkdir()

    os.chdir(tmp_path)
    assert get_runlog(tmp_path) == {}


def test_get_runlog_parses_existing_json(tmp_path):
    smash_dir = tmp_path / ".smash"
    smash_dir.mkdir()

    runlog_path = smash_dir / "runlog.json"
    runlog_path.write_text(
        json.dumps(
            {
                "smashlet_foo.py": {
                    "last_run": 1234567890,
                    "runs": 1,
                    "history": [{"finished_on": 1234567890}],
                }
            }
        )
    )

    os.chdir(tmp_path)
    runlog = get_runlog(tmp_path)
    entry = runlog["smashlet_foo.py"]
    assert entry["last_run"] == 1234567890
    assert entry["runs"] == 1
    assert len(entry["history"]) == 1


def test_update_runlog_adds_or_updates_entry(tmp_path):
    smash_dir = tmp_path / ".smash"
    smash_dir.mkdir()

    fake_smashlet = tmp_path / "smashlet_example.py"
    fake_smashlet.touch()

    os.chdir(tmp_path)
    update_runlog(tmp_path, fake_smashlet)

    runlog_path = smash_dir / "runlog.json"
    assert runlog_path.exists()

    runlog = json.loads(runlog_path.read_text())
    assert str(fake_smashlet) in runlog
    entry = runlog[str(fake_smashlet)]
    assert isinstance(entry, dict)
    assert "last_run" in entry
    assert "runs" in entry
    assert "history" in entry
    assert isinstance(entry["history"], list)

    entry = runlog[str(fake_smashlet)]
    assert entry["last_run"] <= int(time.time())
