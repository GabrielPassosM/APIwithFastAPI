from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_run_migration():
    response = client.post("/run-migration")
    # assert response.content == "oi"
    assert response.status_code == 200
    assert response.json() == {"message": "Migration applied successfully"}
