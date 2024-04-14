"""Validators Module: validations for User related Models."""

from datetime import date, datetime, timedelta
from typing import Any, Union
from lib.interfaces.exceptions import SettingsProfileError, UserError, UserProfileError
from lib.utils.constants.users import (
    DataSharingPreference,
    Interest,
    ProfileVisibility,
    Regex,
    SocialMediaLink,
    Status,
)
from models.user.profiles import UserProfile


def validate_email(email: str) -> Union[str, UserError]:
    """Validates an Email.

    Args:
        email (str): Valid Email.

    Raises:
        UserError: Invalid Email.
    """
    if not isinstance(email, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.EMAIL.value.match(email):
        raise UserError("Invalid Email.")
    return email


def validate_password(password: str) -> Union[str, UserError]:
    """Validates the Password.

    Args:
        value (str): Valid Password.

    Raises:
        UserError: Invalid Password.
    """
    if not isinstance(password, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.PASSWORD.value.match(password):
        raise UserError("Invalid Password.")
    return password


def validate_status(status: Union[Status, None]):
    """Validates the User Status.

    Args:
        status (str): Valid User Status.

    Raises:
        UserError: Invalid User Status.
    """
    if not isinstance(status, Status):
        raise UserError("Invalid Type for this Attribute.")
    if status not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
        raise UserError("Invalid User Status.")
    return status


def validate_data_sharing_preferences(data_sharing: list[DataSharingPreference]):
    """Validates the User Data Sharing.

    Args:
        data_sharing (str): Valid User Data Sharing Preference.

    Raises:
        SettingsProfileError: Invalid User Data Sharing Preference.
    """

    if not isinstance(data_sharing, list):
        raise SettingsProfileError("Invalid Type for this Attribute.")
    if not all(
        [
            isinstance(data_sharing_item, DataSharingPreference)
            for data_sharing_item in data_sharing
        ]
    ):
        raise SettingsProfileError("Invalid Data Sharing Preference.")
    return list(set(data_sharing))


def validate_profile_visibility_preference(profile_visibility: ProfileVisibility):
    """Validates the User Profile Visibilty.

    Args:
        profile_visibility (str): Valid User Profile Visibilty Preference.

    Raises:
        SettingsProfileError: Invalid User Profile Visibilty Preference.
    """

    if not isinstance(profile_visibility, ProfileVisibility):
        raise SettingsProfileError("Invalid Type for this Attribute.")
    if profile_visibility in [ProfileVisibility.ADMIN]:
        raise SettingsProfileError("Invalid Profile Visibility Preference.")
    return profile_visibility


def validate_first_name(first_name: str) -> Union[str, UserProfileError]:
    """Validates the value and sets the Private Attribute.

    Args:
        first_name (str): Valid First Name value.

    Raises:
        UserProfileError: String Value of No less than 8 characters. (Max: 30)
    """
    if not isinstance(first_name, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.FIRST_NAME.value.match(first_name):
        raise UserProfileError("Invalid First Name.")
    return first_name


def validate_last_name(last_name: str) -> Union[str, UserProfileError]:
    """Validates the value and sets the Private Attribute.

    Args:
        last_name (str): Valid Last Name value.

    Raises:
        UserProfileError: String Value of No less than 8 characters. (Max: 30)
    """
    if not isinstance(last_name, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.LAST_NAME.value.match(last_name):
        raise UserProfileError("Invalid Last Name.")
    return last_name


def validate_username(username: str) -> Union[str, UserProfileError]:
    """Validates the value and sets the Private Attribute.

    Args:
        username (str): Valid Username value.

    Raises:
        UserProfileError: String Value of No less than 8 characters. (Max: 30)
    """
    if not isinstance(username, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.USERNAME.value.match(username):
        raise UserProfileError("Invalid Username.")
    return username


def validate_date_of_birth(date_of_birth: date):
    """Validates the value and sets the Private Attribute.

    Args:
        date_of_birth (date): Valid Date of Birth value.

    Raises:
        UserProfileError: Valid Date.
    """
    if not isinstance(date_of_birth, date):
        raise UserProfileError("Invalid Type for this Attribute.")
    if date_of_birth > date.today().replace(year=date.today().year - 18):
        raise UserProfileError("invalid Date of Birth.")
    return date_of_birth


def validate_mobile_number(mobile_number: str) -> Union[str, UserProfileError]:
    """Validates the value and sets the Private Attribute.

    Args:
        mobile_number (str): Valid Mobile Number value.

    Raises:
        UserProfileError: Valid Mobile Number.
    """
    if not isinstance(mobile_number, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.MOBILE_NUMBER.value.match(mobile_number):
        raise UserProfileError("Invalid Mobile Number.")
    return mobile_number


def validate_biography(biography: str) -> Union[str, UserProfileError]:
    """Validates the value and sets the Private Attribute.

    Args:
        biography (str): Valid Biography value.

    Raises:
        UserProfileError: String Value of No less than 8 characters. (Max: 250)
    """
    if not isinstance(biography, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.BIOGRAPHY.value.match(biography):
        raise UserProfileError("Invalid Biography.")
    return biography


def validate_interests(
    profile_interests: list[Interest],
) -> Union[list[Interest], UserProfileError]:
    """Validates the value and sets the Private Attribute.

    Args:
        profile_interests (list[str]): Valid Interests value.

    Raises:
        UserProfileError: List of Valid Interests.
    """

    if not isinstance(profile_interests, list):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not all([isinstance(interest, Interest) for interest in profile_interests]):
        raise UserProfileError("Invalid List of Interests.")
    return list(set(profile_interests))


def validate_social_media_links(
    social_media_links: dict[SocialMediaLink, str]
) -> Union[dict[str, str], UserProfileError]:
    """Validates the value and sets the Private Attribute.

    Args:
        social_media_links (dict): Dictionary of allowable Social Media Links.

    Raises:
        UserSocialMediaLinkError: Value must be a Key-Value Pair.
    """
    if not isinstance(social_media_links, dict):
        raise UserProfileError("Invalid Social Media.")
    response: dict[str, str] = {}
    for key, value in social_media_links.items():
        if not isinstance(key, SocialMediaLink) and key.value.match(
            social_media_links[key]
        ):
            response[key.name] = value
    return response
