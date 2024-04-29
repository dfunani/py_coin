"""Warehouse Serialiser Module: Serialiser for Card Model."""

from enum import EnumMeta
from typing import Any, Tuple
from lib.interfaces.exceptions import ApplicationError
from lib.validators.users import (
    validate_balance,
    validate_biography,
    validate_data_sharing_preferences,
    validate_date_of_birth,
    validate_description,
    validate_first_name,
    validate_interests,
    validate_last_name,
    validate_mobile_number,
    validate_name,
    validate_pin,
    validate_profile_visibility_preference,
    validate_social_media_links,
    validate_status,
    validate_username,
)


class BaseSerialiser:
    """A Base/Abstract Serialiser."""

    __table__ = None
    __SERIALISER_EXCEPTION__: type[BaseException] = ApplicationError
    __VALIDATORS__ = {
        # User Profile
        "status": validate_status,
        "first_name": validate_first_name,
        "last_name": validate_last_name,
        "username": validate_username,
        "date_of_birth": validate_date_of_birth,
        "mobile_number": validate_mobile_number,
        "biography": validate_biography,
        "interests": validate_interests,
        "social_media_links": validate_social_media_links,
        # User Card
        "name": validate_name,
        "description": validate_description,
        "balance": validate_balance,
        "pin": validate_pin,
        # Settings
        "data_sharing_preferences": validate_data_sharing_preferences,
        "profile_visibility_preference": validate_profile_visibility_preference,
    }

    def __str__(self) -> str:
        """String Representation of the Base Class."""

        return "Abstract/Base Serialiser."

    def __repr__(self) -> str:
        """String Representation of the Base Class."""

        return f"Application Model: {self.__class__.__name__}"

    def validate_serialiser_kwargs(self, key: str, value: Any) -> Any:
        """Updates Validated Model Attributes."""

        data_type, nullable, validator = self.__get_column_data__(key)

        if not nullable and value is None:
            raise self.__SERIALISER_EXCEPTION__("Non-Nullable Attribute.")

        if not isinstance(value, data_type) and value is not None:
            raise self.__SERIALISER_EXCEPTION__("Invalid Type for this Attribute.")

        if validator is not None and hasattr(validator, "__call__"):
            value = validator(value)

        return value

    def __get_column_data__(self, key: str) -> Tuple[EnumMeta, bool, "function" | None]:
        """Extract a Columns Meta-Data."""

        if not self.__table__:
            raise self.__SERIALISER_EXCEPTION__("Invalid Table Meta Data")

        column = dict(self.__table__.columns).get(key)
        return (
            column.type.python_type,
            column.nullable,
            self.__VALIDATORS__.get(column.name),
        )
