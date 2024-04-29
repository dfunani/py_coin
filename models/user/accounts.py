"""Users Module: Contains Account Model for Mapping User Accounts."""

from typing import Union
from uuid import uuid4
from sqlalchemy import Column, DateTime, String, text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from lib.utils.constants.users import Status
from models import Base
from models.model import BaseModel
from models.user.payments import PaymentProfile
from models.user.profiles import UserProfile
from models.user.settings import SettingsProfile


class Account(Base, BaseModel):
    """Model representing a User's Account."""

    __tablename__ = "accounts"
    __table_args__ = ({"schema": "users"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: str | Column[str] = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    account_id: str | Column[str] = Column(
        "account_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        unique=True,
    )
    user_id: str | Column[str] = Column(
        "user_id", String(256), ForeignKey("users.users.id"), nullable=False
    )
    status: Union[Status, Column[Status]] = Column(
        "status",
        Enum(Status, name="account_status"),
        default=Status.NEW,
        nullable=False,
    )
    created_date = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    user_profiles = relationship(
        UserProfile, backref="Account", cascade="all, delete-orphan"
    )
    payment_profiles = relationship(
        PaymentProfile, backref="Account", cascade="all, delete-orphan"
    )
    settings_profile = relationship(
        SettingsProfile, backref="Account", cascade="all, delete-orphan"
    )

    def __init__(self) -> None:
        """Account Object Constructor."""

        self.id = str(uuid4())
        self.account_id = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Account Object."""

        return f"Account ID: {self.account_id}"

    def __repr__(self) -> str:
        """String Representation of the Account Object."""

        return f"Application Model: {self.__class__.__name__}"
