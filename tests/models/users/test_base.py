"""Base Test Module testing the User Abstract Class"""

from pytest import raises

from lib.interfaces.types import UserEmailError, UserPasswordError
from models.user.users import User


def test_base_user_valid():
    """Test Valid User Data."""
    user = User("test@test.com", "test@test123")
    with raises(AttributeError):
        assert user.__email and user.__password
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
        user = User("TEST@TEST.COM", None)
