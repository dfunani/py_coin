"""_summary_"""

from os import getenv
from pytest import fixture
from models.user.users import User


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
def fkey() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    return getenv("FERNET_KEY")
    