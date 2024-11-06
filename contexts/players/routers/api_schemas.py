from pydantic import BaseModel, field_validator

from contexts.players.models import Category


class PlayerBase(BaseModel):
    name: str
    category: Category
    quantity: int
    image_url: str


class PlayerCreate(PlayerBase):
    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value):
        return value.lower()
