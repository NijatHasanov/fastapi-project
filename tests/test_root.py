import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import create_access_token

client = TestClient(app)

@pytest.fixture
def admin_token():
    return create_access_token({"sub": "test_admin"})

@pytest.fixture
def viewer_token():
    return create_access_token({"sub": "test_viewer"})

def test_root_endpoint_with_auth(admin_token):
    response = client.get("/", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_root_endpoint_without_auth():
    response = client.get("/")
    assert response.status_code == 401

def test_create_room_data(admin_token):
    room_data = {
        "room_id": "test_room",
        "temperature": 23.5,
        "occupancy": 5,
        "humidity": 45.0
    }
    response = client.post(
        "/api/v1/data",
        json=room_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["room_id"] == "test_room"

def test_get_all_room_data(viewer_token):
    response = client.get(
        "/api/v1/data/all",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
