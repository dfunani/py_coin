"""Users Serialiser Module: Serialiser for User Model."""

from json import dumps
from typing import Union

from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session

from cryptography.fernet import Fernet

from config import AppConfig
from lib.interfaces.exceptions import (
    FernetError,
    UserEmailError,
    UserError,
    UserPasswordError,
)
from lib.utils.constants.users import DateFormat, Regex
from lib.utils.helpers.users import get_hash_value
from models import ENGINE
from models.user.users import User


class UserSerialiser(User):
    """
    Serialiser for the User Model.

    Args:
        User (class): Access Point to the User Model.
    """

    @classmethod
    def get_user(cls, email: str, password: str) -> str:
        """CRUD Operation: Get User.

        Args:
            email (str): User Email.
            password (str): User Password.

        Returns:
            str: User Object.
        """
        with Session(ENGINE) as session:
            valid_email = cls.__get_valid_email__(email)
            cls.__validate_password__(password)
            user_id = cls.__get_valid_user_id__(str(valid_email), password)

            query = select(User).where(cast(User.user_id, String) == user_id)
            user = session.execute(query).scalar_one_or_none()

            if not user:
                raise UserError("No User Found.")

            return cls.__get_encrypted_user_data__(user)

    @classmethod
    def create_user(cls, email: str, password: str) -> str:
        """CRUD Operation: Add User.

        Args:
            email (str): User Email.
            password (str): Email Password.

        Returns:
            str: User Object.
        """
        with Session(ENGINE) as session:
            user = cls()

            user.email = user.__get_valid_email__(email)
            user.password = user.__get_valid_password__(password)
            user.user_id = user.__get_valid_user_id__(user.email, password)

            if not user:
                raise UserError("User not created.")

            user_id = str(user)
            session.add(user)
            session.commit()

            return user_id

    @classmethod
    def update_user(cls, id: str, **kwargs) -> str:
        """CRUD Operation: Update User.

        Args:
            id (str): Private User ID.

        Returns:
            str: User Object.
        """
        with Session(ENGINE) as session:
            query = select(cls).filter(cast(User.id, String) == id)
            user = session.execute(query).scalar_one_or_none()

            if user is None:
                raise UserError("User Not Found.")

            for key, value in kwargs.items():
                if key != "password":
                    raise UserError("Invalid attribute to Update.")

                valid_password = user.__get_valid_password__(value)
                valid_user_id = user.__get_valid_user_id__(str(user.email), value)
                setattr(user, key, valid_password)
                setattr(user, "user_id", valid_user_id)

            user_id = str(user)
            session.add(user)
            session.commit()

            return user_id

    @classmethod
    def delete_user(cls, id: str) -> str:
        """CRUD Operation: Delete User.

        Args:
            id (str): Private User ID.

        Returns:
            str: User Object.
        """
        with Session(ENGINE) as session:
            user = session.get(User, id)

            if not user:
                raise UserError("User Not Found")

            session.delete(user)
            session.commit()
            return f"Deleted: {id}"

    @classmethod
    def __get_valid_email__(cls, email: str) -> Union[str, ValueError, UserEmailError]:
        """Sets the Private Attribute.

        Args:
            email (str): Valid Email value.

        Raises:
            UserEmailError: Invalid User Email.
        """
        UserSerialiser.__validate_email__(email)
        return str(get_hash_value(email, str(AppConfig().salt_value)))

    @staticmethod
    def __validate_email__(email: str) -> UserEmailError:
        """Validates the Private Attribute.

        Args:
            email (str): Valid Email value.

        Raises:
            UserEmailError: Invalid User Email.
        """
        if not isinstance(email, str):
            raise UserEmailError("Invalid Type for this Attribute.")
        if not Regex.EMAIL.value.match(email):
            raise UserEmailError("Invalid Email.")

    def __get_valid_password__(
        self, password: str
    ) -> Union[str, ValueError, UserPasswordError]:
        """Sets the Private Attribute.

        Args:
            password (str): Valid Password value.

        Raises:
            UserPasswordError: Invalid User Password.
        """
        UserSerialiser.__validate_password__(password)
        return str(get_hash_value(password, self.salt_value))

    @staticmethod
    def __validate_password__(password: str) -> UserPasswordError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Password value.

        Raises:
            UserPasswordError: Invalid User Password.
        """
        if not isinstance(password, str):
            raise UserPasswordError("No Password Provided")
        if not Regex.PASSWORD.value.match(password):
            raise UserPasswordError("Invalid User Password.")

    @classmethod
    def __get_valid_user_id__(
        cls, email: str, password: str
    ) -> Union[str, ValueError, UserEmailError]:
        """Sets the Private Attribute.

        Args:
            email (str): Valid Email value.
            password (str): Valid Password value.

        Raises:
            UserEmailError: Invalid User.
        """
        return str(get_hash_value(email + password, str(AppConfig().salt_value)))

    @classmethod
    def __get_encrypted_user_data__(
        cls, user: User
    ) -> Union[str, UserError, FernetError]:
        """Get User Information.

        Returns:
            str: Encrypted User Data.
        """
        cls.__vallidate_user__(user)
        data = {
            "id": user.id,
            "created_date": user.created_date.strftime(DateFormat.HYPHEN.value),
            "email": user.email,
            "password": user.password,
            "salt_value": user.salt_value,
        }
        fernet = AppConfig().fernet
        if not isinstance(fernet, Fernet):
            raise UserError("Invalid User Data")
        return fernet.encrypt(dumps(data).encode()).decode()

    @staticmethod
    def __vallidate_user__(user: User) -> UserError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid User Data.

        Raises:
            UserEmailError: Invalid User Data.
        """
        for key in [
            user.id,
            user.created_date,
            user.email,
            user.password,
            user.salt_value,
        ]:
            if not key:
                raise UserError("Invalid User Data.")
