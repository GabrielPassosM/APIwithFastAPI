from dataclasses import dataclass

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from contexts.players.models import Player
from contexts.players.routers.api_schemas import PlayerCreate, PlayerIncrementStats
from contexts.users.models import User
from infra.database import get_session
from libs.base_types.uuid import BaseUUID
from libs.datetime import utcnow
from libs.exceptions.basis_exception import BasisException


router = APIRouter(tags=["Players"])


@dataclass
class _UserNotLogged(BasisException):
    status_code: int = 401
    detail: str = "Precisa estar logado para realizar essa ação"


def _verify_user(session: Session, user_id: BaseUUID) -> None:
    if not user_id or not __get_user(session, user_id):
        raise _UserNotLogged()


def __get_user(session: Session, user_id: BaseUUID) -> User | None:
    user = session.exec(select(User).where(User.id == user_id)).first()
    return user


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
    _verify_user(session, player_info.user_id)

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
    del player_info["user_id"]

    # check if there is any change
    if all(getattr(player, campo) == valor for campo, valor in player_info.items()):
        return

    for campo, valor in player_info.items():
        setattr(player, campo, valor)
    player.updated_at = utcnow()

    session.commit()
    session.refresh(player)
    return player


@router.put("/player/increment/{player_id}", status_code=200)
async def increment_player_stats(
    player_id: BaseUUID,
    increment_info: PlayerIncrementStats,
    session: Session = Depends(get_session),
) -> Player | None:
    _verify_user(session, increment_info.user_id)

    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        return None

    increment_info: dict = increment_info.model_dump()
    del increment_info["user_id"]
    for campo, valor in increment_info.items():
        setattr(player, campo, getattr(player, campo) + valor)
    player.updated_at = utcnow()

    session.commit()
    session.refresh(player)
    return player


@router.delete("/player/{player_id}/{user_id}", status_code=200)
async def delete_player(
    player_id: BaseUUID,
    user_id: BaseUUID,
    session: Session = Depends(get_session),
) -> None:
    _verify_user(session, user_id)

    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        return None
    session.delete(player)
    session.commit()
