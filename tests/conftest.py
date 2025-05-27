
from fastapi.testclient import TestClient

from fastapi_zero.app import app

import pytest


@pytest.fixture
def client():
    return TestClient(app)
