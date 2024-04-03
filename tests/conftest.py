"""App Module: Testing Configuration."""

from pytest import fixture
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


def user_test_commit(object, session):
    """Abstraction of the persistence functionality.

    Args:
        entity (Model): Model to Persist
        session (Session): Database Session
    """
    session.add(object)
    session.commit()


def user_test_teardown(model_id, model, session):
    """Abstraction of the Clearing of the Test Database.

    Args:
        model (Model): Model to Persist
        session (Session): Database Session
    """
    model = session.get(model, model_id)
    session.delete(model)
    session.commit()
