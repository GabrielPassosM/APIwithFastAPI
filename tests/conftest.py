import os

import pytest

from api.main import app
from infra.database import get_session
from tests.database import get_testing_session, init_test_db, remove_test_db


os.environ["ISPYTEST"] = "true"


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_test_db()
    yield
    remove_test_db()


app.dependency_overrides[get_session] = lambda: next(get_testing_session())
