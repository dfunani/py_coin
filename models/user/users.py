"""Users Module: Contains User Model for Mapping Users."""

from json import dumps
from os import getenv
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, DateTime, Integer, String, text
from lib.interfaces.exceptions import FernetError, UserEmailError, UserError, UserPasswordError
from lib.utils.constants.users import DateFormat, Regex
from lib.utils.helpers.users import get_hash_value
from models import Base
from config import AppConfig


class User(Base):
    """
    Model representing a User.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        - __tablename__ (str): The name of the database table for users.
        - user_id (str): User's Public ID.
        - user (str): Encrypted User Data.

    """

    __tablename__ = "users"

    __id = Column(
        "id", Integer, primary_key=True, autoincrement=True
    )
    __user_id = Column(
        "user_id", String(256), nullable=False
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

        self.__salt_value = str(uuid4())
        self.__set_email(email)
        self.__set_password(password)
        self.user_id = get_hash_value(email + password, AppConfig().salt_value)

    def __str__(self) -> str:
        """String Representation of the Accounts Object.

        Returns:
            str: Representation of a User Object.
        """
        return f"User: {self.user_id}"

    @property
    def user_id(self) -> Union[str, UserError, FernetError]:
        """
        Returns Encrypted User Data.

        Returns:
        - str: An encrypted string representing the user's ID information.
        """
        data = {}
        for keys in [ self.__id,
            self.__created.strftime(DateFormat.HYPHEN.value),
            self.__email,
            self.__password,
            self.__salt_value,]:
            if not keys:
                raise UserError('Invalid User.')
        data = {
            "id": self.__id,
            "created": self.__created.strftime(DateFormat.HYPHEN.value),
            "email": self.__email,
            "password": self.__password,
            "salt_value": self.__salt_value,
        }
        # if not fkey:
            
        # return .encrypt(dumps(data).encode()).decode()

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

        self.__set_email(value)
        

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
        self.__set_password(value)

    

    @property
    def salt_value(self) -> Union[str, Column[str]]:
        """The value used to salt the Hash Generated for the User.

        Returns:
            salt_value: The Salt Value used for Current User.
        """
        return self.__salt_value
    
    def __set_email(self, value: str) -> UserEmailError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Email value.

        Raises:
            UserEmailError: Invalid User Email.
        """
        if not isinstance(value, str):
            raise UserEmailError("Invalid Type for this Attribute.")
        if not Regex.EMAIL.value.match(value):
            raise UserEmailError("Invalid Email.")
        self.__email = value

    def __set_password(self, value: str) -> UserPasswordError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Password value.

        Raises:
            UserPasswordError: Invalid User Password.
        """
        if not isinstance(value, str):
            raise UserPasswordError("No Password Provided")
        if not Regex.PASSWORD.value.match(value):
            raise UserPasswordError("Invalid User Password.")
        self.__password = get_hash_value(value, self.__salt_value)
