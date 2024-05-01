"""Serialisers Module: Testing User Serialiser."""

from datetime import datetime
import json
from uuid import uuid4

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import LoginHistoryError, UserError
from lib.utils.constants.users import Country, LoginMethod, Status
from models.warehouse.logins import LoginHistory
from serialisers.warehouse.logins import LoginHistorySerialiser
from models import ENGINE
from models.user.users import User
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit


def test_loginhistoryserialiser_create(user):
    """Testing User Serialiser: Create User."""

    with Session(ENGINE) as session:
        login_history = LoginHistorySerialiser().create_login_history(user.id)
        login_id = get_id_by_regex(login_history)
        login = (
            session.query(LoginHistory)
            .filter(LoginHistory.login_id == login_id)
            .one_or_none()
        )
        assert login.id is not None
        run_test_teardown(login.id, LoginHistory, session)


def test_loginhistoryserialiser_create_invalid():
    """Testing User Serialiser: Invalid Create User [Email]."""

    with raises(LoginHistoryError):
        LoginHistorySerialiser().create_login_history("id")


def test_loginhistoryserialiser_get(login):
    """Testing User Serialiser: Get User."""

    login_history = LoginHistorySerialiser().get_login_history(login.login_id)

    assert isinstance(login_history, dict)
    for key in login_history:
        assert key not in LoginHistory.__EXCLUDE_ATTRIBUTES__


def test_loginhistoryserialiser_get_invalid():
    """Testing User Serialiser: Invalid Get User."""

    with raises(LoginHistoryError):
        LoginHistorySerialiser().get_login_history("id")


def test_loginhistoryserialiser_delete(login):
    """Testing User Serialiser: Delete User."""

    LoginHistorySerialiser().delete_login_history(login.id)


def test_loginhistoryserialiser_delete_invalid():
    """Testing User Serialiser: Invalid Delete User."""

    with raises(LoginHistoryError):
        LoginHistorySerialiser().delete_login_history("id")


def test_loginhistoryserialiser_update_valid(login):
    """Testing User Serialiser: Update User [PASSWORD]."""

    with Session(ENGINE) as session:
        session_id = str(uuid4())
        token = str(uuid4())
        logout = datetime.now()
        LoginHistorySerialiser().update_login_history(
            login.id,
            session_id=session_id,
            login_location=Country.ALBANIA,
            login_device="Chrome",
            login_method=LoginMethod.EMAIL,
            logged_in=True,
            logout_date=logout,
            authentication_token=token,
        )
        login = session.get(LoginHistory, login.id)
        assert login.session_id == session_id
        assert login.login_location == Country.ALBANIA
        assert login.login_device == "Chrome"
        assert login.login_method == LoginMethod.EMAIL
        assert login.logged_in == True
        assert login.logout_date == logout
        assert login.authentication_token == token


def test_loginhistoryserialiser_update_invalid():
    """Testing User Serialiser: Invalid Update User [PASSWORD]."""

    with raises(LoginHistoryError):
        LoginHistorySerialiser().update_login_history(
            "login.id",
            session_id=1,
            login_date=1,
            login_device=1,
            logged_in=1,
            logout_date=1,
            authentication_token=1,
        )
