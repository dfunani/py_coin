"""Base Test Module testing the User Abstract Class"""

from json import loads
from pytest import raises
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from lib.interfaces.types import UserEmailError, UserPasswordError
from models import ENGINE
from models.user.users import User
from tests.models.users.conftest import user_test_commit, user_test_teardown


def test_base_user_valid():
    """Test Valid User Data."""
    user = User("test@test.com", "test@test123")
    with raises(AttributeError):
        assert user.get("__email") and user.get("__password")
    with raises(UserEmailError):
        assert user.email
    with raises(UserPasswordError):
        assert user.password


def test_base_user_invalid_email():
    """Test invalid Email. Invalid Email Provided."""
    with raises(UserEmailError):
        User("test/test.com", "test@test123")


def test_base_user_invalid_password():
    """Test Invalid Password. Invalid Password Provided."""
    with raises(UserPasswordError):
        User("test@test.com", "testpassword")


def test_base_user_no_email():
    """Test Invalid User Email. No Email Provided."""
    with raises(UserEmailError):
        User(None, "test")


def test_base_user_no_password():
    """Test Invalid User Password. No Email Provided."""
    with raises(UserPasswordError):
        User("TEST@TEST.COM", None)


def test_create_user(get_user, fkey):
    """_summary_

    Args:
        get_user (_type_): _description_
        fkey (_type_): _description_
    """
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)
        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))

        assert "id" in user_data and user_data.get("id")

        user_test_teardown(user_data.get("id"), User, session)
