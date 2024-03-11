"""_summary_

Raises:
    UserAccountError: _description_

Returns:
    _type_: _description_
"""

from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, DateTime, String, text, ForeignKey, Enum
from lib.interfaces.types import UserAccountError
from lib.utils.constants.users import (
    AccountRole,
    AccountStatus,
    AccountEmailVerification,
)
from lib.utils.helpers.users import check_account_status
from models import Base


class UserAccount(Base):
    """_summary_

    Args:
        Base (_type_): _description_

    Raises:
        UserAccountError: _description_

    Returns:
        _type_: _description_
    """
    __tablename__ = "user_accounts"

    account_id = Column(
        "account_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    user_id: Column[str] = Column("user_id", ForeignKey("users.id"), nullable=False)
    __account_status: Union[AccountStatus, Column[AccountStatus]] = Column(
        "account_status",
        Enum(AccountStatus),
        default=AccountStatus.NEW,
    )
    email_status: Union[AccountEmailVerification, Column[AccountEmailVerification]] = (
        Column(
            "account_email_status",
            Enum(AccountEmailVerification),
            default=AccountEmailVerification.UNVERIFIED,
        )
    )
    __account_creation_date = Column(
        "account_creation_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    __account_updated_date = Column(
        "account_updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
    __account_status_updated_date: Union[datetime, Column[datetime]] = Column(
        "account_status_updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    last_login_date = Column("last_login_date", DateTime, nullable=True)
    __role: Union[AccountRole, Column[AccountRole]] = Column(
        "account_role", Enum(AccountRole), nullable=False, default=AccountRole.USER
    )

    @property
    def role(self) -> Union[AccountRole, Column[AccountRole]]:
        """_summary_

        Returns:
            Union[AccountRole, Column[AccountRole]]: _description_
        """
        if self.__role == AccountRole.USER:
            return self.__role
        return AccountRole.USER

    @property
    def account_status(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__account_status

    @account_status.setter
    def account_status(self, value: AccountStatus) -> UserAccountError:
        """_summary_

        Args:
            value (AccountStatus): _description_

        Raises:
            UserAccountError: _description_

        Returns:
            UserAccountError: _description_
        """
        if not check_account_status(self.__account_status, value):
            raise UserAccountError(
                f"Invalid Account Status for {self.__account_status} User."
            )
        self.__account_status = value
        self.__account_status_updated_date = datetime.now()

    @property
    def account_creation_date(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__account_creation_date

    @property
    def account_updated_date(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__account_updated_date

    @property
    def account_status_updated_date(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__account_status_updated_date
