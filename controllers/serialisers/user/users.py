"""Users Serialiser Module: Serialiser for User Model."""

from json import dumps
from typing import Union

from sqlalchemy import Column, String, cast, select
from sqlalchemy.orm import Session

from config import AppConfig
from lib.interfaces.exceptions import (
    FernetError,
    UserEmailError,
    UserError,
    UserPasswordError,
)
from lib.utils.constants.users import DateFormat, Regex
from lib.utils.helpers.cards import decrypt_data, encrypt_data
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
    def get_user(cls, user_id: str) -> Union[str, UserError, FernetError]:
        """CRUD Operation: Get User.

        Args:
            user_id (str): Public User ID.

        Returns:
            str: User Object.
        """
        with Session(ENGINE) as session:
            query = select(User).filter(cast(User.user_id, String) == user_id)
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
            user.user_id = user.get_validated_user_id(email, password)

            if not user:
                raise UserError("User not created.")

            user_id = str(user)
            session.add(user)
            session.commit()

            return user_id

    @classmethod
    def update_user(cls, private_id: str, **kwargs) -> str:
        """CRUD Operation: Update User.

        Args:
            id (str): Private User ID.

        Returns:
            str: User Object.
        """
        with Session(ENGINE) as session:
            user = session.get(cls, private_id)

            if user is None:
                raise UserError("User Not Found.")

            for key, value in kwargs.items():
                if key != "password":
                    raise UserError("Invalid attribute to Update.")

                valid_password = user.__get_valid_password__(value)
                valid_user_id = user.get_validated_user_id(
                    decrypt_data(user.email), value
                )
                setattr(user, key, valid_password)
                setattr(user, "user_id", valid_user_id)

            user_id = str(user)
            session.add(user)
            session.commit()

            return user_id

    @classmethod
    def delete_user(cls, private_id: str) -> str:
        """CRUD Operation: Delete User.

        Args:
            id (str): Private User ID.

        Returns:
            str: User Object.
        """
        with Session(ENGINE) as session:
            user = session.get(User, private_id)

            if not user:
                raise UserError("User Not Found")

            session.delete(user)
            session.commit()

            return f"Deleted: {private_id}"

    def __get_valid_email__(
        self, email: str
    ) -> Union[str, ValueError, UserPasswordError, UserError]:
        """Sets the Private Attribute.

        Args:
            email (str): Valid Email.

        Raises:
            UserPasswordError: Invalid User Email.
        """
        UserSerialiser.__validate_email__(email)
        return encrypt_data(email.encode())

    def __get_valid_password__(
        self, password: str
    ) -> Union[str, ValueError, UserPasswordError]:
        """Sets the Private Attribute.

        Args:
            password (str): Valid Password.

        Raises:
            UserPasswordError: Invalid User Password.
        """
        UserSerialiser.__validate_password__(password)
        return str(get_hash_value(password, self.salt_value))

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
            "updated_date": user.updated_date.strftime(DateFormat.HYPHEN.value),
            "email": user.email,
            "password": user.password,
            "salt_value": user.salt_value,
        }
        return encrypt_data(dumps(data).encode())

    @staticmethod
    def __validate_email__(email: str) -> UserEmailError:
        """Validates the Private Attribute.

        Args:
            email (str): Valid Email.

        Raises:
            UserEmailError: Invalid User Email.
        """
        if not isinstance(email, str):
            raise UserEmailError("Invalid Type for this Attribute.")
        if not Regex.EMAIL.value.match(email):
            raise UserEmailError("Invalid Email.")

    @staticmethod
    def __validate_password__(password: str) -> UserPasswordError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Password.

        Raises:
            UserPasswordError: Invalid User Password.
        """
        if not isinstance(password, str):
            raise UserPasswordError("No Password Provided")
        if not Regex.PASSWORD.value.match(password):
            raise UserPasswordError("Invalid User Password.")

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

    @staticmethod
    def get_validated_user_id(
        email: Union[str, Column[str]], password: str
    ) -> Union[str, ValueError, UserEmailError]:
        """Sets the Private Attribute.

        Args:
            email (str): Valid Email.
            password (str): Valid Password.

        Raises:
            UserEmailError: Invalid User.
        """
        UserSerialiser.__validate_email__(email)
        UserSerialiser.__validate_password__(password)
        return str(get_hash_value(str(email) + password, str(AppConfig().salt_value)))
