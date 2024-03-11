"""_summary_
"""

from json import loads
from pytest import raises
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from models import ENGINE
from models.user.accounts import UserAccount

from models.user.users import User
from tests.models.users.conftest import user_test_commit, user_test_teardown


def test_invalid_user_account_no_user_id(get_user, fkey):
    """_summary_"""
    with Session(ENGINE) as session:
        session.add(get_user)
        session.commit()

        user_data = loads(Fernet(fkey).decrypt(get_user.user_id.encode()))
        assert "id" in user_data and user_data.get("id")
        account = UserAccount()
        with raises(AttributeError):
            account.user_id.get("id")

        user = session.get(User, user_data.get("id"))
        session.delete(user)
        session.commit()


def test_invalid_user_account_no_valid_user_id(get_user, fkey):
    """_summary_"""
    with Session(ENGINE) as session:
        session.add(get_user)
        session.commit()

        user_data = loads(Fernet(fkey).decrypt(get_user.user_id.encode()))
        assert "id" in user_data and user_data.get("id")
        account = UserAccount(user_id="test_id")
        with raises(AttributeError):
            account.user_id.get("id")

        user = session.get(User, user_data.get("id"))
        session.delete(user)
        session.commit()


def test_valid_user_account_no_valid_user_id(get_user, fkey):
    """_summary_"""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)
        user_data = loads(Fernet(fkey).decrypt(get_user.user_id.encode()))

        get_account = UserAccount(user_id=user_data.get("id"))
        user_test_commit(get_account, session)

        assert get_account.user_id is not None

        user_test_teardown(get_account.account_id, UserAccount, session)
        user_test_teardown(user_data.get("id"), User, session)
