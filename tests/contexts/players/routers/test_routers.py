from fastapi.testclient import TestClient
from api.main import app
from libs.base_types.uuid import BaseUUID

client = TestClient(app)


def test_get_players():
    response = client.get("/players")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# TODO fix this test
# def test_get_player():
#     # hardcoded player id mock for now
#     response = client.get("/players/1")
#     assert response.status_code == 200
#     assert response.json()["name"] == "player1"


def test_post_player():
    data = {
        "name": "Player X",
        "position": "goalkeeper",
        "image_url": "https://example.com/image.jpg",
        "red_cards": 1,
    }
    response = client.post("/player", json=data)
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert "id" in response.json()
