"""Accounts Serialiser Module: Serialiser for Account Model."""

from typing import Union

from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.interfaces.exceptions import (
    FernetError,
    AccountError,
)
from lib.utils.constants.users import Status
from lib.validators.users import validate_status
from models import ENGINE
from models.user.accounts import Account


class AccountSerialiser(Account):
    """
    Serialiser for the Account Model.

    Args:
        Account (class): Access Point to the Account Model.
    """

    def get_account(self, account_id: str) -> Union[dict, AccountError, FernetError]:
        """CRUD Operation: Read Account.

        Args:
            account_id (str): Public Account ID.

        Returns:
            str: Account Object.
        """
        with Session(ENGINE) as session:
            query = select(Account).filter(
                cast(Account.account_id, String) == account_id
            )
            account = session.execute(query).scalar_one_or_none()

            if not account:
                raise AccountError("Account Not Found.")

            return self.__get_encrypted_account_data__(account)

    def create_account(self, user_id) -> str:
        """CRUD Operation: Create Account.

        Args:
            private_id (str): Unique User ID.

        Returns:
            str: Account Object.
        """
        with Session(ENGINE) as session:
            self.user_id = user_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Created.") from exc

            return str(self)

    def update_account(self, private_id: str, status: Status) -> str:
        """CRUD Operation: Update Account.

        Args:
            id (str): Private Account ID.

        Returns:
            str: Account Object.
        """
        with Session(ENGINE) as session:
            account = session.get(Account, private_id)

            if account is None:
                raise AccountError("Account Not Found.")

            validate_status(status)
            setattr(account, "status", status)

            try:
                session.add(account)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Updated.") from exc

            return str(account)

    def delete_account(self, private_id: str) -> str:
        """CRUD Operation: Delete Account.

        Args:
            id (str): Private Account ID.

        Returns:
            str: Account Object.
        """
        with Session(ENGINE) as session:
            account = session.get(Account, private_id)

            if not account:
                raise AccountError("Account Not Found")

            try:
                session.delete(account)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Deleted.") from exc

            return f"Deleted: {private_id}"

    def __get_encrypted_account_data__(
        self, account: Account
    ) -> Union[dict, AccountError, FernetError]:
        """Get Account Information.

        Returns:
            dict: Encrypted Account Data.
        """
        data = {
            "id": account.id,
            "account_id": account.account_id,
            "user_id": account.user_id,
            "status": account.status,
            "created_date": account.created_date,
            "updated_date": account.updated_date,
            "user_profiles": account.user_profiles,
            "payment_profiles": account.payment_profiles,
            "settings_profile": account.settings_profile,
        }
        return data
