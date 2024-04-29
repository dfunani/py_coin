"""Application's (Global) Configurations and Settings."""

from datetime import datetime
from os import getenv
from typing import Union
from uuid import uuid4
from cryptography.fernet import Fernet
from lib.interfaces.exceptions import ApplicationError
from lib.utils.constants.users import DateFormat
from lib.validators.config import (
    validate_card_length,
    validate_cvv_length,
    validate_end_date,
    validate_fernet_key,
    validate_salt_value,
    validate_session_id,
    validate_start_date,
)


class AppConfig:
    """AppConfig Singleton Class."""

    __session__id__ = uuid4()
    __START_DATE__ = datetime.now()
    __end_date__ = datetime.now()
    __SALT_VALUE__ = getenv("SALT_VALUE")
    __FERNET_KEY__ = getenv("FERNET_KEY")
    __CARD_LENGTH__ = 13
    __CVV_LENGTH__ = 3

    def __str__(self) -> str:
        """String Representation of the Application Configuration."""

        return f"Application Session: {self.__session__id__}"

    @property
    def session_id(self) -> str:
        """Getter for Session ID."""

        return str(validate_session_id(self.__session__id__))

    @property
    def start_date(self) -> str:
        """Getter for Start Datetime."""

        return validate_start_date(self.__START_DATE__).strftime(DateFormat.LONG.value)

    @property
    def end_date(self) -> str:
        """Getter for End Datetime."""

        return validate_end_date(self.__end_date__, self.__START_DATE__).strftime(
            DateFormat.LONG.value
        )

    @end_date.setter
    def end_date(self, value: datetime):
        """Getter for End Datetime."""

        self.__end_date__ = validate_end_date(value, self.__START_DATE__)

    @property
    def salt_value(self) -> str:
        """Getter for Salt Value."""

        return validate_salt_value(str(self.__SALT_VALUE__))

    @property
    def card_length(self) -> int:
        """Getter for Card Length."""

        return validate_card_length(self.__CARD_LENGTH__)

    @property
    def cvv_length(self) -> int:
        """Getter for CVV Length."""

        return validate_cvv_length(self.__CVV_LENGTH__)

    @property
    def fernet(self) -> Fernet:
        """Getter for Fernet Key."""

        return Fernet(validate_fernet_key(str(self.__FERNET_KEY__)))
