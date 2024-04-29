"""Users Serialiser Module: Serialiser for User Model."""

from enum import Enum
from json import dumps

from sqlalchemy import Column, String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from lib.interfaces.exceptions import UserError
from lib.utils.constants.users import Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.users import validate_email, validate_password, validate_status
from models import ENGINE
from models.user.users import User
from serialisers.serialiser import BaseSerialiser


class UserSerialiser(User, BaseSerialiser):
    """Serialiser for the User Model."""

    __SERIALISER_EXCEPTION__ = UserError
    __MUTABLE_KWARGS__: list[str] = []

    def get_user(self, user_id: str) -> str:
        """CRUD Operation: Read User."""

        with Session(ENGINE) as session:
            query = select(User).filter(cast(User.user_id, String) == user_id)
            user = session.execute(query).scalar_one_or_none()

            if not user:
                raise UserError("User Not Found.")

            return self.__get_encrypted_user_data__(user)

    def create_user(self, email: str, password: str) -> str:
        """CRUD Operation: Create User."""

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
        status: Status | None = None,
        password: str | None = None,
    ) -> str:
        """CRUD OperatiFon: Update User."""

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

    def delete_user(self, private_id: str) -> str:
        """CRUD Operation: Delete User."""

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

    def __get_valid_email__(self, email: str) -> str:
        """Get Valid Email."""

        validate_email(email)
        return encrypt_data(email.encode())

    def __get_valid_password__(self, password: str) -> str:
        """Get Valid Password."""

        validate_password(password)
        return str(get_hash_value(password, str(self.salt_value)))

    def __get_encrypted_user_data__(self, user: User) -> str:
        """Get User Data."""

        data = user.to_dict()
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = key.value
        return encrypt_data(dumps(data).encode())

    def __get_valid_user_id__(self, email: str | Column[str], password: str) -> str:
        """Get Valid User ID."""

        validate_email(str(email))
        validate_password(password)
        return get_hash_value(str(email) + password, str(AppConfig().salt_value))
