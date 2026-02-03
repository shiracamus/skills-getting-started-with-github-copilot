import pytest
from fastapi.testclient import TestClient
from app import app, activities

def test_remove_participant():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    # 事前に参加者がいることを確認
    assert email in activities[activity_name]["participants"]
    # 削除APIを呼び出し
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Removed {email} from {activity_name}"
    # 参加者が削除されていることを確認
    assert email not in activities[activity_name]["participants"]
    # もう一度削除しようとすると404
    response2 = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response2.status_code == 404
    assert response2.json()["detail"] == "Participant not found in this activity"
