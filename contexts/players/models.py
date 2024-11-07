from enum import Enum

from sqlmodel import SQLModel, Field

from libs.base_types.uuid import BaseUUID


class Category(Enum):
    ARTILHEIROS = "artilheiros"
    ASSISTENTES = "assistentes"
    MVPS = "mvps"
    CARTOES_AMARELOS = "cartoes-amarelos"
    CARTOES_VERMELHOS = "cartoes-vermelhos"


class Player(SQLModel, table=True):
    id: BaseUUID = Field(default_factory=BaseUUID, primary_key=True)
    name: str
    category: Category
    quantity: int
    image_url: str
