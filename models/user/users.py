"""Base Module: Contains User Abstract/Base class,
modelling a Users Base structure."""

from json import dumps
from os import getenv
from typing import Union
from uuid import uuid4
from cryptography.fernet import Fernet
from sqlalchemy import Column, DateTime, String, text
from lib.interfaces.types import FernetError, UserEmailError, UserPasswordError
from lib.utils.constants.users import Regex
from lib.utils.helpers.users import get_hash_value
from models import Base


class User(Base):
    """
    Model representing user information.

    Properties:
        - __tablename__ (str): The name of the database table for users.
        - user_id (str): Encrypted User Data

    Usage:
    - To create a new user:
        new_user = User("email@testing.com", "password@specialcharacters")
        session.add(new_user)
        session.commit()

    - To retrieve the encrypted user ID:
        encrypted_user_id = queried_user.user_id()
    """

    __tablename__ = "users"

    __id = Column(
        "id", String(256), default=text(f"'{str(uuid4())}'"), primary_key=True
    )
    __user_id = Column("user_id", String(256), default=text(f"'{str(uuid4())}'"))
    __created = Column("created", DateTime, default=text("CURRENT_TIMESTAMP"))
    __email: Union[str, Column[str]] = Column(
        "email", String(256), unique=True, nullable=False
    )
    __password: Union[str, Column[str]] = Column(
        "password", String(256), nullable=False
    )

    def __init__(self, email: str, password: str) -> None:
        """User Object Constructor

        Args:
            email (str): Email to Assign to Created User
            password (str): Password to Assign to Created User

        Raises:
            UserEmailError: Custom User Email Error
            UserPasswordError: Custom User Password Error
        """
        if not isinstance(email, str):
            raise UserEmailError("No Email Provided")
        if not isinstance(password, str):
            raise UserPasswordError("No Password Provided")

        if not Regex.EMAIL.value.match(email):
            raise UserEmailError("Invalid User Email.")
        if not Regex.PASSWORD.value.match(password):
            raise UserPasswordError("Invalid User Password.")

        self.__email = email
        self.__password = get_hash_value(password)

    @property
    def email(self) -> UserEmailError:
        """Getter For User Email

        Raises:
            UserEmailError: Raises a User Email Error
        """
        raise UserEmailError("Can Not Access Private Attribute: [Email]")

    @email.setter
    def email(self, value: str) -> UserEmailError:
        """Setter For User Email

        Args:
            value (str): Value to set attribute to.

        Raises:
            UserEmailError: Custom Exception for Invalid Email Actions.

        Returns:
            Union[None, UserEmailError]: Returns None or Raises a User Email Error.
        """

        if not Regex.EMAIL.value.match(value):
            raise UserEmailError("Invalid User Email.")
        self.__email = value

    @property
    def password(self) -> UserPasswordError:
        """Getter For User Password

        Raises:
            UserPasswordlError: Raises a User Password Error
        """
        raise UserPasswordError("Can Not Access Private Attribute: [PASSWORD]")

    @password.setter
    def password(self, value: str) -> UserPasswordError:
        """Setter For User Pasword

        Args:
            value (str): Value to set attribute to.

        Raises:
            UserEmailError: Custom Exception for Invalid Password Actions.

        Returns:
            Union[None, UserEmailError]: Returns None or Raises a User Password Error.
        """
        if not Regex.PASSWORD.value.match(value):
            raise UserPasswordError("Invalid User Password.")
        self.__password = get_hash_value(value)

    @property
    def user_id(self) -> str:
        """
        Return an encrypted string combining the user's unique ID, user ID, and creation timestamp.

        Returns:
        - str: An encrypted string representing the user's ID information.
        """
        data = {
            "id": self.__id,
            "user_id": self.__user_id,
            "created": str(self.__created),
            "email": self.__email,
            "password": self.__password,
        }
        fkey = getenv("FERNET_KEY")
        if not fkey:
            raise FernetError("Fernet Key not found.")
        return Fernet(fkey).encrypt(dumps(data).encode()).decode()
