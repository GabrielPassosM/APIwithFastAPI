from typing import Final

from pydantic import BaseModel, field_validator

from contexts.players.models import PlayerPosition
from libs.base_types.numbers import PositiveNumber
from libs.base_types.uuid import BaseUUID

DEFAULT_IMAGE_URL: Final = (
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKu1w7TulWMUKGszjJlb7PDtn0LVSJgGnrog&s"
)


class _UserRequired:
    user_id: BaseUUID = None


class _PlayerStats(BaseModel):
    goals: PositiveNumber = 0
    assists: PositiveNumber = 0
    mvps: PositiveNumber = 0
    yellow_cards: PositiveNumber = 0
    red_cards: PositiveNumber = 0


class _PlayerBase(_PlayerStats):
    name: str
    position: PlayerPosition
    shirt_number: PositiveNumber
    image_url: str = DEFAULT_IMAGE_URL


class PlayerCreate(_PlayerBase, _UserRequired):
    @field_validator("position", mode="before")
    @classmethod
    def validate_position(cls, value):
        return value.lower()

    @field_validator("image_url", mode="before")
    @classmethod
    def validate_image_url(cls, value):
        return value or DEFAULT_IMAGE_URL


class PlayerIncrementStats(_PlayerStats, _UserRequired):
    pass
