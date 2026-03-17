import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest

from rayhunter import RayhunterApi

HOSTNAME = "localhost"
PORT = 8080


@pytest.fixture(scope="session")
def api() -> RayhunterApi:
    """Single RayhunterApi instance shared across the entire test session."""
    return RayhunterApi(hostname=HOSTNAME, port=PORT)


@pytest.fixture(scope="session")
def recorded_filenames() -> list[str]:
    """
    Mutable list shared across test modules.
    Populated by the recording tests, consumed by the download and deletion tests.
    """
    return []


@pytest.fixture(scope="session")
def config_state() -> dict:
    """
    Mutable dict shared across configuration tests.
    Stores the original Config under the key "original" before any modifications are made.
    """
    return {"original": None}
