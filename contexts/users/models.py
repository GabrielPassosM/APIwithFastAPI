from sqlmodel import SQLModel, Field

from libs.base_types.uuid import BaseUUID


class User(SQLModel, table=True):
    id: BaseUUID = Field(default_factory=BaseUUID, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
