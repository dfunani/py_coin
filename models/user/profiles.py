"""Users Module: Contains User Profile Model for Mapping User's Profiles."""

from datetime import date, datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import (
    ARRAY,
    JSON,
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


class UserProfile(Base):
    """Model representing a User's Profile.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        profile_id (str): Unique Public Profile ID.
        account_id (str): Reference to the Associated Account.
        first_name (str): First Name of the Associated User.
        last_name (str): Last Name of the Associated User.
        username (str): Username of the Associated User.
        date_of_birth (date): Date of Birth of the Associated User.
        gender (gender): Gender of the Associated User.
        profile_picture (str): Profile Picture of the Associated User.
        mobile_number (str): Mobile Number of the Associated User.
        country (country): Country of the Associated User.
        language (language): Language of the Associated User.
        biography (str): Biography of the Associated User.
        occupation (occupation): Occupation of the Associated User.
        interests (list[interest]): Interests of the Associated User.
        social_media_links (dict): Social Media Links of the Associated User.
        created_date (str): Date the Asscoaited User was created.
        updated_date (str): Date the Asscoaited User was Last Updated.

    """

    __tablename__ = "user_profiles"
    __table_args__ = ({"schema": "users"},)

    id = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        primary_key=True,
        nullable=False,
    )
    profile_id: Union[str, Column[str]] = Column(
        "profile_id", String(256), default=text(f"'{str(uuid4())}'"), nullable=False
    )
    account_id: Union[str, Column[str]] = Column(
        "account_id", String(256), ForeignKey("users.accounts.id"), nullable=False
    )
    first_name = Column("first_name", String(256), nullable=False)
    last_name = Column("last_name", String(256), nullable=False)
    username = Column("username", String(256), nullable=False)
    date_of_birth: Union[date, Column[date]] = Column(
        "date_of_birth", Date, nullable=False
    )
    gender: Union[str, Column[str]] = Column("gender", Enum(Gender, name="gender"), nullable=False)
    profile_picture = Column("profile_picture", LargeBinary, nullable=True)
    mobile_number = Column("mobile_number", String(256), nullable=True)
    country: Union[Country, Column[Country]] = Column(
        "country", Enum(Country, name="account_country"), nullable=True
    )
    language: Union[Language, Column[Language]] = Column(
        "language",
        Enum(Language, name="account_language"),
        default=Language.ENGLISH,
        nullable=False,
    )
    biography = Column(
        "biography",
        String(256),
        default="This user has not provided a bio yet.",
        nullable=False,
    )
    occupation: Union[Occupation, Column[Occupation]] = Column(
        "occupation",
        Enum(Occupation, name="account_occupation"),
        default=Occupation.OTHER,
        nullable=False,
    )
    interests: Union[list[Interest], Column[list[Interest]]] = Column(
        "interests",
        ARRAY(Enum(Interest, name="profile_interest")),
        default=[],
        nullable=False,
    )
    social_media_links = Column("social_media_links", JSON, default={}, nullable=False)
    status: Union[Status, Column[Status]] = Column(
        "status",
        Enum(Status, name="profile_status"),
        default=Status.NEW,
        nullable=False,
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

    def __init__(self):
        """User Profile Constructor.

        Args:
            first_name (str): Profile's First Name.
            last Name (str): Profile's Last_name.
            username (str): Profile's Username.
            date_of_birth (str): Profile's Date of Birth.
            mobile_number (str): Profile's Mobile Number.
            biography (str): Profile's Biography.
            interests (list[str]): Profile's Interests.
            social_media_links (dict): Profile's Social Media Links.
        """
        self.id = str(uuid4())
        self.profile_id = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the User Profile Object.

        Returns:
            str: Representation of a User Profile Object.
        """
        return f"User Profile ID: {self.profile_id}"

    def __repr__(self) -> str:
        """String Representation of the User Profile Object.

        Returns:
            str: Representation of a User Profile Object.
        """
        return f"Application Model: {self.__class__.__name__}"
