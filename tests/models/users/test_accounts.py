"""Base Test Module testing the User Abstract Class"""

from json import loads
from pytest import raises
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from lib.interfaces.types import UserAccountError
from lib.utils.constants.users import (
    AccountEmailVerification,
    AccountRole,
    AccountStatus,
)
from models import ENGINE
from models.user.accounts import Account

from models.user.users import User
from tests.models.users.conftest import user_test_commit, user_test_teardown


def test_invalid_user_account_user_id(get_user, fkey):
    """Test Valid User ID."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))

        account = Account(user_id=user_data.get("id"))
        user_test_commit(account, session)

        user_test_teardown(account.id, Account, session)
        user_test_teardown(user_data.get("id"), User, session)


def test_invalid_user_account_no_user_id_fail(get_user, fkey):
    """Test Invalid User ID."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))
        with raises(BaseException):
            account = Account(user_id="Fail User ID")
            assert account.id

        user_test_teardown(user_data.get("id"), User, session)


def test_invalid_user_account_new(get_user, fkey):
    """Test New Valid User Email Status."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))
        account = Account(user_id=user_data.get("id"))
        user_test_commit(account, session)
        assert account.account_status == AccountStatus.NEW
        user_test_teardown(account.id, Account, session)
        user_test_teardown(user_data.get("id"), User, session)


def test_valid_user_account_status(get_user, fkey):
    """Test Invalid User Data Email Status."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))
        account = Account(user_id=user_data.get("id"))
        user_test_commit(account, session)
        account.account_status = AccountStatus.VERIFIED
        assert account.account_status == AccountStatus.VERIFIED
        user_test_teardown(account.id, Account, session)
        user_test_teardown(user_data.get("id"), User, session)


def test_invalid_user_account_role(get_user, fkey):
    """Test Valid User Role."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))
        account = Account(user_id=user_data.get("id"))
        user_test_commit(account, session)

        assert account.role == AccountRole.USER
        user_test_teardown(account.id, Account, session)
        user_test_teardown(user_data.get("id"), User, session)


def test_invalid_user_account_status_invalid(get_user, fkey):
    """Test Valid User Email Status."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))
        account = Account(user_id=user_data.get("id"))
        user_test_commit(account, session)
        with raises(UserAccountError):
            account.account_status = AccountStatus.DELETED
        user_test_teardown(account.id, Account, session)
        user_test_teardown(user_data.get("id"), User, session)


def test_valid_user_account_status_email_invalid(get_user, fkey):
    """Test Valid User Email Status."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))
        account = Account(user_id=user_data.get("id"))
        user_test_commit(account, session)
        assert account.email_status == AccountEmailVerification.UNVERIFIED
        user_test_teardown(account.id, Account, session)
        user_test_teardown(user_data.get("id"), User, session)


def test_update_user_account_status_email_invalid(get_user, fkey):
    """Test Valid User Email Status."""
    with Session(ENGINE) as session:
        user_test_commit(get_user, session)

        user_data = loads(Fernet(fkey).decrypt(get_user.user.encode()))
        account = Account(user_id=user_data.get("id"))
        account.email_status = AccountEmailVerification.FAILED
        user_test_commit(account, session)

        assert account.email_status == AccountEmailVerification.FAILED
        user_test_teardown(account.id, Account, session)
        user_test_teardown(user_data.get("id"), User, session)
