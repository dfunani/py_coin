"""Types: Data-Classes for Custom Typed Dictionaries."""

from typing import Optional, TypedDict

from sqlalchemy import DateTime
from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.transactions import TransactionStatus
from lib.utils.constants.users import (
    Communication,
    Country,
    DataSharingPreference,
    Gender,
    Interest,
    Language,
    LoginMethod,
    Occupation,
    ProfileVisibility,
    SocialMediaLink,
    Status,
    Theme,
    Verification,
)


class AccountDict(TypedDict):
    """Typed Account Dictionary."""

    status: Optional[Status]


class ProfileDict(TypedDict):
    """Typed Profile Dictionary."""

    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    date_of_birth: Optional[DateTime]
    gender: Optional[Gender]
    profile_picture: Optional[str]
    mobile_number: Optional[str]
    country: Optional[Country]
    language: Optional[Language]
    biography: Optional[str]
    occupation: Optional[Occupation]
    interests: Optional[Interest]
    social_media_links: Optional[SocialMediaLink]
    status: Optional[Status]


class SettingsDict(TypedDict):
    """Typed Settings Dictionary."""

    mfa_enabled: Optional[str]
    location_tracking_enabled: Optional[bool]
    cookies_enabled: Optional[bool]
    email_status: Optional[Verification]
    data_sharing_preferences: Optional[DataSharingPreference]
    communication_preference: Optional[Communication]
    theme_preference: Optional[Theme]
    profile_visibility_preference: Optional[ProfileVisibility]
    mfa_last_used_date: Optional[DateTime]
    communication_status: Optional[Verification]


class UserDict(TypedDict):
    """Typed User-Account Dictionary."""

    email: Optional[str]
    password: Optional[str]
    login_location: Optional[Country]
    login_device: Optional[str]
    login_method: Optional[LoginMethod]


class DataDict(TypedDict):
    """Generic Typed Data Dictionary."""

    title: Optional[str]
    description: Optional[str]


class TransactionDict(DataDict):
    """Typed Dictionary for Transaction Data."""

    amount: Optional[float]
    transaction_status: Optional[TransactionStatus]


class ContractDict(DataDict):
    """Typed Dictionary for Contract Data."""

    contract: Optional[str]
    contract_status: Optional[ContractStatus]
