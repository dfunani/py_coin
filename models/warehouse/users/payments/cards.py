"""Cards Module: Warehouse of Account Cards."""

from datetime import datetime
from random import randint
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, DateTime, Enum, String, text
from config import AppConfig
from lib.interfaces.exceptions import CardValidationError
from lib.utils.constants.users import CardType, CardStatus
from models import Base


class Card(Base):
    """
    Model representing an Account Card.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        - __tablename__ (str): The name of the database table for users.
        - Card_id (str): Card's Public ID.
        - card_number (str): Valid Card Number.
        - cvv_number (str): Valid CVV Number.
        - card_type (str): Valid Card Type.

    """

    __tablename__ = "cards"

    __id: Union[str, Column[str]] = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
        primary_key=True,
    )
    card_id: Union[str, Column[str]] = Column(
        "card_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
    )
    __card_number: Union[str, Column[str]] = Column(
        "card_number", String(256), unique=True, nullable=False
    )
    __cvv_number: Union[str, Column[str]] = Column(
        "cvv_number", String(256), nullable=False
    )
    __card_type: Union[CardType, Column[CardType]] = Column(
        "card_type", Enum(CardType), nullable=False
    )
    __card_status: Union[CardStatus, Column[CardStatus]] = Column(
        "card_status", Enum(CardStatus), nullable=False, default=CardStatus.INACTIVE
    )
    __created_date: Union[datetime, Column[datetime]] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP")
    )
    __updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __init__(self, card_type: CardType, card_number: str):
        """Card Object Constructor.

        Args:
            card_type (CardType): Valid Card Type.
            card_number (str): Valid Card Number.

        Raises:
            CardValidationError: Invalid Card Information.
        """
        self.__id = str(uuid4())
        self.card_id = str(uuid4())
        self.__set_card_type__(card_type)
        self.__set_card_number__(card_number)
        self.__set_cvv_number__()

    def __str__(self) -> str:
        """String Representation of the Card Object.

        Returns:
            str: Representation of a Card Object.
        """
        return f"Card ID: {self.card_id}"

    @property
    def card_number(self) -> Union[str, Column[str]]:
        """Getter For Card Number.

        Returns:
            str: Valid Card Number.
        """
        return self.__card_number

    @property
    def cvv_number(self) -> Union[str, Column[str]]:
        """Getter For CVV Number.

        Returns:
            str: Valid CVV Number.
        """
        return self.__cvv_number

    @property
    def card_type(self) -> Union[CardType, Column[CardType]]:
        """Getter For Card Type.

        Returns:
            str: Valid Card Type.
        """
        return self.__card_type

    @property
    def card_status(self) -> Union[CardStatus, Column[CardStatus]]:
        """Getter For Card Status.

        Returns:
            str: Invalid Access to Card Status Attribute.
        """
        return self.__card_status

    @card_status.setter
    def card_status(self, value: CardStatus) -> CardValidationError:
        """Setter For Card Status.

        Args:
            value (str): Valid Card Status.

        Raises:
            UserEmailError: Invalid Card Status.
        """
        self.__set_card_status__(value)

    def __set_card_number__(self, value: str) -> CardValidationError:
        """Sets the Private Attribute.

        Args:
            value (str): Valid Card Number value.

        Raises:
            CardValidationError: Invalid Card Number Value.
        """
        self.__validate_card_number__(value)
        self.__card_number = self.__card_type.value[1] + value

    def __set_cvv_number__(self):
        """Sets the Private Attribute.

        Args:
            value (str): Valid CVV Number value.

        Raises:
            CardValidationError: Invalid CVV Number Value.
        """
        cvv_number = "".join(
            [str(randint(0, 9)) for _ in range(AppConfig().cvv_length)]
        )
        self.__validate_cvv_number__(cvv_number)
        self.__cvv_number = cvv_number

    def __set_card_type__(self, value: CardType) -> CardValidationError:
        """Sets the Private Attribute.

        Args:
            value (str): Valid Card Type value.

        Raises:
            CardValidationError: Invalid Card Type Value.
        """
        self.__validate_card_type__(value)
        self.__card_type = value

    def __set_card_status__(self, value: CardStatus) -> CardValidationError:
        """Sets the Private Attribute.

        Args:
            value (str): Valid Card Status value.

        Raises:
            CardValidationError: Invalid Card Status Value.
        """
        self.__validate_cvv_status__(value)
        self.__card_status = value

    def __validate_card_number__(self, value: str) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Card Number value.

        Raises:
            CardValidationError: Invalid Card Number value.
        """
        if not isinstance(value, str):
            raise CardValidationError("Invalid Type for this Attribute.")
        card_number = self.__card_type.value[1] + value
        if len(card_number) != AppConfig().card_length:
            raise CardValidationError("Invalid Card Number.")

    def __validate_cvv_number__(self, value: str) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid CVV value.

        Raises:
            CardValidationError: Invalid CVV value.
        """
        if not isinstance(value, str):
            raise CardValidationError("Invalid Type for this Attribute.")
        if len(value) != AppConfig().cvv_length:
            raise CardValidationError("Invalid CVV Number.")

    def __validate_card_type__(self, value: CardType) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Card Type value.

        Raises:
            CardValidationError: Invalid Card Type value.
        """
        if not isinstance(value, CardType):
            raise CardValidationError("Invalid Type for this Attribute.")

    def __validate_card_status__(self, value: CardStatus) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Card Status value.

        Raises:
            CardValidationError: Invalid Card Status value.
        """
        if not isinstance(value, CardStatus):
            raise CardValidationError("Invalid Type for this Attribute.")
        if value not in [CardStatus.ACTIVE, CardStatus.INACTIVE]:
            raise CardValidationError("Invalid Card Status.")


# """
# User Module

# This module defines classes and abstractions related to archiving
# and warehousing in the application. It includes a User class
# that encapsulates various aspects of a user, such as user_id.

# Classes:
#     - User: Class representing a user with various attributes.


# Example:
#     >>> from users import User
#     >>> user = User()
#     >>> user_id = User.id
# """

# from datetime import datetime
# from json import dumps
# from os import getenv
# from typing import Union
# from uuid import uuid4
# from sqlalchemy import Column, DateTime, String, Uuid, text
# from lib.interfaces.types import UserEmailError, UserPasswordError
# from lib.utils.helpers.users import get_hash_value
# from models import Base
# from cryptography.fernet import Fernet
# from lib.utils.constants.users import Regex


# # class Login(Base):
# #     user_id = User()
# #     login_date = Column(
# #         DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now()
# #     )
# #     login_location = Column(String, nullable=False)
# #     login_device = Column(UserDevice)
# #     login_method = Column(Enum(AccountLoginMethod))
# #     is_login_successful = Column(Boolean, nullable=False)
# #     session_id = Column(String(256), nullable=False)
# #     logout_date = Column(DateTime, nullable=True)
# #     logout_location = Column(String, nullable=False)
# #     duration_of_Session = Column(DateTime, nullable=False)
# #     authentication_tokens = Column(String, nullable=False)


# # class Device(Base):
# #     device_id = Column(String, nullable=False)
# #     device_type = Column(String, nullable=False)
# #     operating_system = Column(String, nullable=False)
# #     os_version = Column(String, nullable=False)
# #     device_manufacturer = Column(String, nullable=False)
# #     model_name = Column(String, nullable=False)
# #     number = Column(String, nullable=False)
# #     screen_size = Column(String, nullable=False)
# #     resolution = Column(String, nullable=False)
# #     processor_information = Column(String, nullable=False)
# #     memory_ram = Column(String, nullable=False)
# #     storage_capacity = Column(String, nullable=False)
# #     network_information = Column(String, nullable=False)
# #     imei_udid = Column(String, nullable=False)
# #     battery_information = Column(String, nullable=False)
# #     location_services = Column(String, nullable=False)
# #     last_active_date = Column(String, nullable=False)
# #     user_agent_browser = Column(String, nullable=False)
# #     device_permissions = Column(Enum(UserDevicePermission), nullable=False)
# #     device_status = Column(Enum(AccountStatus), nullable=False)
