"""Testing Application constants"""

import sys
from lib.utils.constants.users import Regex
from lib.utils.constants.users import (
    Gender,
    AccountRole,
    AccountStatus,
    EmailVerification,
    UserDevicePermission,
    AccountLoginMethod,
    AccountCommunication,
    AccountOccupation,
    AccountCountry,
    AccountLanguage,
)

print(sys.path)
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



def test_gender_enum(genders: list[str]):
    """Testing Genders Enum

    Args:
        genders (list): list of genders that should always be present.
    """
    for gender in Gender:
        assert gender.value[0] in genders[0]
        assert gender.value[1] in genders[1]


def test_account_status_enum(statuses: list[str]):
    """Testing AccountStatus Enum

    Args:
        account_statuses (list): list of account statuses that should
        always be present.
    """
    for status in AccountStatus:
        assert status.value in statuses


def test_account_role_enum(roles: list[str]):
    """Testing Roles Enum

    Args:
        roles (list): list of roles that should always be present.
    """
    for role in AccountRole:
        assert role.value in roles


def test_email_verification_status(email_status: list[str]):
    """Testing Email Status Enum

    Args:
        email_status (list): list of Email Status that should always
        be present.
    """
    for status in EmailVerification:
        assert status.value in email_status


def device_permissions(permissions: list[str]):
    """Testing Device Permissions Enum

    Args:
        permissions (list): list of User Device Permissions that
        should always be present.
    """
    for status in UserDevicePermission:
        assert status.value in permissions


def account_login_method(login_methods: list[str]):
    """Testing Login Methods Enum

    Args:
        login_methods (list): list of Account Login Method that
        should always be present.
    """
    for status in AccountLoginMethod:
        assert status.value in login_methods


def account_communication(communications: list[str]):
    """Testing User Communication Preferences Enum

    Args:
        communications (list): list of Account Communication
        Prefereces that should always be present.
    """
    for status in AccountCommunication:
        assert status.value in communications


def account_occupations(occupations: list[str]):
    """Testing User Occupations Preferences Enum

    Args:
        occupations (list): list of Account Communication Prefereces
        that should always be present.
    """
    for status in AccountOccupation:
        assert status.value in occupations


def test_countries_enum():
    """Testing User Country Preferences Enum"""
    for country in AccountCountry:
        assert isinstance(country.value, tuple) and len(country.value[1]) == 2


def test_languages_enum():
    """Testing User Language Preferences Enum"""
    for country in AccountLanguage:
        assert isinstance(country.value, tuple)
