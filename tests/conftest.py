"""App Module: Testing Configuration."""

from typing import Any
from pytest import fixture
from sqlalchemy.orm import Session
from config import AppConfig


@fixture
def app() -> AppConfig:
    """Initializes the Application Config."""
    return AppConfig()


@fixture
def email() -> str:
    """Initializes the Test Email."""
    return "testing123@test.com"


@fixture
def password() -> str:
    """Initializes the Test Email."""
    return "testing@123"

@fixture
def name() -> str:
    """Initializes the Test Name."""
    return "testing123"


@fixture
def description() -> str:
    """Initializes the Test Description."""
    return "Longer Description for testing 123."


def setup_test_commit(model: Any, session: Session):
    """Abstraction of the persistence functionality.

    Args:
        model (Model): Model to Persist
        session (Session): Database Session
    """
    session.add(model)
    session.commit()


def run_test_teardown(private_id: str, model: Any, session: Session):
    """Abstraction of the Clearing of the Test Database.

    Args:
        private_id (str): Model Private ID.
        model (Model): Model to Persist
        session (Session): Database Session
    """
    model = session.get(model, private_id)
    session.delete(model)
    session.commit()
