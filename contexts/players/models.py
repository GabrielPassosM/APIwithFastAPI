from enum import Enum

from sqlmodel import SQLModel, Field

from libs.base_types.uuid import BaseUUID


class PlayerPosition(Enum):
    GOALKEEPER = "goalkeeper"
    DEFENDER = "defender"
    MIDFIELDER = "midfielder"
    FORWARD = "forward"


class Player(SQLModel, table=True):
    id: BaseUUID = Field(default_factory=BaseUUID, primary_key=True)
    name: str
    shirt_number: int = Field(default=0)
    position: PlayerPosition
    image_url: str = Field(nullable=True, default=None)
    goals: int = Field(default=0)
    assists: int = Field(default=0)
    mvps: int = Field(default=0)
    yellow_cards: int = Field(default=0)
    red_cards: int = Field(default=0)
