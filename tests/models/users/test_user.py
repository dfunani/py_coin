"""Base Test Module testing the User Abstract Class"""

from json import loads
from pytest import raises
from sqlalchemy.orm import Session
from config import AppConfig
from lib.interfaces.exceptions import UserEmailError, UserPasswordError
from models import ENGINE
from models.user.users import User
from tests.models.users.conftest import user_test_commit, user_test_teardown


def test_base_user_valid():
    """Test Valid User Data."""
    user = User("test@test.com", "test@test123")
    with raises(AttributeError):
        assert user.get("__email") and user.get("__password")


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


def test_create_user(get_user):
    """_summary_

    Args:
        get_user (_type_): _description_
        fkey (_type_): _description_
    """
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)
        user_data = loads(AppConfig().fernet.decrypt(get_user.user_data.encode()))

        assert "id" in user_data and user_data.get("id")
        assert "email" in user_data and user_data.get("email")
        assert "password" in user_data and user_data.get("password")
        assert "salt_value" in user_data and user_data.get("salt_value")

        user_test_teardown(user_data.get("id"), User, session)
