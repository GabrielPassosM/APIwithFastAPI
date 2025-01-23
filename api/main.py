import os
import sys

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlmodel import Session

from contexts.players.routers import players
from contexts.users.routers import users
from infra.database import get_session

app = FastAPI(
    title="API made with FastAPI",
    version="0.1.0",
)

app.include_router(players.router)
app.include_router(users.router)

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
async def status(session: Session = Depends(get_session)):
    db_status = await _check_db_connection(session)
    return {
        "python_version": sys.version,
        "db_status": db_status,
    }


@app.get("/database-check")
async def database_check(session: Session = Depends(get_session)):
    return await _check_db_connection(session)


async def _check_db_connection(session: Session) -> dict:
    try:
        session.exec(text("SELECT 1"))
    except OperationalError:
        return {"status": "waiting connection"}
    return {"status": "ready"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
