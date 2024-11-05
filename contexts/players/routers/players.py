from fastapi import APIRouter

from contexts.players.routers.api_schemas import PlayerBase, PlayerCreate


router = APIRouter(tags=["Players"])

"""Mock for now"""
PLAYERS_MOCK = [
    {
        "id": 1,
        "name": "player1",
        "category": "artilheiros",
        "quantity": 10,
        "image_url": "https://example.com/image.jpg",
    },
    {
        "id": 2,
        "name": "player2",
        "category": "assistentes",
        "quantity": 5,
        "image_url": "https://example.com/image.jpg",
    },
    {
        "id": 3,
        "name": "player3",
        "category": "artilheiros",
        "quantity": 7,
        "image_url": "https://example.com/image.jpg",
    },
    {
        "id": 4,
        "name": "player4",
        "category": "mvps",
        "quantity": 8,
        "image_url": "https://example.com/image.jpg",
    },
    {
        "id": 5,
        "name": "player5",
        "category": "cartoes-amarelos",
        "quantity": 9,
        "image_url": "https://example.com/image.jpg",
    },
]


@router.get("/players", status_code=200)
async def get_players() -> list[PlayerBase]:
    """Mock for now"""
    return [PlayerBase(**player) for player in PLAYERS_MOCK]


@router.get("/players/{player_id}", status_code=200)
async def get_player(player_id: int) -> PlayerBase | None:
    """Mock for now"""
    player = next(
        (PlayerBase(**player) for player in PLAYERS_MOCK if player["id"] == player_id),
        None,
    )
    return player


@router.post("/player", status_code=201)
async def create_player(player: PlayerCreate) -> int:
    """Mock for now"""
    id = PLAYERS_MOCK[-1]["id"] + 1
    player = player.model_dump()
    player["id"] = id
    PLAYERS_MOCK.append(player)
    return id


@router.put("/player/{player_id}", status_code=200)
async def update_player(player_id: int, player: dict):
    """Mock for now"""
    return player


@router.delete("/player/{player_id}", status_code=200)
async def delete_player(player_id: int):
    """Mock for now"""
    return {"deleted": player_id}
