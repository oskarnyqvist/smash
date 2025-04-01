# tests/unit/test_public_api.py

import smash


def test_public_api_exports():
    assert callable(smash.read)
    assert callable(smash.write)
    assert callable(smash.log_step)
    assert callable(smash.read_text_files)
