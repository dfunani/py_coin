"""Serialisers Module: Testing User Serialiser."""

import json

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import UserError
from lib.utils.constants.users import Status
from serialisers.user.users import UserSerialiser
from models import ENGINE
from models.user.users import User
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit


def test_userserialiser_create(email, password, regex_user):
    """Testing User Serialiser: Create User."""

    with Session(ENGINE) as session:
        user = UserSerialiser().create_user(email, password)
        user_id = get_id_by_regex(regex_user, user)
        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        assert user.id is not None
        run_test_teardown(user.id, User, session)


def test_userserialiser_create_invalid_email(password):
    """Testing User Serialiser: Invalid Create User [Email]."""

    with raises(UserError):
        UserSerialiser().create_user("email", password)


def test_userserialiser_create_invalid_password(email):
    """Testing User Serialiser: Invalid Create User [Password]."""

    with raises(UserError):
        UserSerialiser().create_user(email, "password")


def test_userserialiser_get(get_user, regex_user, user_keys, app):
    """Testing User Serialiser: Get User."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)
        user_id = get_id_by_regex(regex_user, str(get_user))

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


def test_userserialiser_get_invalid(email, password):
    """Testing User Serialiser: Invalid Get User."""

    with raises(UserError):
        UserSerialiser().get_user("id")


def test_userserialiser_delete(get_user, regex_user):
    """Testing User Serialiser: Delete User."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)
        UserSerialiser().delete_user(get_user.id)


def test_userserialiser_delete_invalid():
    """Testing User Serialiser: Invalid Delete User."""

    with raises(UserError):
        UserSerialiser().delete_user("id")


def test_userserialiser_update_valid_password(get_user, password):
    """Testing User Serialiser: Update User [PASSWORD]."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)
        UserSerialiser().update_user(get_user.id, password=password)
        run_test_teardown(get_user.id, User, session)


def test_userserialiser_update_invalid_password(get_user):
    """Testing User Serialiser: Invalid Update User [PASSWORD]."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        with raises(UserError):
            UserSerialiser().update_user(get_user.id, password="password")
        run_test_teardown(get_user.id, User, session)


def test_userserialiser_update_invalid_password_type(get_user):
    """Testing User Serialiser: Invalid Update User [PASSWORD]."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        with raises(UserError):
            UserSerialiser().update_user(get_user.id, password=1)
        run_test_teardown(get_user.id, User, session)


def test_userserialiser_update_valid_user_status(get_user):
    """Testing User Serialiser: Update User [STATUS]."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        UserSerialiser().update_user(get_user.id, status=Status.ACTIVE)
        run_test_teardown(get_user.id, User, session)


def test_userserialiser_update_invalid_user_status(get_user):
    """Testing User Serialiser: Update User [STATUS]."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        with raises(UserError):
            UserSerialiser().update_user(get_user.id, status=Status.DISABLED)
        run_test_teardown(get_user.id, User, session)


def test_userserialiser_update_invalid_user_status_type(get_user):
    """Testing User Serialiser: Update User [STATUS]."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        with raises(UserError):
            UserSerialiser().update_user(get_user.id, status="Status.DISABLED")
        run_test_teardown(get_user.id, User, session)


def test_userserialiser_update_invalid_email(get_user, email):
    """Testing User Serialiser: Update User."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        with raises(TypeError):
            UserSerialiser().update_user(get_user.id, email=email)
        run_test_teardown(get_user.id, User, session)


def test_userserialiser_update_invalid():
    """Testing User Serialiser: Invalid Update User."""

    with raises(TypeError):
        UserSerialiser().update_user("id", id="")
