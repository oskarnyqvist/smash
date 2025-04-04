# tests/unit/test_public_api.py

"""
Tests that key helper functions are exposed via the public `smash` API.

Checks for presence of `read`, `write`, `log_step`, and `read_text_files`.
"""

import smash


def test_public_api_exports():
    assert callable(smash.read)
    assert callable(smash.write)
    assert callable(smash.log_step)
    assert callable(smash.read_text_files)
