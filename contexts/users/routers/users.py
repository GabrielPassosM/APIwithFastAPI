import os

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from contexts.users.models import User
from contexts.users.routers.api_schemas import UserCreate
from infra.database import get_session
from libs.base_types.uuid import BaseUUID
from passlib.context import CryptContext

router = APIRouter(tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/users/{api_secret}", status_code=200)
async def get_users(
    api_secret: str,
    session: Session = Depends(get_session),
) -> list[User]:
    if api_secret != os.getenv("USER_API_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid api secret")

    users = session.exec(select(User)).all()
    return users


@router.get("/users/{user_id}/{api_secret}", status_code=200)
async def get_user(
    user_id: BaseUUID,
    api_secret: str,
    session: Session = Depends(get_session),
) -> User | None:
    if api_secret != os.getenv("USER_API_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid api secret")

    user = session.exec(select(User).where(User.id == user_id)).first()
    return user


@router.post("/user/{api_secret}", status_code=201)
async def create_user(
    api_secret: str,
    user_info: UserCreate,
    session: Session = Depends(get_session),
) -> User:
    if api_secret != os.getenv("USER_API_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid api secret")

    user_info.password = pwd_context.hash(user_info.password)
    user = User(**user_info.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/user/{user_id}/{api_secret}", status_code=200)
async def delete_user(
    user_id: BaseUUID,
    api_secret: str,
    session: Session = Depends(get_session),
) -> None:
    if api_secret != os.getenv("USER_API_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid api secret")

    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return None
    session.delete(user)
    session.commit()
