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


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    email = "test1@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    email = "test2@mergington.edu"
    # First signup
    client.post(f"/activities/Chess Club/signup?email={email}")
    # Duplicate signup
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
