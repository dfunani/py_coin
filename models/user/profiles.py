"""Profile Module: Contains an User's Account"""

from datetime import date, datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import (
    ARRAY,
    JSON,
    Column,
    Date,
    DateTime,
    LargeBinary,
    String,
    text,
    Enum,
)
from lib.utils.constants.users import (
    AccountCountry,
    AccountLanguage,
    AccountOccupation,
    Gender,
    ProfileInterest,
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

    id = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        primary_key=True,
    )
    profile_id: Column[str] = Column(
        "profile_id", String(256), default=text(f"'{str(uuid4())}'")
    )
    # account_id: Column[str] = Column(
    #     "account_id", ForeignKey("accounts.account_id"), nullable=False
    # )
    first_name = Column("first_name", String(256), nullable=False)
    last_name = Column("last_name", String(256), nullable=False)
    username = Column("username", String(256), nullable=False)
    date_of_birth: Union[date, Column[date]] = Column(
        "date_of_birth", Date, nullable=True
    )
    gender: Column[str] = Column("gender", Enum(Gender, name="gender"), nullable=True)
    profile_picture = Column("profile_picture", LargeBinary, nullable=True)
    mobile_number = Column("mobile_number", String(256), nullable=True)
    country: Union[AccountCountry, Column[AccountCountry]] = Column(
        "country", Enum(AccountCountry, name="account_country"), nullable=True
    )
    language: Union[AccountLanguage, Column[AccountLanguage]] = Column(
        "language",
        Enum(AccountLanguage, name="account_language"),
        default=AccountLanguage.ENGLISH,
        nullable=True,
    )
    biography = Column(
        "biography",
        String(256),
        default="This user has not provided a bio yet.",
        nullable=False,
    )
    occupation: Union[AccountOccupation, Column[AccountOccupation]] = Column(
        "occupation",
        Enum(AccountOccupation, name="account_occupation"),
        default=AccountOccupation.OTHER,
        nullable=True,
    )
    interests: Union[list[ProfileInterest], Column[list[ProfileInterest]]] = Column(
        "interests", ARRAY(Enum(ProfileInterest, name="profile_interest")), default=[]
    )
    social_media_links = Column("social_media_links", JSON, default={}, nullable=True)
    profile_status: Union[Status, Column[Status]] = Column(
        "profile_status", Enum(Status, name="profile_status"), default=Status.NEW
    )
    created_date: Union[datetime, Column[datetime]] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP")
    )
    updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
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
