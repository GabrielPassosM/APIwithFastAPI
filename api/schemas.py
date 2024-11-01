from enum import Enum

from pydantic import BaseModel


class Category(Enum):
    ARTILHEIROS = "artilheiros"
    ASSISTENTES = "assistentes"
    MVPS = "mvps"
    CARTOES_AMARELOS = "cartoes-amarelos"
    CARTOES_VERMELHOS = "cartoes-vermelhos"


class Player(BaseModel):
    id: int
    name: str
    category: Category
    quantity: int
    image_url: str
