"""Users Serialiser Module: Serialiser for User Profile Model."""

from datetime import date
from typing import Any, Union
from sqlalchemy import LargeBinary, String, cast, select
from sqlalchemy.orm import Session
from lib.interfaces.exceptions import (
    FernetError,
    UserProfileError,
)
from lib.utils.constants.users import (
    AccountCountry,
    AccountLanguage,
    AccountOccupation,
    Gender,
    ProfileInterest,
    Status,
    Regex,
    SocialMediaLink,
)
from models import ENGINE
from models.user.profiles import UserProfile


class UserProfileSerialiser(UserProfile):
    """
    Serialiser for the User Profile Model.

    Args:
        UserProfile (class): Access Point to the UserProfile Model.
    """

    @classmethod
    def get_user_profile(
        cls, profile_id: str
    ) -> Union[dict, UserProfileError, FernetError]:
        """CRUD Operation: Get User Profile.

        Args:
            profile_id (str): Public User Profile ID.

        Returns:
            str: User Profile Object.
        """
        with Session(ENGINE) as session:
            query = select(UserProfile).filter(
                cast(cls.profile_id, String) == profile_id
            )
            user_profile = session.execute(query).scalar_one_or_none()

            if not user_profile:
                raise UserProfileError("No User Profile Found.")

            return cls.__get_user_profile_data__(user_profile)

    @classmethod
    def create_user_profile(cls, **kwargs) -> Union[str, UserProfileError]:
        """CRUD Operation: Add User Profile.

        Args:
            name (str): User Profile Name.
            description (str): User Profile Description.
            card_id (str): User Profile's Card ID.

        Returns:
            dict: User Profile Object.
        """
        with Session(ENGINE) as session:
            user_profile: Union[UserProfile, UserProfileError] = cls()

            for key, value in kwargs.items():
                user_profile = cls.__set_profile__(user_profile, key, value)

            if not user_profile:
                raise UserProfileError("User Profile not created.")

            profile_id = str(user_profile)
            session.add(user_profile)
            session.commit()

            return profile_id

    @classmethod
    def update_user_profile(
        cls, private_id: str, **kwargs
    ) -> Union[str, UserProfileError]:
        """CRUD Operation: Update User Profile.

        Args:
            id (str): Private User Profile ID.

        Returns:
            str: User Profile Object.
        """
        with Session(ENGINE) as session:
            user_profile: Union[UserProfile, UserProfileError, None] = session.get(
                cls, private_id
            )

            if user_profile is None:
                raise UserProfileError("User Profile Not Found.")

            for key, value in kwargs.items():
                user_profile = cls.__set_profile__(user_profile, key, value)

            profile_id = str(user_profile)
            session.add(user_profile)
            session.commit()

            return profile_id

    @classmethod
    def delete_user_profile(cls, private_id: str) -> str:
        """CRUD Operation: Delete User Profile.

        Args:
            id (str): Private User Profile ID.

        Returns:
            str: User Profile Object.
        """
        with Session(ENGINE) as session:
            user_profile = session.get(UserProfile, private_id)

            if not user_profile:
                raise UserProfileError("User Profile Not Found")

            session.delete(user_profile)
            session.commit()

            return f"Deleted: {private_id}"

    @classmethod
    def __get_user_profile_data__(cls, user_profile: UserProfile):
        cls.__validate_user_profile__(user_profile)
        return {
            "id": user_profile.id,
            "profile_id": user_profile.profile_id,
            "first_name": user_profile.first_name,
            "last_name": user_profile.last_name,
            "username": user_profile.username,
            "date_of_birth": user_profile.date_of_birth,
            "gender": user_profile.gender,
            "profile_picture": user_profile.profile_picture,
            "mobile_number": user_profile.mobile_number,
            "country": user_profile.country,
            "language": user_profile.language,
            "biography": user_profile.biography,
            "occupation": user_profile.occupation,
            "interests": user_profile.interests,
            "social_media_links": user_profile.social_media_links,
            "created_date": user_profile.created_date,
        }

    @classmethod
    def __set_profile__(
        cls, user_profile: Union[UserProfile, UserProfileError], key: str, value: Any
    ) -> Union[UserProfile, UserProfileError]:
        if key not in [
            "first_name",
            "last_name",
            "username",
            "date_of_birth",
            "gender",
            "profile_picture",
            "mobile_number",
            "country",
            "language",
            "biography",
            "occupation",
            "interests",
            "social_media_links",
            "created_date",
            "profile_status",
        ]:
            raise UserProfileError("Invalid User Profile.")
        match key:
            case "first_name":
                cls.__validate_first_name(value)
                setattr(user_profile, key, value)
            case "last_name":
                cls.__validate_last_name(value)
                setattr(user_profile, key, value)
            case "username":
                cls.__validate_username(value)
                setattr(user_profile, key, value)
            case "date_of_birth":
                cls.__validate_date_of_birth(value)
                setattr(user_profile, key, value)
            case "gender":
                cls.__validate_primitive_type__(value, Gender)
                setattr(user_profile, key, value)
            case "profile_picture":
                cls.__validate_primitive_type__(value, LargeBinary)
                setattr(user_profile, key, value)
            case "mobile_number":
                cls.__validate_mobile_number(value)
                setattr(user_profile, key, value)
            case "country":
                cls.__validate_primitive_type__(value, AccountCountry)
                setattr(user_profile, key, value)
            case "language":
                cls.__validate_primitive_type__(value, AccountLanguage)
                setattr(user_profile, key, value)
            case "biography":
                cls.__validate_biography(value)
                setattr(user_profile, key, value)
            case "occupation":
                cls.__validate_primitive_type__(value, AccountOccupation)
                setattr(user_profile, key, value)
            case "profile_status":
                cls.__validate_primitive_type__(value, Status)
                setattr(user_profile, key, value)
            case "interests":
                cls.__validate_interests(value)
                # cls.interests.extend()
                temp = set(cls.interests)
                cls.interests = list(temp)
            case "social_media_links":
                cls.__validate_social_media_links(value)
                setattr(user_profile, key, value)

        return user_profile

    @staticmethod
    def __validate_first_name(value: str) -> UserProfileError:
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

    @staticmethod
    def __validate_last_name(value: str) -> UserProfileError:
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

    @staticmethod
    def __validate_username(value: str) -> UserProfileError:
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

    @staticmethod
    def __validate_date_of_birth(value: date):
        """Validates the value and sets the Private Attribute.

        Args:
            value (date): Valid Date of Birth value.

        Raises:
            UserProfileError: Valid Date.
        """
        if not isinstance(value, date):
            raise UserProfileError("Invalid Type for this Attribute.")

    @staticmethod
    def __validate_mobile_number(value: str) -> UserProfileError:
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

    @staticmethod
    def __validate_biography(value: str) -> UserProfileError:
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

    @staticmethod
    def __validate_interests(value: list[ProfileInterest]) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (list[str]): Valid Interests value.

        Raises:
            UserProfileError: List of Valid Interests.
        """
        if not isinstance(value, list):
            raise UserProfileError("Invalid Type for this Attribute.")
        temp = [isinstance(_, ProfileInterest) for _ in value]
        if not all(temp):
            raise UserProfileError("Invalid List of Interests.")

    @staticmethod
    def __validate_social_media_links(value: dict) -> UserProfileError:
        """Validates the value and sets the Private Attribute.

        Args:
            value (dict): Dictionary of allowable Social Media Links.

        Raises:
            UserSocialMediaLinkError: Value must be a Key-Value Pair.
        """
        if not isinstance(value, dict):
            raise UserProfileError("Invalid Social Media.")
        response = {}
        for key in value:
            if key in SocialMediaLink and key.value.match(value[key]):
                response[key.name] = value[key]
        # social_media_links =
        # social_media_links.update(response)(social_media_links)

    @staticmethod
    def __validate_user_profile__(
        user_profile: UserProfile,
    ) -> UserProfileError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Settings Profile Data.

        Raises:
            UserProfileError: Invalid Settings Profile Data.
        """
        for key in [
            user_profile.first_name,
            user_profile.last_name,
            user_profile.username,
            user_profile.profile_status,
        ]:
            if key is None:
                raise UserProfileError("Invalid Settings Profile Data.")

    @staticmethod
    def __validate_primitive_type__(value: Any, primitive: type) -> UserProfileError:
        if not isinstance(value, primitive):
            raise UserProfileError("Invalid Type for this Attribute.")
