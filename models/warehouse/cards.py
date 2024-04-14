"""Warehouse Module: Contains Card Model for Mapping Cards to Accounts."""

from datetime import date, datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, Date, DateTime, Enum, String, text
from lib.utils.constants.users import CardType, Status
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
        - card_type (CardType): Valid Card Type.
        - status (Status): Valid Card Status.
        - expiration_date (date): Card Expiration date.
        - pin (str): Card Pin.
        - created_date (date): Card Created Date.
        - updated_date (date): Card Updated Date.
        - salt_value (str): Card's Hash Salt Value.

    """

    __tablename__ = "cards"
    __table_args__ = ({"schema": "warehouse"},)

    id: Union[str, Column[str]] = Column(
        "id",
        String(256),
        primary_key=True,
    )
    card_id: Union[str, Column[str]] = Column(
        "card_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
    )
    card_number: Union[str, Column[str]] = Column(
        "card_number", String(256), nullable=False
    )
    cvv_number: Union[str, Column[str]] = Column(
        "cvv_number", String(256), nullable=False
    )
    card_type: Union[CardType, Column[CardType]] = Column(
        "card_type", Enum(CardType), nullable=False
    )
    status: Union[Status, Column[Status]] = Column(
        "status", Enum(Status), nullable=False, default=Status.NEW
    )
    pin: Union[str, Column[str]] = Column("pin", String(256), nullable=False)
    expiration_date: Union[date, Column[date]] = Column(
        "expiration_date", Date, nullable=False
    )
    salt_value: Union[str, Column[str]] = Column(
        "salt_value", String(256), nullable=False
    )
    created_date: Union[datetime, Column[datetime]] = Column(
        "created_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __init__(self):
        """Card Object Constructor."""

        self.id = str(uuid4())
        self.salt_value = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Card Object.

        Returns:
            str: Representation of a Card Object.
        """

        return f"Card ID: {self.card_id}"

    def __repr__(self) -> str:
        """String Representation of the Card Object.

        Returns:
            str: Representation of a Card Object.
        """

        return f"Application Model: {self.__class__.__name__}"


# """
# Card Module

# This module defines classes and abstractions related to archiving
# and warehousing in the application. It includes a Card class
# that encapsulates various aspects of a user, such as user_id.

# Classes:
#     - Card: Class representing a user with various attributes.


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
