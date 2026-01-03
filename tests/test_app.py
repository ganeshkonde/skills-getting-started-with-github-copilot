from fastapi.testclient import TestClient
from urllib.parse import quote

from src import app as app_module

client = TestClient(app_module.app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "pytest_user@example.com"
    activity = "Programming Class"

    # ensure clean state
    participants = app_module.activities[activity]["participants"]
    if email in participants:
        participants.remove(email)

    path = f"/activities/{quote(activity)}/signup?email={quote(email)}"
    r = client.post(path)
    assert r.status_code == 200
    json_data = r.json()
    assert "Signed up" in json_data.get("message", "")
    assert email in app_module.activities[activity]["participants"]


def test_signup_nonexistent_activity():
    r = client.post("/activities/ThisDoesNotExist/signup?email=foo@example.com")
    assert r.status_code == 404


def test_duplicate_signup():
    email = "duplicate@example.com"
    activity = "Programming Class"

    participants = app_module.activities[activity]["participants"]
    # ensure email is present
    if email not in participants:
        participants.append(email)

    path = f"/activities/{quote(activity)}/signup?email={quote(email)}"
    r = client.post(path)
    assert r.status_code == 400
