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


def test_login_valid():
    """Testing a Valid LoginHistory Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        user = User()
        user.email = "test@test.com"
        user.password = "password123@"
        user.user_id = "test_user_id"
        session.add(user)
        session.commit()

        login_history = LoginHistory()
        login_history.user_id = user.id
        session.add(login_history)
        session.commit()

        assert login_history.id is not None
        assert login_history.logged_in == False

        run_test_teardown(login_history.id, LoginHistory, session)
        run_test_teardown(user.id, User, session)
