"""User Serialiser Module: Serialiser for User Profile Model."""

from datetime import date
from typing import Union
from sqlalchemy import LargeBinary, String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from lib.interfaces.exceptions import (
    FernetError,
    UserProfileError,
)
from lib.utils.constants.users import (
    Country,
    Language,
    Occupation,
    Gender,
    Status,
)
from lib.validators.users import (
    validate_biography,
    validate_date_of_birth,
    validate_first_name,
    validate_interests,
    validate_last_name,
    validate_mobile_number,
    validate_social_media_links,
    validate_status,
    validate_username,
)
from models import ENGINE
from models.user.profiles import UserProfile


class UserProfileSerialiser(UserProfile):
    """
    Serialiser for the User Profile Model.

    Args:
        UserProfile (class): Access Point to the UserProfile Model.
    """

    __MUTABLE_ATTRIBUTES__ = {
        "first_name": (str, False, validate_first_name),
        "last_name": (str, False, validate_last_name),
        "username": (str, False, validate_username),
        "date_of_birth": (date, False, validate_date_of_birth),
        "gender": (Gender, False, None),
        "profile_picture": (LargeBinary, True, None),
        "mobile_number": (str, True, validate_mobile_number),
        "country": (Country, True, None),
        "language": (Language, False, None),
        "biography": (str, False, validate_biography),
        "occupation": (Occupation, False, None),
        "interests": (list, False, validate_interests),
        "social_media_links": (dict, False, validate_social_media_links),
        "status": (Status, False, validate_status),
    }

    def get_user_profile(
        self, profile_id: str
    ) -> Union[dict, UserProfileError, FernetError]:
        """CRUD Operation: Get User Profile.

        Args:
            profile_id (str): Public User Profile ID.

        Returns:
            str: User Profile Object.
        """
        with Session(ENGINE) as session:
            query = select(UserProfile).filter(
                cast(UserProfile.profile_id, String) == profile_id
            )
            user_profile = session.execute(query).scalar_one_or_none()

            if not user_profile:
                raise UserProfileError("No User Profile Found.")

            return self.__get_user_profile_data__(user_profile)

    def create_user_profile(
        self, account_id: str, **kwargs
    ) -> Union[str, UserProfileError]:
        """CRUD Operation: Add User Profile.

        Args:
            account_id (str): Unique Account ID.

        Returns:
            str: User Profile Object.
        """
        with Session(ENGINE) as session:
            self.account_id = account_id

            for key, value in kwargs.items():
                if key not in UserProfileSerialiser.__MUTABLE_ATTRIBUTES__:
                    raise UserProfileError("Invalid User Profile.")

                data_type, nullable, validator = (
                    UserProfileSerialiser.__MUTABLE_ATTRIBUTES__[key]
                )
                if not nullable and value is None:
                    raise UserProfileError("Invalid Type for this Attribute.")

                if not isinstance(value, data_type) and value is not None:
                    raise UserProfileError("Invalid Type for this Attribute.")

                if validator and value is not None and hasattr(validator, "__call__"):
                    value = validator(value)

                setattr(self, key, value)

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise UserProfileError("User Profile Not Created.") from exc

            return str(self)

    def update_user_profile(
        self, private_id: str, **kwargs
    ) -> Union[str, UserProfileError]:
        """CRUD Operation: Update User Profile.

        Args:
            id (str): Private User Profile ID.

        Returns:
            str: User Profile Object.
        """
        with Session(ENGINE) as session:
            user_profile: Union[UserProfile, UserProfileError, None] = session.get(
                UserProfile, private_id
            )

            if user_profile is None:
                raise UserProfileError("User Profile Not Found.")

            for key, value in kwargs.items():
                if key not in UserProfileSerialiser.__MUTABLE_ATTRIBUTES__:
                    raise UserProfileError("Invalid User Profile.")

                data_type, nullable, validator = (
                    UserProfileSerialiser.__MUTABLE_ATTRIBUTES__[key]
                )
                if not nullable and value is None:
                    raise UserProfileError("Invalid Type for this Attribute.")

                if not isinstance(value, data_type) and value is not None:
                    raise UserProfileError("Invalid Type for this Attribute.")

                if validator and value is not None and hasattr(validator, "__call__"):
                    value = validator(value)

                setattr(user_profile, key, value)

            try:
                session.add(user_profile)
                session.commit()
            except IntegrityError as exc:
                raise UserProfileError("User Profile not Updated.") from exc

            return str(user_profile)

    def delete_user_profile(self, private_id: str) -> str:
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

    def __get_user_profile_data__(self, user_profile: UserProfile):
        return {
            "id": user_profile.id,
            "profile_id": user_profile.profile_id,
            "account_id": user_profile.account_id,
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
            "status": user_profile.status,
        }
