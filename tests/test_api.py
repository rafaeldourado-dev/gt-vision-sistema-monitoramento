import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/api/")
    assert response.status_code == 200
    assert "GT-VISION Dashboard" in response.text

def test_get_alerts():
    response = client.get("/api/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)