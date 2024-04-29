"""Warehouse Module: Testing the Login History Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ENGINE
from models.user.users import User
from models.warehouse.logins import LoginHistory
from tests.conftest import setup_test_commit, run_test_teardown


def test_login_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            login_history = LoginHistory()
            session.add(login_history)
            session.commit()


def test_login_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            login_history = LoginHistory("email", "password")
            session.add(login_history)
            session.commit()


def test_login_valid(get_user):
    """Testing a Valid LoginHistory Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        login_history = LoginHistory()
        login_history.user_id = get_user.id

        setup_test_commit(login_history, session)

        run_test_teardown(login_history.id, LoginHistory, session)
        run_test_teardown(get_user.id, User, session)
