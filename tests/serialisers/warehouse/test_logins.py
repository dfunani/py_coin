"""Serialisers Module: Testing User Serialiser."""

import json

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import LoginHistoryError, UserError
from lib.utils.constants.users import Status
from models.warehouse.logins import LoginHistory
from serialisers.warehouse.logins import LoginHistorySerialiser
from models import ENGINE
from models.user.users import User
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit


def test_loginhistoryserialiser_create(get_user, regex_login_history):
    """Testing User Serialiser: Create User."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)
        login_history = LoginHistorySerialiser().create_login_history(get_user.id)
        login_id = get_id_by_regex(regex_login_history, login_history)
        login = (
            session.query(LoginHistory)
            .filter(LoginHistory.login_id == login_id)
            .one_or_none()
        )
        assert login.id is not None
        run_test_teardown(login.id, LoginHistory, session)
        run_test_teardown(get_user.id, User, session)


def test_loginhistoryserialiser_create_invalid():
    """Testing User Serialiser: Invalid Create User [Email]."""

    with raises(LoginHistoryError):
        LoginHistorySerialiser().create_login_history("id")


def test_loginhistoryserialiser_get(get_user, regex_user, login_keys, app):
    """Testing User Serialiser: Get User."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)
        login = LoginHistory()
        login.user_id = get_user.id
        setup_test_commit(login, session)
        login_history = LoginHistorySerialiser().get_login_history(login.login_id)

        assert isinstance(login_history, dict)
        for key in login_history:
            assert key not in LoginHistory.__EXCLUDE_ATTRIBUTES__

        run_test_teardown(login_history.id, LoginHistory, session)
        run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_get_invalid(email, password):
#     """Testing User Serialiser: Invalid Get User."""

#     with raises(UserError):
#         LoginHistorySerialiser().get_user("id")


# def test_loginhistoryserialiser_delete(get_user, regex_user):
#     """Testing User Serialiser: Delete User."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)
#         LoginHistorySerialiser().delete_user(get_user.id)


# def test_loginhistoryserialiser_delete_invalid():
#     """Testing User Serialiser: Invalid Delete User."""

#     with raises(UserError):
#         LoginHistorySerialiser().delete_user("id")


# def test_loginhistoryserialiser_update_valid_password(get_user, password):
#     """Testing User Serialiser: Update User [PASSWORD]."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)
#         LoginHistorySerialiser().update_user(get_user.id, password=password)
#         run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_update_invalid_password(get_user):
#     """Testing User Serialiser: Invalid Update User [PASSWORD]."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)

#         with raises(UserError):
#             LoginHistorySerialiser().update_user(get_user.id, password="password")
#         run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_update_invalid_password_type(get_user):
#     """Testing User Serialiser: Invalid Update User [PASSWORD]."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)

#         with raises(UserError):
#             LoginHistorySerialiser().update_user(get_user.id, password=1)
#         run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_update_valid_user_status(get_user):
#     """Testing User Serialiser: Update User [STATUS]."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)

#         LoginHistorySerialiser().update_user(get_user.id, status=Status.ACTIVE)
#         run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_update_invalid_user_status(get_user):
#     """Testing User Serialiser: Update User [STATUS]."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)

#         with raises(UserError):
#             LoginHistorySerialiser().update_user(get_user.id, status=Status.DISABLED)
#         run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_update_invalid_user_status_type(get_user):
#     """Testing User Serialiser: Update User [STATUS]."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)

#         with raises(UserError):
#             LoginHistorySerialiser().update_user(get_user.id, status="Status.DISABLED")
#         run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_update_invalid(get_user, email):
#     """Testing User Serialiser: Update User."""

#     with Session(ENGINE) as session:
#         setup_test_commit(get_user, session)

#         with raises(TypeError):
#             LoginHistorySerialiser().update_user(get_user.id, email=email)
#         run_test_teardown(get_user.id, User, session)


# def test_loginhistoryserialiser_update_invalid():
#     """Testing User Serialiser: Invalid Update User."""

#     with raises(TypeError):
#         LoginHistorySerialiser().update_user("id", id="")
