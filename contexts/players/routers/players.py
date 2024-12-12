from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from contexts.players.models import Player
from contexts.players.routers.api_schemas import PlayerCreate, PlayerIncrementStats
from infra.database import get_session
from libs.base_types.uuid import BaseUUID

router = APIRouter(tags=["Players"])


@router.get("/players", status_code=200)
async def get_players(
    session: Session = Depends(get_session),
) -> list[Player]:
    players = session.exec(select(Player)).all()
    return players


@router.get("/players/{player_id}", status_code=200)
async def get_player(
    player_id: BaseUUID,
    session: Session = Depends(get_session),
) -> Player | None:
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    return player


@router.post("/player", status_code=201)
async def create_player(
    player_info: PlayerCreate,
    session: Session = Depends(get_session),
) -> Player:
    player = Player(**player_info.model_dump())
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


@router.put("/player/{player_id}", status_code=200)
async def update_player(
    player_id: BaseUUID,
    player_info: PlayerCreate,
    session: Session = Depends(get_session),
) -> Player | None:
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        return None

    player_info: dict = player_info.model_dump()

    # check if there is any change
    if all(getattr(player, campo) == valor for campo, valor in player_info.items()):
        return

    for campo, valor in player_info.items():
        setattr(player, campo, valor)

    session.commit()
    session.refresh(player)
    return player


@router.put("/player/increment/{player_id}", status_code=200)
async def increment_player_stats(
    player_id: BaseUUID,
    increment_info: PlayerIncrementStats,
    session: Session = Depends(get_session),
) -> Player | None:
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        return None

    increment_info: dict = increment_info.model_dump()
    for campo, valor in increment_info.items():
        setattr(player, campo, getattr(player, campo) + valor)

    session.commit()
    session.refresh(player)
    return player


@router.delete("/player/{player_id}", status_code=200)
async def delete_player(
    player_id: BaseUUID,
    session: Session = Depends(get_session),
) -> None:
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        return None
    session.delete(player)
    session.commit()
