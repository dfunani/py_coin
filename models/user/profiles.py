"""Profile Module: Contains an User's Account Profile Model for Mapping a Profile to an Account."""

from datetime import date, datetime
from json import dumps, loads
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
from lib.interfaces.exceptions import UserProfileError, UserSocialMediaLinkError
from lib.utils.constants.users import (
    AccountCountry,
    AccountLanguage,
    AccountOccupation,
    DateFormat,
    Gender,
    ProfileInterest,
    Regex,
    SocialMediaLink,
)
from models import Base


class Profile(Base):
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

    __tablename__ = "profiles"

    id = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        primary_key=True,
    )
    profile_id: Column[str] = Column(
        "profile_id", String(256), default=text(f"'{str(uuid4())}'")
    )
    account_id: Column[str] = Column(
        "account_id", ForeignKey("accounts.account_id"), nullable=False
    )
    __first_name = Column("first_name", String(256), nullable=False)
    __last_name = Column("last_name", String(256), nullable=False)
    __username = Column("username", String(256), nullable=False)
    __date_of_birth: Union[date, Column[date]] = Column(
        "date_of_birth", Date, nullable=False
    )
    gender: Column[str] = Column("gender", Enum(Gender), nullable=False)
    profile_picture = Column("profile_picture", LargeBinary, nullable=False)
    __mobile_number = Column("mobile_number", String(256), nullable=False)
    country: Union[AccountCountry, Column[AccountCountry]] = Column(
        "country", Enum(AccountCountry), nullable=False
    )
    language: Union[AccountLanguage, Column[AccountLanguage]] = Column(
        "language", Enum(AccountLanguage), default=AccountLanguage.ENGLISH
    )
    __biography = Column(
        "biography", String(256), default="This user has not provided a bio yet."
    )
    occupation = Column(
        "occupation", Enum(AccountOccupation), default=AccountOccupation.OTHER
    )
    __interests = Column("interests", ARRAY(String(256)), default=[])
    __social_media_links = Column("social_media_links", JSON, default={})
    __created_date: Union[datetime, Column[datetime]] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP")
    )
    __updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        date_of_birth: str,
        mobile_number: str,
        biography: str,
        interests: list[str],
        social_media_links: dict,
        **kwargs
    ):
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
        self.__set_first_name(first_name)
        self.__set_last_name(last_name)
        self.__set_username(username)
        self.__set_date_of_birth(date_of_birth)
        self.__set_mobile_number(mobile_number)
        self.__set_biography(biography)
        self.__set_interests(interests)
        self.__set_social_media_links(social_media_links)
        super().__init__(**kwargs)

    @property
    def first_name(self) -> str:
        """Getter for the First Name Property.

        Returns:
            str: Representation of the First Name.
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str) -> UserProfileError:
        """Setter for the First Name Property.

        Args:
            value (str): Valid First Name value.
        """
        self.__set_first_name(value)

    @property
    def last_name(self) -> str:
        """Getter for the Last Name Property.

        Returns:
            str: Representation of the Last Name.
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str) -> UserProfileError:
        """Setter for the Last Name Property.

        Args:
            value (str): Valid Last Name value.
        """
        self.__set_last_name(value)

    @property
    def username(self) -> str:
        """Getter for the Username Property.

        Returns:
            str: Representation of the Username.
        """
        return self.__username

    @last_name.setter
    def username(self, value: str) -> UserProfileError:
        """Setter for the Username Property.

        Args:
            value (str): Valid Username value.
        """
        self.__set_username(value)

    @property
    def date_of_birth(self) -> str:
        """Getter for the Date of Birth Property.

        Returns:
            str: Representation of the Date of Birth.
        """
        return self.__date_of_birth.strftime(DateFormat.LONG)

    @date_of_birth.setter
    def date_of_birth(self, value: date) -> UserProfileError:
        """Setter for the Date of Birth Property.

        Args:
            value (str): Valid Date of Birth value.
        """
        self.__set_date_of_birth(value)

    @property
    def mobile_number(self) -> str:
        """Getter for the Mobile Number Property.

        Returns:
            str: Representation of the Mobile Number.
        """
        return self.__mobile_number

    @mobile_number.setter
    def mobile_number(self, value: str) -> UserProfileError:
        """Setter for the Mobile Number Property.

        Args:
            value (str): Valid Mobile Number value.
        """
        self.__set_mobile_number(value)

    @property
    def biography(self) -> str:
        """Getter for the Biography Property.

        Returns:
            str: Representation of the Biography.
        """
        return self.__biography

    @biography.setter
    def biography(self, value: str) -> str:
        """Setter for the Biography Property.

        Args:
            value (str): Valid Biography value.
        """
        self.__set_biography(value)

    @property
    def interests(self) -> list[str]:
        """Getter for the Interests Property.

        Returns:
            str: Representation of the Interests.
        """
        return self.__interests

    @interests.setter
    def interests(self, value: list[str]) -> UserProfileError:
        """Setter for the Interests Property.

        Returns:
            list[str]: Representation of the Interests.
        """
        self.__set_interests(value)

    @property
    def social_media_links(self) -> dict:
        """Getter for the Social Media Links Property.

        Returns:
            dict: Social Media Links as a Key-Value Pair.
        """
        return loads(self.__social_media_links)

    @social_media_links.setter
    def social_media_links(self, value: dict) -> ValueError:
        """Setter for the Social Media Links Property.

        Args:
            value (dict): Dictionary of Valid Social Media Links.

        Raises:
            ValueError: Value must be a Key-Value Pair.
        """
        self.__set_social_media_links(value)

    @property
    def created_date(self) -> str:
        """Getter for The Last Updated Date Property.

        Returns:
            str: Representation of the Created Date.
        """
        return self.__created_date.strftime(DateFormat.SLASH)

    @property
    def updated_date(self) -> str:
        """Getter for The Created Date Property.

        Returns:
            str: Representation of the Updated Date.
        """
        return self.__updated_date.strftime(DateFormat.SLASH)

    def __set_first_name(self, value: str) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid First Name value.

        Raises:
            UserProfileError: String Value of No less than 8 characters. (Max: 30)
        """
        if not isinstance(value, str):
            raise UserProfileError("Invalid Type for this Attribute.")
        if not Regex.FIRST_NAME.value.match(value):
            raise UserProfileError("Invalid First Name.")
        self.__first_name = value

    def __set_last_name(self, value: str) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Last Name value.

        Raises:
            UserProfileError: String Value of No less than 8 characters. (Max: 30)
        """
        if not isinstance(value, str):
            raise UserProfileError("Invalid Type for this Attribute.")
        if not Regex.LAST_NAME.value.match(value):
            raise UserProfileError("Invalid Last Name.")
        self.__last_name = value

    def __set_username(self, value: str) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Username value.

        Raises:
            UserProfileError: String Value of No less than 8 characters. (Max: 30)
        """
        if not isinstance(value, str):
            raise UserProfileError("Invalid Type for this Attribute.")
        if not Regex.USERNAME.value.match(value):
            raise UserProfileError("Invalid Username.")
        self.__username = value

    def __set_date_of_birth(self, value: date):
        """Validates the value and sets the Private Attribute.

        Args:
            value (date): Valid Date of Birth value.

        Raises:
            UserProfileError: Valid Date.
        """
        if not isinstance(value, date):
            raise UserProfileError("Invalid Type for this Attribute.")
        self.__date_of_birth = value

    def __set_mobile_number(self, value: str) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Mobile Number value.

        Raises:
            UserProfileError: Valid Mobile Number.
        """
        if not isinstance(value, str):
            raise UserProfileError("Invalid Type for this Attribute.")
        if not Regex.MOBILE_NUMBER.value.match(value):
            raise UserProfileError("Invalid Mobile Number.")
        self.__mobile_number = value

    def __set_biography(self, value: str) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (str): Valid Biography value.

        Raises:
            UserProfileError: String Value of No less than 8 characters. (Max: 250)
        """
        if not isinstance(value, str):
            raise UserProfileError("Invalid Type for this Attribute.")
        if not Regex.BIOGRAPHY.value.match(value):
            raise UserProfileError("Invalid Biography.")
        self.__biography = value

    def __set_interests(self, value: list[str]) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (list[str]): Valid Interests value.

        Raises:
            UserProfileError: List of Valid Interests.
        """
        interests = []
        if not isinstance(value, list):
            raise UserProfileError("Invalid Type for this Attribute.")
        for interest in value:
            if list(filter(lambda i: interest == i.value, ProfileInterest)):
                interests.append(interest)
        self.__interests = list(set(list(self.__interests or []) + interests))

    def __set_social_media_links(self, value: dict) -> UserSocialMediaLinkError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (dict): Dictionary of allowable Social Media Links.

        Raises:
            UserSocialMediaLinkError: Value must be a Key-Value Pair.
        """
        if not isinstance(value, dict):
            raise UserSocialMediaLinkError("Invalid Social Media.")
        response = {}
        for key in value:
            if key in SocialMediaLink and key.value.match(value[key]):
                response[key.name] = value[key]
        social_media_links = loads(self.__social_media_links or '{}')
        social_media_links.update(response)
        self.__social_media_links = dumps(social_media_links)
