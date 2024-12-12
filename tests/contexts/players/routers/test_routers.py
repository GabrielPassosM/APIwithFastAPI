from fastapi.testclient import TestClient
from sqlmodel import select

from api.main import app
from contexts.players.models import Player, PlayerPosition
from tests.database import TestingSessionLocal

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
        "shirt_number": 1,
        "image_url": "https://example.com/image.jpg",
        "red_cards": 1,
    }
    response = client.post("/player", json=data)
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert "id" in response.json()


def test_update_player():
    with TestingSessionLocal() as session:
        player = Player(name="Lionel Messi", position=PlayerPosition.FORWARD)
        session.add(player)
        session.commit()
        session.refresh(player)

    # 1 - Update some fields
    data = {
        "name": player.name,
        "position": player.position.value,
        "shirt_number": 10,
        "goals": 99,
        "assists": 70,
        "red_cards": 1,
    }

    response = client.put(f"/player/{str(player.id)}", json=data)
    assert response.status_code == 200
    assert response.json()["goals"] == 99
    assert response.json()["assists"] == 70
    assert response.json()["red_cards"] == 1

    with TestingSessionLocal() as session:
        player = session.exec(select(Player).where(Player.id == player.id)).first()
        assert player.goals == 99
        assert player.assists == 70

    # 2 - Send same data, should return None
    response = client.put(f"/player/{str(player.id)}", json=data)
    assert response.status_code == 200
    assert response.json() is None
