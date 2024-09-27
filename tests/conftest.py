import pytest
from starlette.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app=app)
