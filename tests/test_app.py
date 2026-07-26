from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    data = activities_response.json()
    assert email not in data[activity_name]["participants"]


def test_unregister_unknown_participant_returns_error():
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "missing.student@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not found for this activity"
