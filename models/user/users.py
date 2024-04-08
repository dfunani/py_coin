"""Users Module: Contains User Model for Mapping Users."""

from typing import Union
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, text

from lib.utils.constants.users import UserStatus
from models import Base


class User(Base):
    """
    Model representing a User.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        - __tablename__ (str): The name of the database table for users.
        - id (str): User's Private ID.
        - user_id (str): User's Public ID.
        - created_date (datetime): User Created Date.
        - updated_date (datetime): User Updated Date.
        - email (str): User's Email.
        - password (str): User's Password.
        - salt_value (str): User's Hash Salt Value.
    """

    __tablename__ = "users"

    id: Union[str, Column[str]] = Column("id", String(256), primary_key=True)
    user_id: Union[str, Column[str]] = Column("user_id", String(256), nullable=False)
    email: Union[str, Column[str]] = Column(
        "email", String(256), unique=True, nullable=False
    )
    user_status: Union[UserStatus, Column[UserStatus]] = Column(
        "user_status", Enum(UserStatus), nullable=False, default=UserStatus.NEW
    )
    password: Union[str, Column[str]] = Column("password", String(256), nullable=False)
    salt_value: Union[str, Column[str]] = Column(
        "salt_value", String(256), nullable=False
    )

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
