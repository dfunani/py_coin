"""Serialisers Module: Testing Accounts Serialiser."""

from pytest import raises
from sqlalchemy.orm import Session

from config import AppConfig
from lib.interfaces.exceptions import AccountError, UserError
from lib.utils.constants.users import Status
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models.user.accounts import Account
from models.user.users import User
from models.warehouse.cards import Card
from serialisers.user.accounts import AccountSerialiser
from models import ENGINE
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit


def test_accountprofileserialiser_create(user):
    """Testing Account Serialiser: Create Account."""

    with Session(ENGINE) as session:
        account = AccountSerialiser().create_account(user.id)
        account_id = get_id_by_regex(account)
        account = (
            session.query(Account)
            .filter(Account.account_id == account_id)
            .one_or_none()
        )
        assert account.id is not None

        run_test_teardown(account.id, Account, session)


def test_accountprofileserialiser_create_invalid():
    """Testing Account Serialiser: Create Account."""

    with raises(AccountError):
        AccountSerialiser().create_account("user.id")


def test_accountprofileserialiser_get(account):
    """Testing Account Serialiser: Get Account."""

    account_data = AccountSerialiser().get_account(account.account_id)

    assert isinstance(account_data, dict)
    for key in account_data:
        assert key not in Account.__EXCLUDE_ATTRIBUTES__


def test_accountprofileserialiser_get_invalid():
    """Testing Account Serialiser: Get Account."""

    with raises(AccountError):
        AccountSerialiser().get_account("account_id")


def test_accountprofileserialiser_delete(account):
    """Testing Account Serialiser: Delete Account."""

    AccountSerialiser().delete_account(account.id)


def test_accountprofileserialiser_delete_invalid():
    """Testing Account Serialiser: Delete Account."""

    with raises(AccountError):
        AccountSerialiser().delete_account("account_data.id")


def test_accountprofileserialiser_update_valid_status(account):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        AccountSerialiser().update_account(account.id, status=Status.DELETED)
        account = session.get(Account, account.id)
        assert account.id is not None
        assert account.status == Status.DELETED


def test_accountprofileserialiser_update_invalid_status(account):
    """Testing Account Serialiser: Update Account."""

    with raises(UserError):
        AccountSerialiser().update_account(account.id, status=Status.DISABLED)
        AccountSerialiser().update_account(account.id, status="Status.DISABLED")
        AccountSerialiser().update_account("account_data.id")
