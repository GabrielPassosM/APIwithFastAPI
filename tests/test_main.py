from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["db_status"]["status"] == "ready"
    assert data["python_version"] not in [None, ""]


def test_database_check():
    response = client.get("/database-check")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
