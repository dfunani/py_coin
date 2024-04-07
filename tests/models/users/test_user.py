"""Base Test Module testing the User Abstract Class"""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig

from models import ENGINE
from models.user.users import User
from lib.utils.helpers.users import get_hash_value
from tests.conftest import test_commit, test_teardown


def test_user_invalid_no_args():
    """Testing User With Missing Attributes."""
    with Session(ENGINE) as session:
        with raises(IntegrityError):
            user = User()
            session.add(user)
            session.commit()


def test_user_invalid_args(email, password):
    """Testing Constructor, for Invalid Arguments."""
    with Session(ENGINE) as session:
        with raises(TypeError):
            user = User(email, password)
            session.add(user)
            session.commit()


def test_user_valid(email, password):
    """Testing a Valid User Constructor, with Required Arguments."""
    with Session(ENGINE) as session:
        user = User()
        email = str(get_hash_value(email, str(AppConfig().salt_value)))
        user.email = email

        password = str(get_hash_value(password, user.salt_value))
        user.password = password

        user_id = str(get_hash_value(email + password, str(AppConfig().salt_value)))
        user.user_id = user_id

        test_commit(user, session)
        test_teardown(user.id, User, session)
