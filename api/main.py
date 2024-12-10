import os
import sys

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from contexts.players.routers import players


app = FastAPI(
    title="API made with FastAPI",
    version="0.1.0",
)

app.include_router(players.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4173",
        "https://tribunata-git-staging-gabriel-martins-projects-3f4ed294.vercel.app",
        "https://tribunata.vercel.app",
        "https://tribunata-v2.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _run_migration():
    alembic_cfg_path = os.path.join("infra", "alembic.ini")
    alembic_cfg = Config(alembic_cfg_path)

    command.upgrade(alembic_cfg, "head")


@app.post("/run-migration/{password}", status_code=200)
async def run_db_migration(password: str):
    if password != os.getenv("MIGRATION_PWD"):
        raise HTTPException(status_code=401, detail="Invalid password")

    try:
        _run_migration()
        return {"message": "Migration applied successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Migration error: {str(e)}")


@app.get("/", status_code=200)
async def index():
    return {"Hello": "World"}


@app.get("/status", status_code=200)
async def status():
    return {"python_version": sys.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
