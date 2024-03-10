"""
User Module

This module defines classes and abstractions related to archiving and warehousing in the application. It includes a User class
that encapsulates various aspects of a user, such as user_id.

Classes:
    - User: Class representing a user with various attributes.
    

Example:
    >>> from users import User
    >>> user = User()
    >>> user_id = User.id
"""

from datetime import datetime
from json import dumps
from os import getenv
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, DateTime, String, Uuid, text
from lib.interfaces.types import UserEmailError, UserPasswordError
from lib.utils.helpers.users import get_hash_value
from models import Base
from cryptography.fernet import Fernet
from lib.utils.constants.users import Regex


# class Login(Base):
#     user_id = User()
#     login_date = Column(
#         DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now()
#     )
#     login_location = Column(String, nullable=False)
#     login_device = Column(UserDevice)
#     login_method = Column(Enum(AccountLoginMethod))
#     is_login_successful = Column(Boolean, nullable=False)
#     session_id = Column(String(256), nullable=False)
#     logout_date = Column(DateTime, nullable=True)
#     logout_location = Column(String, nullable=False)
#     duration_of_Session = Column(DateTime, nullable=False)
#     authentication_tokens = Column(String, nullable=False)


# class Device(Base):
#     device_id = Column(String, nullable=False)
#     device_type = Column(String, nullable=False)
#     operating_system = Column(String, nullable=False)
#     os_version = Column(String, nullable=False)
#     device_manufacturer = Column(String, nullable=False)
#     model_name = Column(String, nullable=False)
#     number = Column(String, nullable=False)
#     screen_size = Column(String, nullable=False)
#     resolution = Column(String, nullable=False)
#     processor_information = Column(String, nullable=False)
#     memory_ram = Column(String, nullable=False)
#     storage_capacity = Column(String, nullable=False)
#     network_information = Column(String, nullable=False)
#     imei_udid = Column(String, nullable=False)
#     battery_information = Column(String, nullable=False)
#     location_services = Column(String, nullable=False)
#     last_active_date = Column(String, nullable=False)
#     user_agent_browser = Column(String, nullable=False)
#     device_permissions = Column(Enum(UserDevicePermission), nullable=False)
#     device_status = Column(Enum(AccountStatus), nullable=False)
