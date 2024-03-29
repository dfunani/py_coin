"""Application's (Global) Configurations and Settings."""

from datetime import datetime
from os import getenv
from typing import Union
from cryptography.fernet import Fernet
from lib.interfaces.exceptions import ApplicationError
from lib.utils.constants.users import DateFormat


class AppConfig:
    """AppConfig Singleton Class."""

    __START_DATE__ = datetime.now()
    __END_DATE__ = datetime.now()
    __SALT_VALUE__ = getenv("SALT_VALUE") or ""
    __FERNET_KEY__ = getenv("FERNET_KEY") or ""
    __CARD_LENGTH__ = 13
    __CVV_LENGTH__ = 3

    @property
    def start_date(self) -> Union[str, ApplicationError]:
        """Getter for Start Datetime.

        Raises:
            ApplicationError: Invalid Start Date.

        Returns:
            str: Valid Start Date.
        """
        self.__validate_start_date__()
        return self.__START_DATE__.strftime(DateFormat.LONG.value)

    @property
    def end_date(self) -> Union[str, ApplicationError]:
        """Getter for End Datetime.

        Raises:
            ApplicationError: Invalid End Date.

        Returns:
            str: Valid End Date.
        """
        self.__validate_end_date__()
        return AppConfig.__END_DATE__.strftime(DateFormat.LONG.value)

    @end_date.setter
    def end_date(self, value: datetime) -> ApplicationError:
        """Getter for End Datetime.

        Args:
            value (datetime): Valid End Date.

        Raises:
            ApplicationError: Invalid End Date.

        Returns:
            str: Valid End Date.
        """
        self.__validate_end_date__()
        AppConfig.__END_DATE__ = value

    @property
    def salt_value(self) -> Union[str, ApplicationError]:
        """Getter for Salt Value.

        Raises:
            ApplicationError: Invalid Salt Value.

        Returns:
            str: Valid Salt Value.
        """
        self.__set_salt_value__()
        return AppConfig.__SALT_VALUE__

    @property
    def card_length(self) -> Union[int, ApplicationError]:
        """Getter for Card Length.

        Raises:
            ApplicationError: Invalid Card Length.

        Returns:
            int: Valid Card Length.
        """
        self.__validate_card_length__()
        return self.__CARD_LENGTH__

    @property
    def cvv_length(self) -> Union[int, ApplicationError]:
        """Getter for CVV Length.

        Raises:
            ApplicationError: Invalid CVV Length.

        Returns:
            int: Valid CVV Length.
        """
        self.__validate_cvv_length__()
        return self.__CVV_LENGTH__

    @property
    def fernet(self) -> Union[Fernet, ApplicationError]:
        """Getter for Fernet Key.

        Raises:
            ApplicationError: Invalid Fernet Key.

        Returns:
            str: Valid Fernet Key.
        """
        self.__set_fernet_key__()
        return Fernet(self.__FERNET_KEY__)

    def __validate_start_date__(self) -> ApplicationError:
        """Validates Start Date."""
        if not isinstance(self.__START_DATE__, datetime):
            raise ApplicationError("Invalid Type for this Attribute. [Start Date]")

    def __validate_end_date__(self) -> ApplicationError:
        """Validates End Date."""
        if not isinstance(self.__END_DATE__, datetime):
            raise ApplicationError("Invalid Type for this Attribute. [End Date]")
        if self.__END_DATE__ <= self.__START_DATE__:
            raise ApplicationError("Invalid End Date.")

    def __set_salt_value__(self) -> ApplicationError:
        """Validates Salt Value."""
        if not isinstance(self.__SALT_VALUE__, str):
            raise ApplicationError("Invalid Type for this Attribute. [Salt Value]")
        if not self.__SALT_VALUE__:
            raise ApplicationError("Invalid Salt Value")

    def __set_fernet_key__(self) -> ApplicationError:
        """Validates Fernet Key."""
        if not isinstance(self.__FERNET_KEY__, str):
            raise ApplicationError("Invalid Type for this Attribute. [Fernet Key]")
        if not self.__FERNET_KEY__:
            raise ApplicationError("Invalid Fernet Key.")

    def __validate_card_length__(self):
        """Validates Card length."""
        if not isinstance(self.__CARD_LENGTH__, int):
            raise ApplicationError("Invalid Type for this Attribute. [Card Length]")
        if self.__CARD_LENGTH__ <= 0:
            raise ApplicationError("Invalid Card Length.")

    def __validate_cvv_length__(self):
        """Validates CVV Length."""
        if not isinstance(self.__CVV_LENGTH__, int):
            raise ApplicationError("Invalid Type for this Attribute. [CVV Length]")
        if self.__CVV_LENGTH__ <= 0:
            raise ApplicationError("Invalid CVV Length.")
