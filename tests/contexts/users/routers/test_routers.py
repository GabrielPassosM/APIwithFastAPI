import os

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_post_user():
    data = {"email": "teste@gmail.com", "password": "123"}
    response = client.post(f"/user/{os.getenv('USER_API_SECRET')}", json=data)
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert "id" in response.json()


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
