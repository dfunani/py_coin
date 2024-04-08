"""Serialisers Module: Testing User Serialiser."""

import json
from re import compile as regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.utils.constants.users import Status
from serialisers.user.users import UserSerialiser
from lib.interfaces.exceptions import UserEmailError, UserError, UserPasswordError
from models import ENGINE
from models.user.users import User
from tests.conftest import run_test_teardown


def test_userserialiser_create(email, password):
    """Testing User Serialiser: Create User."""
    user = UserSerialiser().create_user(email, password)
    regex = regex_compile(r"^User ID: (.*)$")
    regex_match = regex.match(user)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    user_id = matches[0]
    with Session(ENGINE) as session:
        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        run_test_teardown(user.id, User, session)


def test_userserialiser_get(email, password, app, user_keys):
    """Testing User Serialiser: Get User."""
    UserSerialiser().create_user(email, password)

    user_id = UserSerialiser().get_validated_user_id(email, password)
    user = UserSerialiser().get_user(user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())

    assert isinstance(user_data, dict)
    for key in user_keys:
        assert key in user_data
        assert user_data[key] is not None

    for key in user_data:
        assert key in user_keys

    with Session(ENGINE) as session:
        run_test_teardown(user_data["id"], User, session)


def test_userserialiser_delete(email, password, app):
    """Testing User Serialiser: Delete User."""
    UserSerialiser().create_user(email, password)
    user_id = UserSerialiser().get_validated_user_id(email, password)
    user = UserSerialiser().get_user(user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())
    UserSerialiser().delete_user(user_data.get("id"))


def test_userserialiser_update_valid_password(email, password, app):
    """Testing User Serialiser: Update User."""
    UserSerialiser().create_user(email, password)
    user_id = UserSerialiser().get_validated_user_id(email, password)
    user = UserSerialiser().get_user(user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())
    UserSerialiser().update_user(user_data.get("id"), password=password)
    UserSerialiser().delete_user(user_data.get("id"))

def test_userserialiser_update_valid_user_status(email, password, app):
    """Testing User Serialiser: Update User."""
    UserSerialiser().create_user(email, password)
    user_id = UserSerialiser().get_validated_user_id(email, password)
    user = UserSerialiser().get_user(user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())
    UserSerialiser().update_user(user_data.get("id"), user_status=Status.ACTIVE)
    UserSerialiser().delete_user(user_data.get("id"))


def test_userserialiser_create_invalid_email(password):
    """Testing User Serialiser: Invalid Create User [Email]."""
    with raises(UserEmailError):
        UserSerialiser().create_user("email", password)


def test_userserialiser_create_invalid_password(email):
    """Testing User Serialiser: Invalid Create User [Password]."""
    with raises(UserPasswordError):
        UserSerialiser().create_user(email, "password")


def test_userserialiser_get_invalid_email(password):
    """Testing User Serialiser: Invalid Get User [Email]."""
    with raises(UserEmailError):
        user_id = UserSerialiser().get_validated_user_id("email", password)
        UserSerialiser().get_user(user_id)


def test_userserialiser_get_invalid_password(email):
    """Testing User Serialiser: Invalid Get User [Password]."""
    with raises(UserPasswordError):
        user_id = UserSerialiser().get_validated_user_id(email, "password")
        UserSerialiser().get_user(user_id)


def test_userserialiser_get_invalid(email, password):
    """Testing User Serialiser: Invalid Get User."""
    with raises(UserError):
        user_id = UserSerialiser().get_validated_user_id(email, password)
        UserSerialiser().get_user(user_id)


def test_userserialiser_update_invalid():
    """Testing User Serialiser: Invalid Update User."""
    with raises(UserError):
        UserSerialiser().update_user("id")


def test_userserialiser_update_invalid_password(email, password, app):
    """Testing User Serialiser: Invalid Update User [Password]."""
    UserSerialiser().create_user(email, password)
    user_id = UserSerialiser().get_validated_user_id(email, password)
    user = UserSerialiser().get_user(user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())
    with raises(UserPasswordError):
        UserSerialiser().update_user(user_data.get("id"), password="password")
    UserSerialiser().delete_user(user_data.get("id"))


def test_userserialiser_update_invalid_kwarg(email, password, app):
    """Testing User Serialiser: Invalid Update User [Password]."""
    UserSerialiser().create_user(email, password)
    user_id = UserSerialiser().get_validated_user_id(email, password)
    user = UserSerialiser().get_user(user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())
    with raises(UserError):
        UserSerialiser().update_user(user_data.get("id"), email="email@test.com")
    UserSerialiser().delete_user(user_data.get("id"))


def test_userserialiser_update_invalid_kwarg_disabled(email, password, app):
    """Testing User Serialiser: Invalid Update User [Password]."""
    UserSerialiser().create_user(email, password)
    user_id = UserSerialiser().get_validated_user_id(email, password)
    user = UserSerialiser().get_user(user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())
    with raises(UserError):
        UserSerialiser().update_user(user_data.get("id"), user_status=Status.DISABLED)
    UserSerialiser().delete_user(user_data.get("id"))

def test_userserialiser_delete_invalid():
    """Testing User Serialiser: Invalid Delete User."""
    with raises(UserError):
        UserSerialiser().delete_user("id")


def test_userserialiser_get_validated_user_id_invalid_email(password):
    """Testing User Serialiser: Invalid User ID [Email]."""
    with raises(UserEmailError):
        UserSerialiser().get_validated_user_id("email", password)


def test_userserialiser_get_validated_user_id_invalid_password(email):
    """Testing User Serialiser: Invalid User ID [Password]."""
    with raises(UserPasswordError):
        UserSerialiser().get_validated_user_id(email, "password")
