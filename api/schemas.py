from enum import Enum

from pydantic import BaseModel, field_validator


class Category(Enum):
    ARTILHEIROS = "artilheiros"
    ASSISTENTES = "assistentes"
    MVPS = "mvps"
    CARTOES_AMARELOS = "cartoes-amarelos"
    CARTOES_VERMELHOS = "cartoes-vermelhos"


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
