from pathlib import Path

import pytest


@pytest.fixture
def base_hw_path():
    return Path(__file__).parent.parent.parent / "homeworks"
