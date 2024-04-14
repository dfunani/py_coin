"""Users Module: Testing the User Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ENGINE
from models.user.users import User
from lib.utils.constants.users import Role, Status
from tests.conftest import setup_test_commit, run_test_teardown


def test_user_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            user = User()
            session.add(user)
            session.commit()


def test_user_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            user = User("email", "password")
            session.add(user)
            session.commit()


def test_user_valid(get_user):
    """Testing a Valid User Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        assert get_user.id is not None
        assert get_user.status == Status.NEW
        assert get_user.role == Role.USER

        run_test_teardown(get_user.id, User, session)
