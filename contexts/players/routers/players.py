from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from contexts.players.models import Player
from contexts.players.routers.api_schemas import PlayerBase, PlayerCreate
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
) -> BaseUUID:
    player = Player(**player_info.model_dump())
    session.add(player)
    session.commit()
    session.refresh(player)
    return player.id


@router.put("/player/{player_id}", status_code=200)
async def update_player(
    player_id: BaseUUID,
    player_info: PlayerCreate,
    session: Session = Depends(get_session),
) -> Player | None:
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        return None
    player.name = player_info.name
    player.category = player_info.category
    player.quantity = player_info.quantity
    player.image_url = player_info.image_url
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
