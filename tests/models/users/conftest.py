"""_summary_"""

from typing import Union
from os import getenv
from pytest import fixture
from models.user.users import User


def user_test_commit(user, session):
    """_summary_

    Args:
        user (_type_): _description_
        session (_type_): _description_
    """
    session.add(user)
    session.commit()


def user_test_teardown(user_id, entity, session):
    """_summary_

    Args:
        id (_type_): _description_
        entity (_type_): _description_
        session (_type_): _description_
    """
    user = session.get(entity, user_id)
    session.delete(user)
    session.commit()


@fixture
def get_user() -> User:
    """_summary_

    Returns:
        User: _description_
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
