from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, text
from sqlalchemy.orm import relationship
from lib.interfaces.exceptions import CardValidationError
from lib.utils.constants.users import AccountPaymentType, CardStatus
from models import Base


class Cards(Base):
    __tablename__ = "cards"

    __id = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
        primary_key=True,
    )
    card_id = Column(
        "card_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
    )
    __card_number = Column("card_number", String(256), unique=True, nullable=False)
    __card_type = Column("card_type", Enum(AccountPaymentType), nullable=False)
    __card_status = Column("card_status", Enum(CardStatus), nullable=False, default=CardStatus.INACTIVE)
    __created_date: Union[datetime, Column[datetime]] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP")
    )
    __updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __init__(
        self,
        card_number: str,
        card_type: AccountPaymentType,
        **kwargs
    ):
        self.__set_card_number(card_number)
        self.__set_card_type(card_type)
        self.id = str(uuid4())
        self.card_id = str(uuid4())
        super().__init__(**kwargs)

    @property
    def card_number(self):
        return self.__card_number

    @property
    def card_type(self):
        return self.__card_type

    @property
    def card_status(self):
        raise CardValidationError("Can Not Access Private Attribute: [Card Status]")

    @card_status.setter
    def card_status(self, value: CardStatus) -> CardValidationError:
        self.__set_card_status(value)

    def __set_card_number(self, value: str) -> CardValidationError:
        if not isinstance(value, str):
            raise CardValidationError("Invalid Type for this Attribute.")
        if len(value) != 20 or not value[:4] in [
            card.value[1] for card in AccountPaymentType
        ]:
            raise CardValidationError("Invalid Card Number.")
        self.__card_number = value

    def __set_card_type(self, value: AccountPaymentType) -> CardValidationError:
        if not isinstance(value, AccountPaymentType):
            raise CardValidationError("Invalid Type for this Attribute.")
        if value.value[1] != self.__card_number[:4]:
            raise CardValidationError("Invalid Card Type.")
        self.__card_type = value

    def __set_card_status(self, value: CardStatus) -> CardValidationError:
        if not isinstance(value, CardStatus):
            raise CardValidationError("Invalid Type for this Attribute.")
        if value not in [CardStatus.ACTIVE, CardStatus.INACTIVE]:
            raise CardValidationError("Invalid Card Status.")
        self.__card_status = value


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
