"""App Module: Testing Configuration."""

from typing import Any
from pytest import fixture
from sqlalchemy.orm import Session
from config import AppConfig


@fixture
def app() -> AppConfig:
    """Initializes the Application Config."""

    return AppConfig()


def setup_test_commit(model: Any, session: Session):
    """Abstraction of the persistence functionality."""

    session.add(model)
    session.commit()


def run_test_teardown(private_id: str, model: Any, session: Session):
    """Abstraction of the Clearing of the Test Database."""

    model = session.get(model, private_id)
    session.delete(model)
    session.commit()
