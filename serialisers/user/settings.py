"""Settings Serialiser Module: Serialiser for SettingsProfile Model."""

from datetime import datetime
from typing import Any, Union
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from lib.interfaces.exceptions import (
    FernetError,
    SettingsProfileError,
)
from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    EmailVerification,
    ProfileVisibility,
    Theme,
)
from models import ENGINE
from models.user.settings import SettingsProfile


class SettingsProfileSerialiser(SettingsProfile):
    """
    Serialiser for the Settings Model.

    Args:
        SettingsProfile (class): Access Point to the SettingsProfile Model.
    """

    @classmethod
    def get_settings_profile(
        cls, settings_id: str
    ) -> Union[dict, SettingsProfileError, FernetError]:
        """CRUD Operation: Get Settings.

        Args:
            settings_id (str): Public Settings ID.

        Returns:
            str: Settings Object.
        """
        with Session(ENGINE) as session:
            query = select(SettingsProfile).filter(
                cast(cls.settings_id, String) == settings_id
            )
            settings_profile = session.execute(query).scalar_one_or_none()

            if not settings_profile:
                raise SettingsProfileError("No Settings Found.")

            return cls.__get_settings_data__(settings_profile)

    @classmethod
    def create_settings_profile(cls, **kwargs) -> str:
        """CRUD Operation: Add Settings.

        Args:
            name (str): Settings Name.
            description (str): Settings Description.
            card_id (str): Settings's Card ID.

        Returns:
            dict: Settings Object.
        """
        with Session(ENGINE) as session:
            settings_profile = cls()

            for key, value in kwargs.items():
                cls.__set_settings__(settings_profile, key, value)

            if not settings_profile:
                raise SettingsProfileError("Settings not created.")

            settings_id = str(settings_profile)
            session.add(settings_profile)
            session.commit()

            return settings_id

    @classmethod
    def update_settings_profile(cls, private_id: str, **kwargs) -> str:
        """CRUD Operation: Update Settings.

        Args:
            id (str): Private Settings ID.

        Returns:
            str: Settings Object.
        """
        with Session(ENGINE) as session:
            settings_profile = session.get(cls, private_id)

            if settings_profile is None:
                raise SettingsProfileError("Settings Not Found.")

            for key, value in kwargs.items():
                cls.__set_settings__(settings_profile, key, value)

            settings_id = str(settings_profile)
            session.add(settings_profile)
            session.commit()

            return settings_id

    @classmethod
    def delete_settings_profile(cls, private_id: str) -> str:
        """CRUD Operation: Delete Settings.

        Args:
            id (str): Private Settings ID.

        Returns:
            str: Settings Object.
        """
        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, private_id)

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found")

            session.delete(settings_profile)
            session.commit()

            return f"Deleted: {private_id}"

    @classmethod
    def __get_settings_data__(cls, settings_profile: SettingsProfile):
        cls.__vallidate_settings_profile__(settings_profile)
        return {
            "id": settings_profile.id,
            "settings_id": settings_profile.settings_id,
            "email_status": settings_profile.email_status,
            "mfa_enabled": settings_profile.mfa_enabled,
            "mfa_last_used_date": settings_profile.mfa_last_used_date,
            "profile_visibility_preference": settings_profile.profile_visibility_preference,
            "data_sharing_preferences": settings_profile.data_sharing_preferences,
            "communication_preference": settings_profile.communication_preference,
            "location_tracking_enabled": settings_profile.location_tracking_enabled,
            "cookies_enabled": settings_profile.cookies_enabled,
            "theme_preference": settings_profile.theme_preference,
        }

    @classmethod
    def __set_settings__(
        cls, settings_profile: SettingsProfile, key: str, value: Any
    ) -> Union[SettingsProfile, SettingsProfileError]:
        if key not in [
            "mfa_enabled",
            "location_tracking_enabled",
            "cookies_enabled",
            "email_status",
            "data_sharing_preferences",
            "communication_preference",
            "theme_preference",
            "profile_visibility_preference",
        ]:
            raise SettingsProfileError("Invalid Setting.")

        if key in [
            "mfa_enabled",
            "location_tracking_enabled",
            "cookies_enabled",
            "mfa_last_used_date",
        ]:
            settings_profile.__validate_primitive_type__(value, bool)
            setattr(settings_profile, key, value)

        if key in ["mfa_last_used_date"]:
            settings_profile.__validate_primitive_type__(value, datetime)
            setattr(settings_profile, key, value)

        if key == "email_status":
            settings_profile.__validate_primitive_type__(value, EmailVerification)
            settings_profile.email_status = value

        if key == "data_sharing_preferences":
            settings_profile.__validate_primitive_type__(value, DataSharingPreference)
            settings_profile.data_sharing_preferences = value

        if key == "communication_preference":
            settings_profile.__validate_primitive_type__(value, Communication)
            settings_profile.communication_preference = value

        if key == "theme_preference":
            settings_profile.__validate_primitive_type__(value, Theme)
            settings_profile.theme_preference = value

        if key == "profile_visibility_preference":
            settings_profile.__validate_profile_visibility__(value)
            settings_profile.profile_visibility_preference = value
        return settings_profile

    @staticmethod
    def __validate_primitive_type__(
        value: Any, primitive: type
    ) -> SettingsProfileError:
        if not isinstance(value, primitive):
            raise SettingsProfileError("Invalid Type for this Attribute.")

    @staticmethod
    def __validate_profile_visibility__(
        visibility: ProfileVisibility,
    ) -> SettingsProfileError:
        SettingsProfileSerialiser.__validate_primitive_type__(
            visibility, ProfileVisibility
        )
        if visibility == ProfileVisibility.ADMIN:
            raise SettingsProfileError("Invalid Profile Visibilty.")

    @staticmethod
    def __vallidate_settings_profile__(
        settings_profile: SettingsProfile,
    ) -> SettingsProfileError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Settings Profile Data.

        Raises:
            SettingsProfileError: Invalid Settings Profile Data.
        """
        for key in [
            settings_profile.id,
            settings_profile.settings_id,
            settings_profile.email_status,
            settings_profile.mfa_enabled,
            settings_profile.profile_visibility_preference,
            settings_profile.data_sharing_preferences,
            settings_profile.communication_preference,
            settings_profile.location_tracking_enabled,
            settings_profile.cookies_enabled,
            settings_profile.theme_preference,
        ]:
            if key is None:
                raise SettingsProfileError("Invalid Settings Profile Data.")
