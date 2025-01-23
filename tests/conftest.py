import os

import pytest

from api.main import app
from contexts.players.models import Player, PlayerPosition
from contexts.users.models import User
from infra.database import get_session
from tests.database import (
    get_testing_session,
    init_test_db,
    remove_test_db,
    clean_db,
)  # noqa: F401


os.environ["ISPYTEST"] = "true"


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_test_db()
    yield
    remove_test_db()


@pytest.fixture(scope="function")
def mock_user():
    mock = User(email="teste@teste.com", password="1234")
    session = next(get_testing_session())
    session.add(mock)
    session.commit()
    session.refresh(mock)
    yield mock


@pytest.fixture(scope="function")
def mock_player():
    mock = Player(
        name="Teste",
        shirt_number=10,
        position=PlayerPosition.MIDFIELDER,
    )
    session = next(get_testing_session())
    session.add(mock)
    session.commit()
    session.refresh(mock)
    yield mock


app.dependency_overrides[get_session] = lambda: next(get_testing_session())
