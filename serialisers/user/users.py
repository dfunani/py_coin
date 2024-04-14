"""User Serialiser Module: Serialiser for User Model."""

from json import dumps
from typing import Union

from sqlalchemy import Column, String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from lib.interfaces.exceptions import (
    FernetError,
    UserError,
)
from lib.utils.constants.users import DateFormat, Role, Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.users import validate_email, validate_password, validate_status
from models import ENGINE
from models.user.users import User


class UserSerialiser(User):
    """
    Singleton Serialiser for the User Model.

    Args:
        User (class): Access Point to the User Model.
    """

    def get_user(self, user_id: str) -> Union[str, UserError, FernetError]:
        """CRUD Operation: Read User.

        Args:
            user_id (str): Public User ID.

        Returns:
            str: User Object.

        Raises:
            UserError: No User Found.
        """
        with Session(ENGINE) as session:
            query = select(User).filter(cast(User.user_id, String) == user_id)
            user = session.execute(query).scalar_one_or_none()

            if not user:
                raise UserError("User Not Found.")

            return self.__get_encrypted_user_data__(user)

    def create_user(self, email: str, password: str) -> Union[str, UserError]:
        """CRUD Operation: Create User.

        Args:
            email (str): User Email.
            password (str): User Password.

        Returns:
            str: User Object.

        Raises:
            UserError: No User Created.
        """
        with Session(ENGINE) as session:
            self.email = str(self.__get_valid_email__(email))
            self.password = str(self.__get_valid_password__(password))
            self.user_id = str(self.__get_valid_user_id__(str(email), password))

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User Not created.") from exc

            return str(self)

    def update_user(
        self,
        private_id: str,
        status: Union[Status, None] = None,
        password: Union[str, None] = None,
    ) -> Union[str, UserError]:
        """CRUD Operation: Update User.

        Args:
            id (str): Private User ID.

        Returns:
            str: User Object.

        Raises:
            UserError: No User Found.
        """
        with Session(ENGINE) as session:
            user = session.get(User, private_id)

            if user is None:
                raise UserError("User Not Found.")

            if password:
                valid_password = self.__get_valid_password__(password)
                valid_user_id = self.__get_valid_user_id__(
                    str(decrypt_data(str(user.email))), password
                )
                setattr(user, "password", valid_password)
                setattr(user, "user_id", valid_user_id)

            if status:
                validate_status(status)
                setattr(user, "status", status)

            try:
                session.add(user)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User not Updated.") from exc

            return str(user)

    def delete_user(self, private_id: str) -> Union[str, UserError]:
        """CRUD Operation: Delete User.

        Args:
            id (str): Private User ID.

        Returns:
            str: User Object.

        Raises:
            UserError: No User Found.
        """
        with Session(ENGINE) as session:
            user = session.get(User, private_id)

            if not user:
                raise UserError("User Not Found")

            try:
                session.delete(user)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User not Deleted.") from exc

            return f"Deleted: {private_id}"

    def __get_valid_email__(self, email: str) -> Union[str, UserError]:
        """Get Valid Email.

        Args:
            email (str): Valid Email.

        Returns:
            str: Encrypted Email.

        Raises:
            UserError: Invalid Email.
        """
        validate_email(email)
        return encrypt_data(email.encode())

    def __get_valid_password__(self, password: str) -> Union[str, UserError]:
        """Get Valid Password.

        Args:
            password (str): Valid Password.

        Returns:
            str: Encrypted Password.

        Raises:
            UserError: Invalid Password.
        """
        validate_password(password)
        return str(get_hash_value(password, self.salt_value))

    def __get_encrypted_user_data__(
        self, user: User
    ) -> Union[str, UserError, FernetError]:
        """Get User Data.

        Args:
            user (User): Unencrypted User.

        Returns:
            str: Encrypted User Data.

        Raises:
            UserError: Invalid User Data.
            FernetError: Invalid Encryption.
        """
        data = {
            "id": user.id,
            "user_id": user.user_id,
            "created_date": user.created_date.strftime(DateFormat.HYPHEN.value),
            "updated_date": user.updated_date.strftime(DateFormat.HYPHEN.value),
            "email": user.email,
            "password": user.password,
            "salt_value": user.salt_value,
            "status": user.status.value,
            "role": Role.USER.value,
        }
        return encrypt_data(dumps(data).encode())

    def __get_valid_user_id__(
        self, email: Union[str, Column[str]], password: str
    ) -> Union[str, ValueError, UserError]:
        """Get Valid User ID.

        Args:
            email (str): Valid Email.
            password (str): Valid Password.

        Returns:
            str: Valid User Object.

        Raises:
            ValueError: Invalid User.
            UserError: Invalid User Data.
        """
        validate_email(str(email))
        validate_password(password)
        return get_hash_value(str(email) + password, str(AppConfig().salt_value))
