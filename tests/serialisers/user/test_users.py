"""Serialisers Module: Testing User Serialiser."""

import json

from pytest import raises
from sqlalchemy.orm import Session

from config import AppConfig
from lib.interfaces.exceptions import UserError
from lib.utils.constants.users import Status
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from serialisers.user.users import UserSerialiser
from models import ENGINE
from models.user.users import User
from tests.conftest import get_id_by_regex, run_test_teardown


def test_userserialiser_create(email, password):
    """Testing User Serialiser: Create User."""

    with Session(ENGINE) as session:
        user = UserSerialiser().create_user(email, password)
        user_id = get_id_by_regex(user)

        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        assert user.id is not None
        run_test_teardown(user.id, User, session)


def test_userserialiser_create_invalid_email():
    """Testing User Serialiser: Invalid Create User [Email]."""

    with raises(UserError):
        UserSerialiser().create_user("email", "password")


def test_userserialiser_get(app, user):
    """Testing User Serialiser: Get User."""

    user = UserSerialiser().get_user(user.user_id)
    user_data = json.loads(app.fernet.decrypt(user.encode()).decode())

    assert isinstance(user_data, dict)
    for key in user_data:
        assert key not in User.__EXCLUDE_ATTRIBUTES__


def test_userserialiser_get_invalid():
    """Testing User Serialiser: Invalid Get User."""

    with raises(UserError):
        UserSerialiser().get_user("id")


def test_userserialiser_delete(user):
    """Testing User Serialiser: Delete User."""

    UserSerialiser().delete_user(user.id)


def test_userserialiser_delete_invalid():
    """Testing User Serialiser: Invalid Delete User."""

    with raises(UserError):
        UserSerialiser().delete_user("id")


def test_userserialiser_update_valid(user):
    """Testing User Serialiser: Update User [PASSWORD]."""

    with Session(ENGINE) as session:
        UserSerialiser().update_user(
            user.id, password="password123@2", status=Status.ACTIVE
        )
        user = session.get(User, user.id)

        assert user.id is not None
        assert user.password == str(get_hash_value("password123@2", user.salt_value))
        assert user.status == Status.ACTIVE


def test_userserialiser_update_invalid_type(user):
    """Testing User Serialiser: Invalid Update User [PASSWORD]."""

    with raises(UserError):
        UserSerialiser().update_user(
            user.id, password="password", status=Status.DISABLED
        )
        UserSerialiser().update_user(
            user.id, password="password", status="Status.DISABLED"
        )
        UserSerialiser().update_user("user_data.id")
