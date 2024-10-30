from fastapi import FastAPI

app = FastAPI(
    title="API made with FastAPI",
    version="0.1.0",
)


@app.get("/", status_code=200)
def read_root():
    return {"Hello": "World"}


@app.get("/players", status_code=200)
def get_players():
    """Mock for now"""
    return {"players": ["player1", "player2", "player3"]}


@app.get("/player/{player_id}", status_code=200)
def get_player(player_id: int):
    """Mock for now"""
    return {"player": player_id}


@app.post("/player", status_code=200)
def create_player(player: dict):
    """Mock for now"""
    return player


@app.put("/player/{player_id}", status_code=200)
def update_player(player_id: int, player: dict):
    """Mock for now"""
    return player


@app.delete("/player/{player_id}", status_code=200)
def delete_player(player_id: int):
    """Mock for now"""
    return {"deleted": player_id}
