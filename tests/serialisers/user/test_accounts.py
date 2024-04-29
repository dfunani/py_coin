"""Serialisers Module: Testing Accounts Serialiser."""

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import AccountError, UserError
from lib.utils.constants.users import Status
from models.user.accounts import Account
from models.user.users import User
from models.warehouse.cards import Card
from serialisers.user.accounts import AccountSerialiser
from models import ENGINE
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit


def test_accountprofileserialiser_create(get_user, regex_user, regex_account):
    """Testing Account Serialiser: Create Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        account = AccountSerialiser().create_account(get_user.id)
        account_id = get_id_by_regex(regex_account, str(account))
        account_data = (
            session.query(Account)
            .filter(Account.account_id == account_id)
            .one_or_none()
        )
        run_test_teardown(account_data.id, Account, session)
        run_test_teardown(account_data.user_id, User, session)


def test_accountprofileserialiser_create_invalid():
    """Testing Account Serialiser: Create Account."""

    with raises(AccountError):
        AccountSerialiser().create_account("user.id")


def test_accountprofileserialiser_get(get_user, regex_user, regex_account, account_keys):
    """Testing Account Serialiser: Get Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        account = AccountSerialiser().create_account(get_user.id)
        account_id = get_id_by_regex(regex_account, str(account))
        account_data = AccountSerialiser().get_account(account_id)

        assert isinstance(account_data, dict)
        for key in account_data:
            assert key not in Account.__EXCLUDE_ATTRIBUTES__

        run_test_teardown(account_data.get("id"), Account, session)
        run_test_teardown(account_data.get("user_id"), User, session)


def test_accountprofileserialiser_get_invalid():
    """Testing Account Serialiser: Get Account."""

    with raises(AccountError):
        AccountSerialiser().get_account("account_id")


def test_accountprofileserialiser_delete(get_user, regex_user, regex_account):
    """Testing Account Serialiser: Delete Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        account = AccountSerialiser().create_account(get_user.id)
        account_id = get_id_by_regex(regex_account, str(account))

        account_data = (
            session.query(Account)
            .filter(Account.account_id == account_id)
            .one_or_none()
        )

        AccountSerialiser().delete_account(account_data.id)
        run_test_teardown(account_data.user_id, User, session)


def test_accountprofileserialiser_delete_invalid():
    """Testing Account Serialiser: Delete Account."""

    with raises(AccountError):
        AccountSerialiser().delete_account("account_data.id")


def test_accountprofileserialiser_update_valid_status(get_user, regex_user, regex_account):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        account = AccountSerialiser().create_account(get_user.id)
        account_id = get_id_by_regex(regex_account, str(account))

        account_data = (
            session.query(Account)
            .filter(Account.account_id == account_id)
            .one_or_none()
        )

        AccountSerialiser().update_account(account_data.id, status=Status.DELETED)
        run_test_teardown(account_data.id, Account, session)
        run_test_teardown(account_data.user_id, User, session)


def test_accountprofileserialiser_update_invalid_status(
    get_user, regex_user, regex_account
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        account = AccountSerialiser().create_account(get_user.id)
        account_id = get_id_by_regex(regex_account, str(account))

        account_data = (
            session.query(Account)
            .filter(Account.account_id == account_id)
            .one_or_none()
        )

        with raises(UserError):
            AccountSerialiser().update_account(account_data.id, status=Status.DISABLED)

        run_test_teardown(account_data.id, Account, session)
        run_test_teardown(account_data.user_id, User, session)


def test_accountprofileserialiser_update_invalid_status_type(
    get_user, regex_user, regex_account
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_user, session)

        account = AccountSerialiser().create_account(get_user.id)
        account_id = get_id_by_regex(regex_account, str(account))

        account_data = (
            session.query(Account)
            .filter(Account.account_id == account_id)
            .one_or_none()
        )

        with raises(UserError):
            AccountSerialiser().update_account(
                account_data.id, status="Status.DISABLED"
            )

        run_test_teardown(account_data.id, Account, session)
        run_test_teardown(account_data.user_id, User, session)


def test_accountprofileserialiser_update_invalid_status_no_id():
    """Testing Account Serialiser: Update Account."""

    with raises(AccountError):
        AccountSerialiser().update_account("account_data.id")
