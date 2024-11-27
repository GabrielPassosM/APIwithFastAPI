from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from contexts.players.models import Player
from contexts.players.routers.api_schemas import PlayerCreate
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

    # TODO do better
    player.name = player_info.name
    player.position = player_info.position
    player.image_url = player_info.image_url
    player.goals = player_info.goals
    player.assists = player_info.assists
    player.mvps = player_info.mvps
    player.yellow_cards = player_info.yellow_cards
    player.red_cards = player_info.red_cards
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
