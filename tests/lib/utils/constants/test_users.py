"""Testing Application constants"""

from lib.utils.constants.users import Regex, Role
from lib.utils.constants.users import (
    Gender,
    Status,
    Verification,
    DevicePermission,
    LoginMethod,
    Communication,
    Occupation,
    Country,
    Language,
)


def test_regex_constants_email_success():
    """Testing Email Regex Match - Valid Email"""

    assert Regex.EMAIL.value.match("dfunani@test.co.za") is not None


def test_regex_constants_email_error():
    """Testing Email Regex Match - Invalid Email"""

    assert Regex.EMAIL.value.match("dfunanitest.co.za") is None


def test_regex_constants_password_success():
    """Testing Password Regex Match - Valid Password"""

    assert Regex.PASSWORD.value.match("password123@test") is not None


def test_regex_constants_password_error():
    """Testing Password Regex Match - Invalid Password"""

    assert Regex.PASSWORD.value.match("password") is None


def test_gender_enum():
    """Testing Genders Enum"""

    assert Gender.FEMALE.value == ("female", "f")


def test_account_status_enum():
    """Testing Status Enum"""

    assert Status.ACTIVE.value == "Actively is in Use."


def test_account_role_enum():
    """Testing Roles Enum"""

    assert Role.USER.value == "Application User"


def test_email_verification_status():
    """Testing Email Status Enum"""

    assert Verification.VERIFIED.value == "Verified"


def device_permissions():
    """Testing Device Permissions Enum"""

    assert DevicePermission.CAMERA.value == "camera"


def account_login_method():
    """Testing Login Methods Enum"""

    assert LoginMethod.FACEBOOK.value == "Facebook SSO"


def account_communication():
    """Testing User Communication Preferences Enum"""

    assert Communication.EMAIL.value == "Email Messenger"


def account_occupations():
    """Testing User Occupations Preferences Enum"""

    assert Occupation.ARCHITECT.value == "Architect"


def test_countries_enum():
    """Testing User Country Preferences Enum"""

    assert Country.AFGHANISTAN.value == ("Afghanistan", "AF")


def test_languages_enum():
    """Testing User Language Preferences Enum"""

    assert Language.AFRIKAANS.value == ("Afrikaans", "af")
