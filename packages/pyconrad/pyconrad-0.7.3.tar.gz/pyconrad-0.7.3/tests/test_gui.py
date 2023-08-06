import os

import pytest

import pyconrad.autoinit


@pytest.mark.skipif("CI" in os.environ and os.environ["CI"] == "true", reason="Skipping this test on Travis CI.")
def test_start_gui():
    pyconrad.start_gui()
