"""Users Module: Testing the Accounts Class."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ENGINE
from models.user.accounts import Account
from models.user.users import User
from tests.conftest import setup_test_commit, run_test_teardown


def test_account_invalid_no_args():
    """Testing Account With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            account = Account()
            setup_test_commit(account, session)


def test_account_invalid_args(email, password):
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            account = Account(email, password)
            setup_test_commit(account, session)


def test_account_valid(get_account):
    """Testing a Valid Account Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        assert get_account.id is not None

        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)
