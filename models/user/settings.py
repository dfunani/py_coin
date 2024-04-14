"""Users Module: Contains User Settings."""

from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, ARRAY, text

from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    Verification,
    ProfileVisibility,
    Theme,
)
from models import Base


class SettingsProfile(Base):
    """Model representing a User's Settings."""

    __tablename__ = "settings_profiles"
    __table_args__ = ({"schema": "users"},)

    id: Union[str, Column[str]] = Column(
        "id", String(256), primary_key=True, nullable=False
    )
    settings_id: Union[str, Column[str]] = Column(
        "settings_id", String(256), nullable=False
    )
    account_id: Column[str] = Column(
        "account_id", ForeignKey("users.accounts.id"), nullable=False
    )
    email_status: Union[Verification, Column[Verification]] = Column(
        "email_status",
        Enum(Verification, name="email_verification"),
        default=Verification.UNVERIFIED,
        nullable=False,
    )
    communication_status: Union[Verification, Column[Verification]] = Column(
        "communication_status",
        Enum(Verification, name="communication_verification"),
        default=Verification.UNVERIFIED,
        nullable=False,
    )
    mfa_enabled = Column("mfa_enabled", Boolean, default=False)
    mfa_last_used_date = Column("mfa_last_used_date", DateTime, nullable=True)
    profile_visibility_preference: Union[
        ProfileVisibility, Column[ProfileVisibility]
    ] = Column(
        "profile_visibility_preference",
        Enum(ProfileVisibility, name="profilevisibility"),
        default=ProfileVisibility.PUBLIC,
        nullable=False,
    )
    data_sharing_preferences: Union[
        list[DataSharingPreference], Column[list[DataSharingPreference]]
    ] = Column(
        "data_sharing_preferences",
        ARRAY(Enum(DataSharingPreference, name="data_sharing_preference")),
        default=[DataSharingPreference.ACCOUNT],
        nullable=False,
    )
    communication_preference: Union[Communication, Column[Communication]] = Column(
        "communication_preference",
        Enum(Communication, name="communication"),
        default=Communication.EMAIL,
        nullable=False,
    )
    location_tracking_enabled = Column(
        "location_tracking_enabled", Boolean, default=False, nullable=False
    )
    cookies_enabled = Column("cookies_enabled", Boolean, default=False, nullable=False)
    theme_preference: Union[Theme, Column[Theme]] = Column(
        "theme_preference",
        Enum(Theme, name="theme"),
        nullable=False,
        default=Theme.LIGHT,
    )
    created_date: Union[datetime, Column[datetime]] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
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
