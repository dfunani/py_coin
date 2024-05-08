"""Users Serialiser Module: Serialiser for Account Model."""

from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.interfaces.exceptions import AccountError
from lib.utils.constants.users import Status
from lib.validators.users import validate_status
from models import ENGINE
from models.user.accounts import Account
from serialisers.serialiser import BaseSerialiser


class AccountSerialiser(Account, BaseSerialiser):
    """Serialiser for the Account Model."""

    __SERIALISER_EXCEPTION__ = AccountError
    __MUTABLE_KWARGS__: list[str] = ["status"]

    def get_account(self, account_id: str) -> dict:
        """CRUD Operation: Read Account."""

        with Session(ENGINE) as session:
            query = select(Account).filter(
                cast(Account.account_id, String) == account_id
            )
            account = session.execute(query).scalar_one_or_none()

            if not account:
                raise AccountError("Account Not Found.")

            return self.__get_model_data__(account)

    def create_account(self, user_id) -> str:
        """CRUD Operation: Create Account."""

        with Session(ENGINE) as session:
            self.user_id = user_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Created.") from exc

            return str(self)

    def update_account(self, private_id: str, **kwargs) -> str:
        """CRUD Operation: Update Account."""

        with Session(ENGINE) as session:
            account = session.get(Account, private_id)

            if account is None:
                raise AccountError("Account Not Found.")

            for key, value in kwargs.items():
                if key not in AccountSerialiser.__MUTABLE_KWARGS__:
                    raise AccountError("Invalid Account.")

                value = self.validate_serialiser_kwargs(key, value)
                setattr(account, key, value)

            try:
                session.add(account)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Updated.") from exc

            return str(account)

    def delete_account(self, private_id: str) -> str:
        """CRUD Operation: Delete Account."""

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
