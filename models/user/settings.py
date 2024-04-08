"""Settings Module: Contains User Settings."""

from typing import Union
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Enum, String, ARRAY

from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    EmailVerification,
    ProfileVisibility,
    Theme,
)
from models import Base


class SettingsProfile(Base):
    """Model representing a User's Settings Information.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        id (str): Unique Private Profile ID.
        settings_id (str): Unique Public Profile ID.
        email_status (EmailVerification): Status of the User's Email.
        mfa_enabled (bool): Has MFA Been Enabled.
        mfa_last_used_date (datetime): Last login with MFA.
        profile_visibility (ProfileVisibility): Visibility of the profile.
        data_sharing_preferences (list[DataSharingPreferences]): Preferences for Data Sharing.
        communication_preference (CommunicationPreferences): Preferences for Data Sharing.
        location_tracking_enabled (bool): Has Location Tracking been Enabled.
        cookies_enabled (bool): Have Cookies been Enabled.
        theme_preference (Themes): User Theme Preference.
    """

    __tablename__ = "settings_profiles"

    id: Union[str, Column[str]] = Column("id", String(256), primary_key=True)
    settings_id: Union[str, Column[str]] = Column(
        "settings_id", String(256), nullable=False
    )
    # account_id: Column[str] = Column(
    #     "account_id", ForeignKey("accounts.id"), nullable=False
    # )
    email_status: Union[EmailVerification, Column[EmailVerification]] = Column(
        "email_status", Enum(EmailVerification), default=EmailVerification.UNVERIFIED
    )
    mfa_enabled = Column("mfa_enabled", Boolean, default=False)
    mfa_last_used_date = Column("mfa_last_used_date", DateTime, nullable=True)
    profile_visibility_preference: Union[
        ProfileVisibility, Column[ProfileVisibility]
    ] = Column(
        "profile_visibility_preference",
        Enum(ProfileVisibility),
        default=ProfileVisibility.PUBLIC,
    )
    data_sharing_preferences: Union[
        list[DataSharingPreference], Column[list[DataSharingPreference]]
    ] = Column(
        "data_sharing_preferences",
        ARRAY(Enum(DataSharingPreference, name="data_sharing_preference")),
        default=[DataSharingPreference.ACCOUNT],
    )
    communication_preference: Union[Communication, Column[Communication]] = Column(
        "communication_preference", Enum(Communication), default=Communication.EMAIL
    )
    location_tracking_enabled = Column(
        "location_tracking_enabled", Boolean, default=False
    )
    cookies_enabled = Column("cookies_enabled", Boolean, default=False)
    theme_preference: Union[Theme, Column[Theme]] = Column(
        "theme_preference", Enum(Theme), nullable=False, default=Theme.LIGHT
    )

    def __init__(self) -> None:
        """Settings Object Constructor."""
        self.id = str(uuid4())
        self.settings_id = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Settings Object.

        Returns:
            str: Representation of a Settings Object.
        """
        return f"Settings Profile ID: {self.settings_id}"

    def __repr__(self) -> str:
        """String Representation of the Settings Object.

        Returns:
            str: Representation of a Settings Object.
        """
        return f"Application Model: {self.__class__.__name__}"
