from pydantic import BaseModel, field_validator

from contexts.players.models import PlayerPosition


class _PlayerBase(BaseModel):
    name: str
    position: PlayerPosition
    image_url: str = None
    goals: int = 0
    assists: int = 0
    mvps: int = 0
    yellow_cards: int = 0
    red_cards: int = 0


class PlayerCreate(_PlayerBase):
    @field_validator("position", mode="before")
    @classmethod
    def validate_position(cls, value):
        return value.lower()
