import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session


DATABASE_FILE = "test_database.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=Session
)


def init_test_db():
    SQLModel.metadata.create_all(engine)


@pytest.fixture(autouse=True)
def clean_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def remove_test_db():
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)


def get_testing_session():
    with TestingSessionLocal() as session:
        yield session
