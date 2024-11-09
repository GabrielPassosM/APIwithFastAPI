import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

load_dotenv()

def test_run_migration():
    response = client.post(f"/run-migration/{os.getenv('MIGRATION_PWD')}")
    assert response.status_code == 200
    assert response.json() == {"message": "Migration applied successfully"}
