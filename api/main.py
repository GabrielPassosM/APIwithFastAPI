import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from contexts.players.routers import players
from infra.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="API made with FastAPI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(players.router)


@app.get("/", status_code=200)
async def index():
    return {"Hello": "World"}


@app.get("/status", status_code=200)
async def status():
    return {"python_version": sys.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
