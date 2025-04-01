# test_log.py
#
# Unit tests for the log() function in smash_core.log.

import io
import sys
import pytest
from smash_core.log import log


@pytest.mark.parametrize(
    "level, expected_prefix",
    [
        ("info", "ℹ️ "),
        ("warn", "⚠️ "),
        ("error", "❌"),
        ("debug", "🐛"),
        ("unknown", ""),  # fallback case
    ],
)
def test_log_output_prefix(level, expected_prefix):
    stream = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = stream

    try:
        log("hello world", level=level)
    finally:
        sys.stdout = sys_stdout

    output = stream.getvalue().strip()
    assert output.startswith(expected_prefix)
    assert "hello world" in output
