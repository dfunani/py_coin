"""Users Module: Contains User Model for Mapping Users."""

from json import dumps
from os import getenv
from typing import Union
from uuid import uuid4
from cryptography.fernet import Fernet
from sqlalchemy import Column, DateTime, String, text
from lib.interfaces.types import FernetError, UserEmailError, UserPasswordError
from lib.utils.constants.users import DateFormat, Regex
from lib.utils.helpers.users import get_hash_value
from models import Base
from config import AppConfig


class User(Base):
    """
    Model representing a User.

    Properties:
        - __tablename__ (str): The name of the database table for users.
        - user_id (str): User's Public ID.
        - user (str): Encrypted User Data.

    """

    __tablename__ = "users"

    __id = Column(
        "id", String(256), default=text(f"'{str(uuid4())}'"), primary_key=True
    )
    user_id: Union[str, Column[str]] = Column(
        "user_id", String(256), default=text(f"'{str(uuid4())}'")
    )
    __created = Column("created", DateTime, default=text("CURRENT_TIMESTAMP"))
    __email: Union[str, Column[str]] = Column(
        "email", String(256), unique=True, nullable=False
    )
    __password: Union[str, Column[str]] = Column(
        "password", String(256), nullable=False
    )
    __salt_value: Union[str, Column[str]] = Column("salt_value", String(256))

    def __str__(self):
        return f'User: {self.user_id}'

    def __init__(self, email: str, password: str) -> None:
        """User Object Constructor.

        Args:
            email (str): User's Email.
            password (str): User's Password.

        Raises:
            UserEmailError: Custom User Email Error.
            UserPasswordError: Custom User Password Error.
        """
        if not isinstance(email, str):
            raise UserEmailError("No Email Provided")
        if not isinstance(password, str):
            raise UserPasswordError("No Password Provided")

        if not Regex.EMAIL.value.match(email):
            raise UserEmailError("Invalid User Email.")
        if not Regex.PASSWORD.value.match(password):
            raise UserPasswordError("Invalid User Password.")

        self.__salt_value = str(uuid4())
        self.__email = email
        self.__password = get_hash_value(password, self.__salt_value)
        self.user_id = get_hash_value(email + password, AppConfig().salt_value)

    @property
    def email(self) -> UserEmailError:
        """Getter For User Email.

        Raises:
            UserEmailError: Raises a User Email Error.
        """
        raise UserEmailError("Can Not Access Private Attribute: [Email]")

    @email.setter
    def email(self, value: Union[str, Column[str]]) -> UserEmailError:
        """Setter For User Email.

        Args:
            value (str): Value to set attribute to.

        Raises:
            UserEmailError: Custom Exception for Invalid Email Actions.

        """

        if not Regex.EMAIL.value.match(value):
            raise UserEmailError("Invalid User Email.")
        self.__email = value

    @property
    def password(self) -> UserPasswordError:
        """Getter For User Password.

        Raises:
            UserPasswordlError: Raises a User Password Error.
        """
        raise UserPasswordError("Can Not Access Private Attribute: [PASSWORD]")

    @password.setter
    def password(self, value: Union[str, Column[str]]) -> UserPasswordError:
        """Setter For User Pasword

        Args:
            value (str): Value to set attribute to.

        Raises:
            UserEmailError: Custom Exception for Invalid Password Actions.
        """
        if not Regex.PASSWORD.value.match(value):
            raise UserPasswordError("Invalid User Password.")
        self.__password = get_hash_value(value, self.__salt_value)

    @property
    def user(self) -> str:
        """
        Returns Encrypted User Data.

        Returns:
        - str: An encrypted string representing the user's ID information.
        """
        data = {
            "id": self.__id,
            "user_id": self.user_id,
            "created": self.__created.strftime(DateFormat.HYPHEN.value),
            "email": self.__email,
            "password": self.__password,
            "salt_value": self.__salt_value,
        }
        fkey = getenv("FERNET_KEY")
        if not fkey:
            raise FernetError("Fernet Key not found.")
        return Fernet(fkey).encrypt(dumps(data).encode()).decode()

    @property
    def salt_value(self) -> Union[str, Column[str]]:
        """The value used to salt the Hash Generated for the User.

        Returns:
            salt_value: The Salt Value used for Current User.
        """
        return self.__salt_value
