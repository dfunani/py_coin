"""Settings Serialiser Module: Serialiser for SettingsProfile Model."""

from datetime import datetime
from typing import Union

from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from lib.interfaces.exceptions import (
    FernetError,
    SettingsProfileError,
)
from lib.utils.constants.users import (
    Communication,
    Verification,
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

    __MUTABLE_ATTRIBUTES__ = {
        "mfa_enabled": bool,
        "location_tracking_enabled": bool,
        "cookies_enabled": bool,
        "email_status": Verification,
        "data_sharing_preferences": list,
        "communication_preference": Communication,
        "theme_preference": Theme,
        "profile_visibility_preference": ProfileVisibility,
        "mfa_last_used_date": datetime,
        "communication_status": Verification,
    }

    def get_settings_profile(
        self, settings_id: str
    ) -> Union[dict, SettingsProfileError, FernetError]:
        """CRUD Operation: Get Settings.

        Args:
            settings_id (str): Public Settings ID.

        Returns:
            str: Settings Object.
        """
        with Session(ENGINE) as session:
            query = select(SettingsProfile).filter(
                cast(SettingsProfile.settings_id, String) == settings_id
            )
            settings_profile = session.execute(query).scalar_one_or_none()

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found.")

            return self.__get_settings_data__(settings_profile)

    def create_settings_profile(self, account_id) -> str:
        """CRUD Operation: Add Settings.

        Args:
            name (str): Settings Name.
            description (str): Settings Description.
            card_id (str): Settings's Card ID.

        Returns:
            dict: Settings Object.
        """
        with Session(ENGINE) as session:
            self.account_id = account_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings Not Created.") from exc

            return str(self)

    def update_settings_profile(self, private_id: str, **kwargs) -> str:
        """CRUD Operation: Update Settings.

        Args:
            id (str): Private Settings ID.

        Returns:
            str: Settings Object.
        """
        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, private_id)

            if settings_profile is None:
                raise SettingsProfileError("Settings Not Found.")

            for key, value in kwargs.items():
                if key not in SettingsProfileSerialiser.__MUTABLE_ATTRIBUTES__:
                    raise SettingsProfileError("Invalid Setting.")

                if (
                    key == "mfa_last_used_date"
                    and not isinstance(value, datetime)
                    and value is not None
                ) or (
                    not isinstance(
                        value, SettingsProfileSerialiser.__MUTABLE_ATTRIBUTES__[key]
                    )
                    and key != "mfa_last_used_date"
                ):
                    raise SettingsProfileError("Invalid Type for Attribute.")

                if (
                    key == "profile_visibility_preference"
                    and value == ProfileVisibility.ADMIN
                ):
                    raise SettingsProfileError("Invalid Profile Visibilty.")

            session.add(settings_profile)
            session.commit()

            return str(settings_profile)

    def delete_settings_profile(self, private_id: str) -> str:
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

    def __get_settings_data__(self, settings_profile: SettingsProfile):
        data = {
            "id": settings_profile.id,
            "settings_id": settings_profile.settings_id,
            "account_id": settings_profile.account_id,
            "email_status": settings_profile.email_status,
            "communication_status": settings_profile.communication_status,
            "mfa_enabled": settings_profile.mfa_enabled,
            "mfa_last_used_date": settings_profile.mfa_last_used_date,
            "profile_visibility_preference": settings_profile.profile_visibility_preference,
            "data_sharing_preferences": settings_profile.data_sharing_preferences,
            "communication_preference": settings_profile.communication_preference,
            "location_tracking_enabled": settings_profile.location_tracking_enabled,
            "cookies_enabled": settings_profile.cookies_enabled,
            "theme_preference": settings_profile.theme_preference,
        }
        return data
