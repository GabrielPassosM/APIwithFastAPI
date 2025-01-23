from pydantic import BaseModel

from libs.base_types.email_address import EmailAddress
from libs.base_types.password import Password


class UserCreate(BaseModel):
    email: EmailAddress
    password: Password
