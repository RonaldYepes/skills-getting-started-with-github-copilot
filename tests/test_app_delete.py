import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory DB before each test
    for activity in activities.values():
        if isinstance(activity["participants"], list):
            activity["participants"] = [p for p in activity["participants"] if p.endswith("@mergington.edu")]

def test_delete_participant_success(monkeypatch):
    # Primero, registrar un participante
    email = "delete_test@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    assert email in activities[activity]["participants"]

    # Implementar el endpoint DELETE antes de que este test pase
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_delete_participant_not_found():
    response = client.delete("/activities/Chess Club/signup?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
