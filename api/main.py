import sys

from fastapi import FastAPI

from contexts.players.resources import players_router


app = FastAPI(
    title="API made with FastAPI",
    version="0.1.0",
)

app.include_router(players_router)


@app.get("/", status_code=200)
async def index():
    return {"Hello": "World"}


@app.get("/status", status_code=200)
async def status():
    return {"python_version": sys.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
