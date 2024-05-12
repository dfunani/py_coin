"""Users: Settings Profile Model."""

from datetime import datetime
from uuid import uuid4, UUID as uuid
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    ARRAY,
    text,
)

from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    Verification,
    ProfileVisibility,
    Theme,
)
from models import Base
from models.model import BaseModel


class SettingsProfile(Base, BaseModel):
    """Model representing a User's Settings."""

    __tablename__ = "settings_profiles"
    __table_args__ = ({"schema": "users"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: uuid | Column[uuid] = Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False
    )
    settings_id: uuid | Column[uuid] = Column(
        "settings_id", UUID(as_uuid=True), nullable=False
    )
    account_id: uuid | Column[uuid] = Column(
        "account_id",
        UUID(as_uuid=True),
        ForeignKey("users.accounts.id"),
        nullable=False,
    )
    email_status: Verification | Column[Verification] = Column(
        "email_status",
        Enum(Verification, name="email_verification"),
        default=Verification.UNVERIFIED,
        nullable=False,
    )
    communication_status: Verification | Column[Verification] = Column(
        "communication_status",
        Enum(Verification, name="communication_verification"),
        default=Verification.UNVERIFIED,
        nullable=False,
    )
    mfa_enabled = Column("mfa_enabled", Boolean, default=False, nullable=False)
    mfa_last_used_date = Column("mfa_last_used_date", DateTime, nullable=True)
    profile_visibility_preference: ProfileVisibility | Column[ProfileVisibility] = (
        Column(
            "profile_visibility_preference",
            Enum(ProfileVisibility, name="profilevisibility"),
            default=ProfileVisibility.PUBLIC,
            nullable=False,
        )
    )
    data_sharing_preferences: (
        list[DataSharingPreference] | Column[list[DataSharingPreference]]
    ) = Column(
        "data_sharing_preferences",
        ARRAY(Enum(DataSharingPreference, name="data_sharing_preference")),
        default=[DataSharingPreference.ACCOUNT],
        nullable=False,
    )
    communication_preference: Communication | Column[Communication] = Column(
        "communication_preference",
        Enum(Communication, name="communication"),
        default=Communication.EMAIL,
        nullable=False,
    )
    location_tracking_enabled = Column(
        "location_tracking_enabled", Boolean, default=False, nullable=False
    )
    cookies_enabled = Column("cookies_enabled", Boolean, default=False, nullable=False)
    theme_preference: Theme | Column[Theme] = Column(
        "theme_preference",
        Enum(Theme, name="theme"),
        nullable=False,
        default=Theme.LIGHT,
    )
    created_date: datetime | Column[datetime] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date: datetime | Column[datetime] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    def __init__(self) -> None:
        """Settings Object Constructor."""

        self.id = uuid4()
        self.settings_id = uuid4()

    def __str__(self) -> str:
        """String Representation of the Settings Object."""

        return f"Settings Profile ID: {str(self.settings_id)}"

    def __repr__(self) -> str:
        """String Representation of the Settings Object."""

        return f"Application Model: {self.__class__.__name__}"
