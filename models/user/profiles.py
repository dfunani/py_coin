"""Profiles: User Profile Model."""

from datetime import date, datetime
from uuid import uuid4, UUID as uuid
from sqlalchemy import (
    ARRAY,
    JSON,
    UUID,
    Column,
    Date,
    DateTime,
    ForeignKey,
    LargeBinary,
    String,
    text,
    Enum,
)
from lib.utils.constants.users import (
    Country,
    Language,
    Occupation,
    Gender,
    Interest,
    Status,
)
from models import Base
from models.model import BaseModel


class UserProfile(Base, BaseModel):
    """Model representing a User's Profile."""

    __tablename__ = "user_profiles"
    __table_args__ = ({"schema": "users"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id = Column(
        "id",
        UUID(as_uuid=True),
        default=text(f"'{str(uuid4())}'"),
        primary_key=True,
        nullable=False,
    )
    profile_id: uuid | Column[uuid] = Column(
        "profile_id",
        UUID(as_uuid=True),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
    )
    account_id: uuid | Column[uuid] = Column(
        "account_id",
        UUID(as_uuid=True),
        ForeignKey("users.accounts.id"),
        nullable=False,
    )
    first_name = Column("first_name", String(256), nullable=True)
    last_name = Column("last_name", String(256), nullable=True)
    username = Column("username", String(256), nullable=True)
    date_of_birth: date | Column[date] = Column("date_of_birth", Date, nullable=True)
    gender: str | Column[str] = Column(
        "gender", Enum(Gender, name="gender"), nullable=True
    )
    profile_picture = Column("profile_picture", LargeBinary, nullable=True)
    mobile_number = Column("mobile_number", String(256), nullable=True)
    country: Country | Column[Country] = Column(
        "country", Enum(Country, name="account_country"), nullable=True
    )
    language: Language | Column[Language] = Column(
        "language",
        Enum(Language, name="account_language"),
        default=Language.ENGLISH,
        nullable=True,
    )
    biography = Column(
        "biography",
        String(256),
        default="This user has not provided a bio yet.",
        nullable=True,
    )
    occupation: Occupation | Column[Occupation] = Column(
        "occupation",
        Enum(Occupation, name="account_occupation"),
        default=Occupation.OTHER,
        nullable=True,
    )
    interests: list[Interest] | Column[list[Interest]] = Column(
        "interests",
        ARRAY(Enum(Interest, name="profile_interest")),
        default=[],
        nullable=True,
    )
    social_media_links = Column("social_media_links", JSON, default={}, nullable=True)
    status: Status | Column[Status] = Column(
        "status",
        Enum(Status, name="profile_status"),
        default=Status.NEW,
        nullable=False,
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

    def __init__(self):
        """User Profile Constructor."""

        self.id = uuid4()
        self.profile_id = uuid4()

    def __str__(self) -> str:
        """String Representation of the User Profile Object."""

        return f"User Profile ID: {str(self.profile_id)}"

    def __repr__(self) -> str:
        """String Representation of the User Profile Object."""

        return f"Application Model: {self.__class__.__name__}"
