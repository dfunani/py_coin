"""Interfaces: Custom User Data Structures."""

from lib.decorators.utils import validate_function_signature
from lib.interfaces.abstract import AbstractType
from lib.interfaces.types import UserDict, AccountDict, ProfileDict, SettingsDict


class __AccountData__(AbstractType):
    """Type Check for Account Related Data."""

    @validate_function_signature(True)
    def __init__(self, data: AccountDict) -> None:
        self.status = data.get("status")


class __ProfileData__(AbstractType):
    """Type Check for Profile Related Data."""

    @validate_function_signature(True)
    def __init__(self, data: ProfileDict) -> None:
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.username = data.get("username")
        self.date_of_birth = data.get("date_of_birth")
        self.gender = data.get("gender")
        self.profile_picture = data.get("profile_picture")
        self.mobile_number = data.get("mobile_number")
        self.country = data.get("country")
        self.language = data.get("language")
        self.biography = data.get("biography")
        self.occupation = data.get("occupation")
        self.interests = data.get("interests")
        self.social_media_links = data.get("social_media_links")
        self.status = data.get("status")


class __SettingsData__(AbstractType):
    """Type Check for Settings Related Data."""

    @validate_function_signature(True)
    def __init__(self, data: SettingsDict) -> None:
        self.mfa_enabled = data.get("mfa_enabled")
        self.location_tracking_enabled = data.get("location_tracking_enabled")
        self.cookies_enabled = data.get("cookies_enabled")
        self.email_status = data.get("email_status")
        self.data_sharing_preferences = data.get("data_sharing_preferences")
        self.communication_preference = data.get("communication_preference")
        self.theme_preference = data.get("theme_preference")
        self.profile_visibility_preference = data.get("profile_visibility_preference")
        self.mfa_last_used_date = data.get("mfa_last_used_date")
        self.communication_status = data.get("communication_status")


class __LoginData__(AbstractType):
    """Type Check for Login Meta Data."""

    @validate_function_signature(True)
    def __init__(self, data: UserDict):
        self.email = data.get("email")
        self.password = data.get("password")
        self.login_location = data.get("login_location")
        self.login_device = data.get("login_device")
        self.login_method = data.get("login_method")


class UserData(AbstractType):
    """Type Check for User Related Data."""

    @validate_function_signature(True)
    def __init__(
        self,
        account: AccountDict = None,
        profile: ProfileDict = None,
        settings: SettingsDict = None,
        login: UserDict = None,
    ) -> None:
        if account:
            self.account = __AccountData__(account)
        if profile:
            self.profile = __ProfileData__(profile)
        if settings:
            self.settings = __SettingsData__(settings)
        if login:
            self.login = __LoginData__(login)
