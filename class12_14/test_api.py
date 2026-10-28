import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
def test_requests_have_different_ids(client):
    # TODO: send two GET /health requests.
    # Assert that their X-Request-ID header values are different.
    first = client.get("/health")
    second = client.get("/health")
    
    id1 = first.headers["X-Request-ID"]
    id2 = second.headers["X-Request-ID"]
    
    assert id1 != id2