from pydantic import BaseModel

from libs.base_types.email_address import EmailAddress
from libs.base_types.password import Password
from libs.base_types.uuid import BaseUUID


class UserCreate(BaseModel):
    email: EmailAddress
    password: Password


class LoginInfo(UserCreate):
    pass


class LoginReturn(BaseModel):
    email: EmailAddress
    id: BaseUUID
