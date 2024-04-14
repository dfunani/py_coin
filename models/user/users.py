"""Users Module: Contains User Model for Mapping Users."""

from datetime import datetime
from typing import Union
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, text

from lib.utils.constants.users import Role, Status
from models import Base


class User(Base):
    """
    Model representing a User.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        - __tablename__ (str): The name of the database table for users.
        - id (str): Private User ID.
        - user_id (str): Public User ID.
        - created_date (datetime): User Created Date.
        - updated_date (datetime): User Updated Date.
        - email (str): User's Email.
        - password (str): User's Password.
        - salt_value (str): User's Hash Salt Value.
    """

    __tablename__ = "users"
    __table_args__ = ({"schema": "users"},)

    id: Union[str, Column[str]] = Column(
        "id", String(256), primary_key=True, nullable=False
    )
    user_id: Union[str, Column[str]] = Column(
        "user_id", String(256), nullable=False, unique=True
    )
    email: Union[str, Column[str]] = Column(
        "email", String(256), unique=True, nullable=False
    )
    password: Union[str, Column[str]] = Column("password", String(256), nullable=False)
    created_date: Union[datetime, Column[datetime]] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    status: Union[Status, Column[Status]] = Column(
        "status", Enum(Status, name="user_status"), nullable=False, default=Status.NEW
    )
    salt_value: Union[str, Column[str]] = Column(
        "salt_value", String(256), nullable=False
    )
    role: Union[Role, Column[Role]] = Column(
        "role", Enum(Role), nullable=False, default=Role.USER
    )
    # login_history = Column(UserLoginHistory, unique=True, nullable=False)
    # registered_user_devices = Column(UserDevice)

    def __init__(self) -> None:
        """User Object Constructor."""

        self.id = str(uuid4())
        self.salt_value = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the User Object.

        Returns:
            str: Representation of a User Object.
        """
        return f"User ID: {self.user_id}"

    def __repr__(self) -> str:
        """String Representation of the User Object.

        Returns:
            str: Representation of a User Object.
        """
        return f"Application Model: {self.__class__.__name__}"
