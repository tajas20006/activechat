import os

import pytest

ci = pytest.mark.skipif(
    os.getenv("CI", "false").lower() == "true",
    reason="skip tests that are hard to setup on ci",
)
