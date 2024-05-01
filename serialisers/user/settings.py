"""Users Serialiser Module: Serialiser for SettingsProfile Model."""

from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from lib.interfaces.exceptions import (
    SettingsProfileError,
)
from models import ENGINE
from models.user.settings import SettingsProfile
from serialisers.serialiser import BaseSerialiser


class SettingsProfileSerialiser(SettingsProfile, BaseSerialiser):
    """Serialiser for the Settings Model."""

    __SERIALISER_EXCEPTION__ = SettingsProfileError
    __MUTABLE_KWARGS__: list[str] = [
        "mfa_enabled",
        "location_tracking_enabled",
        "cookies_enabled",
        "email_status",
        "data_sharing_preferences",
        "communication_preference",
        "theme_preference",
        "profile_visibility_preference",
        "mfa_last_used_date",
        "communication_status",
    ]

    def get_settings_profile(self, settings_id: str) -> dict:
        """CRUD Operation: Get Settings."""

        with Session(ENGINE) as session:
            query = select(SettingsProfile).filter(
                cast(SettingsProfile.settings_id, String) == settings_id
            )
            settings_profile = session.execute(query).scalar_one_or_none()

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found.")

            return self.__get_settings_data__(settings_profile)

    def create_settings_profile(self, account_id: str) -> str:
        """CRUD Operation: Add Settings."""

        with Session(ENGINE) as session:
            self.account_id = account_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings Not Created.") from exc

            return str(self)

    def update_settings_profile(self, private_id: str, **kwargs) -> str:
        """CRUD Operation: Update Settings."""

        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, private_id)

            if settings_profile is None:
                raise SettingsProfileError("Settings Not Found.")

            for key, value in kwargs.items():
                if key not in SettingsProfileSerialiser.__MUTABLE_KWARGS__:
                    raise SettingsProfileError("Invalid Setting to Update.")

                value = self.validate_serialiser_kwargs(key, value)
                setattr(settings_profile, key, value)

            try:
                session.add(settings_profile)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings not Updated.") from exc

            return str(settings_profile)

    def delete_settings_profile(self, private_id: str) -> str:
        """CRUD Operation: Delete Settings."""

        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, private_id)

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found")

            try:
                session.delete(settings_profile)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings not Deleted.") from exc

            return f"Deleted: {private_id}"

    def __get_settings_data__(self, settings_profile: SettingsProfile) -> dict:
        """Gets the Settings Data."""

        data = settings_profile.to_dict()
        return data
