import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

def test_get_activities():
    client = TestClient(app)
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    client = TestClient(app)
    activity_name = "Math Olympiad"
    email = "testuser@mergington.edu"
    # 事前に参加していないことを確認
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)
    # サインアップ
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    # 削除
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    # 2回目の削除は404
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 404
