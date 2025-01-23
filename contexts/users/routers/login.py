from dataclasses import dataclass

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlmodel import Session, select

from contexts.users.models import User
from contexts.users.routers.api_schemas import LoginInfo, LoginReturn
from infra.database import get_session
from libs.exceptions.basis_exception import BasisException


router = APIRouter(tags=["Login"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class _EmailNotFound(BasisException):
    status_code: int = 401
    detail: str = "Não existe usuário com esse e-mail"


@dataclass
class _WrongPassword(BasisException):
    status_code: int = 401
    detail: str = "Senha inválida"


@router.post("/login", status_code=200)
async def login(
    login_info: LoginInfo,
    session: Session = Depends(get_session),
) -> LoginReturn:
    user = session.exec(select(User).where(User.email == login_info.email)).first()
    if not user:
        raise _EmailNotFound()

    if not pwd_context.verify(login_info.password, user.password):
        raise _WrongPassword()

    # TODO Using id to authenticate for now. Implement jwt later
    return LoginReturn(email=user.email, id=user.id)
