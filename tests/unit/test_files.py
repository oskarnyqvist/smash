"""
Tests file I/O helpers used in smashlets: `read`, `write`, and `resolve`.

Verifies that paths are correctly resolved relative to `context["cwd"]`
and that basic reading and writing behaves as expected.
"""

import os
from smash_core.files import read, write, resolve


def test_resolve_and_read_write(tmp_path):
    os.chdir(tmp_path)
    smashlet_dir = tmp_path / "smashlet_test"
    smashlet_dir.mkdir()

    context = {"cwd": smashlet_dir}

    # Write a file in the smashlet dir
    write("example.txt", "Hello Smash!", context)

    resolved_path = resolve("example.txt", context)
    assert resolved_path.exists()
    assert resolved_path.parent == smashlet_dir
    assert resolved_path.read_text() == "Hello Smash!"

    content = read("example.txt", context)
    assert content == "Hello Smash!"
