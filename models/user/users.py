"""Users Module: Contains User Model for Mapping Users."""

from json import dumps
from typing import Union
from uuid import uuid4
from cryptography.fernet import Fernet
from sqlalchemy import Column, DateTime, String, text
from lib.interfaces.exceptions import (
    FernetError,
    UserEmailError,
    UserError,
    UserPasswordError,
)
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
        - user_data (str): Encrypted User Data.

    """

    __tablename__ = "users"

    __id = Column(
        "id", String(256), default=text(f"'{str(uuid4())}'"), primary_key=True
    )
    user_id: Union[str, Column[str]] = Column("user_id", String(256), nullable=False)
    __created_date = Column("created_date", DateTime, default=text("CURRENT_TIMESTAMP"))
    __email: Union[str, Column[str]] = Column(
        "email", String(256), unique=True, nullable=False
    )
    __password: Union[str, Column[str]] = Column(
        "password", String(256), nullable=False
    )
    __salt_value: Union[str, Column[str]] = Column("salt_value", String(256))

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
        self.__set_email__(email)
        self.__set_password__(password)
        self.user_id = get_hash_value(email + password, str(AppConfig().salt_value))

    def __str__(self) -> str:
        """String Representation of the Accounts Object.

        Returns:
            str: Representation of a User Object.
        """
        return f"User ID: {self.user_id}"

    @property
    def user_data(self) -> Union[str, UserError, FernetError]:
        """Getter For User Data.

        Returns:
            str: Encrypted User Data.
        """
        return self.__get_encrypted_user_data__()

    @property
    def password(self) -> UserPasswordError:
        """Getter For User Password.

        Raises:
            UserPasswordlError: Invalid Password Value.
        """
        raise UserPasswordError("Can Not Access Private Attribute: [PASSWORD]")

    @password.setter
    def password(self, value: Union[str, Column[str]]) -> UserPasswordError:
        """Setter For User Pasword.

        Args:
            value (str): Valid Password Value.

        Raises:
            UserEmailError: Invalid Password Value.
        """
        self.__set_password__(str(value))

    @property
    def salt_value(self) -> Union[str, Column[str]]:
        """The value used to salt the Hash Generated for the User.

        Returns:
            salt_value: Valid Salt Value.
        """
        return self.__salt_value

    def __get_encrypted_user_data__(self) -> Union[str, UserError, FernetError]:
        """Public User ID.

        Returns:
            str: Encrypted User Data.
        """
        self.__vallidate_user_data__()
        data = {
            "id": self.__id,
            "user_id": self.user_id,
            "created_date": self.__created_date.strftime(DateFormat.HYPHEN.value),
            "email": self.__email,
            "password": self.__password,
            "salt_value": self.__salt_value,
        }
        fernet = AppConfig().fernet
        if not isinstance(fernet, Fernet):
            raise UserError("Invalid User Data")
        return fernet.encrypt(dumps(data).encode()).decode()

    def __set_email__(self, value: str) -> UserEmailError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Email value.

        Raises:
            UserEmailError: Invalid User Email.
        """
        self.__validate_email__(value)
        self.__email = get_hash_value(value, self.__salt_value)

    def __set_password__(self, value: str) -> UserPasswordError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Password value.

        Raises:
            UserPasswordError: Invalid User Password.
        """
        self.__validate_password__(value)
        self.__password = get_hash_value(value, self.__salt_value)

    def __vallidate_user_data__(self) -> UserError:
        for key in [
            self.__id,
            self.__created_date,
            self.__email,
            self.__password,
            self.__salt_value,
        ]:
            if not key:
                raise UserError("Invalid User.")

    def __validate_email__(self, value: str) -> UserEmailError:
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

    def __validate_password__(self, value: str) -> UserPasswordError:
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
