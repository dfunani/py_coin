"""Test Config Module for Users Modules."""

from typing import Union
from os import getenv
from pytest import fixture
from models.user.users import User


def user_test_commit(model, session):
    """Abstraction of the persistence functionality.

    Args:
        entity (Model): Model to Persist
        session (Session): Database Session
    """
    session.add(model)
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


@fixture
def get_user() -> User:
    """Returns a Test User

    Returns:
        User: Test User.
    """
    return User(
        "never_to_be_used_email_address_its_for_test@test_mail.test",
        "password11313@",
    )


@fixture
def fkey() -> Union[str, None]:
    """_summary_

    Returns:
        str: _description_
    """
    return getenv("FERNET_KEY")
