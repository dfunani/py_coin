"""Accounts Module: Contains a User's Account Model for Mapping a User to an Account."""

from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, DateTime, String, text, ForeignKey, Enum
from lib.interfaces.types import UserAccountError
from lib.utils.constants.users import (
    AccountRole,
    AccountStatus,
    AccountEmailVerification,
    DateFormat,
)
from lib.utils.helpers.users import check_account_status
from models import Base


class Account(Base):
    """
    Model representing a User's Account.

    Properties:
        - __tablename__ (str): The name of the database table for users.
        - account_id (str): User's Public Account ID.
        - user_id (str): User's Asscociated with the Account.
        - email_status (AccountEmailVerification): Status of
        the Verification of the User's Email.
        - last_login_date (datetime): User's Last Login Datetime.

    """

    __tablename__ = "accounts"

    id = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    account_id: Column[str] = Column(
        "account_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        unique=True,
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
    __account_creation_date: Union[datetime, Column[datetime]] = Column(
        "account_creation_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    __account_updated_date: Union[datetime, Column[datetime]] = Column(
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
    last_login_date: Union[datetime, Column[datetime]] = Column(
        "last_login_date", DateTime, nullable=True
    )
    __role: Union[AccountRole, Column[AccountRole]] = Column(
        "account_role", Enum(AccountRole), nullable=False, default=AccountRole.USER
    )

    def __str__(self) -> str:
        """String Representation of the Accounts Object.

        Returns:
            str: String Representation
        """
        return f"Account: {self.account_id}"

    @property
    def role(self) -> Union[AccountRole, Column[AccountRole]]:
        """Getter for the User's Role.

        Returns:
            AccountRole: User's Role.
        """
        if self.__role == AccountRole.USER:
            return self.__role
        return AccountRole.USER

    @property
    def account_status(self) -> Union[AccountStatus, Column[AccountStatus]]:
        """Getter for the User's Account Status.

        Returns:
            AccountStatus: User's Account Status.
        """
        return self.__account_status

    @account_status.setter
    def account_status(self, value: AccountStatus) -> UserAccountError:
        """Setter for the User's Account Status.

        Args:
            value (AccountStatus): Updated Account Status Value.

        Raises:
            UserAccountError: Custom Exception for User's Account.
        """
        if not check_account_status(self.__account_status, value):
            raise UserAccountError(
                f"Invalid Account Status for {self.__account_status.value} User."
            )
        self.__account_status = value
        self.__account_status_updated_date = datetime.now()

    @property
    def account_creation_date(self) -> str:
        """Getter for the User's Account Creation Date.

        Returns:
            datetime: User's Creation Date.
        """
        return self.__account_creation_date.strftime(DateFormat.HYPHEN.value)

    @property
    def account_updated_date(self) -> str:
        """Getter for the User's Account Updated Date.

        Returns:
            datetime: User's Updated Date.
        """
        return self.__account_updated_date.strftime(DateFormat.HYPHEN.value)

    @property
    def account_status_updated_date(self) -> str:
        """Getter for the User's Account Status Updated Date.

        Returns:
            datetime: User's Creation Date.
        """
        return self.__account_status_updated_date.strftime(DateFormat.HYPHEN.value)
