"""Constants: Testing User Constants Module."""

from pytest import mark
from lib.utils.constants.users import Regex, Role
from lib.utils.constants.users import (
    Gender,
    Status,
    Verification,
    DevicePermission,
    Communication,
    Occupation,
    Country,
    Language,
)


@mark.parametrize(
    "data",
    ["test@test.co.za", "name123@testing.com", "testing1223@testing.co.org"],
)
def test_regex_constants_email_success(data):
    """Testing Email Regex Match - Valid Email"""

    assert Regex.EMAIL.value.match(data) is not None


@mark.parametrize(
    "data",
    [
        "test#test.co.za",
        "name123@testing.",
        "name123-testing.co.com-org",
        "testing1223@testing.c",
        "testing1223@testing.comutil",
    ],
)
def test_regex_constants_email_error(data):
    """Testing Email Regex Match - Invalid Email"""

    assert Regex.EMAIL.value.match(data) is None


@mark.parametrize(
    "data",
    [
        "test123@password.co.za",
        "name123@passwording.com",
        "passwording1223@passwording.co.org",
    ],
)
def test_regex_constants_password_success(data):
    """Testing Password Regex Match - Valid Password"""

    assert Regex.PASSWORD.value.match(data) is not None


@mark.parametrize(
    "data",
    ["@test", "nametestingcom", "122312345678"],
)
def test_regex_constants_password_error(data):
    """Testing Password Regex Match - Invalid Password"""

    assert Regex.PASSWORD.value.match(data) is None


@mark.parametrize(
    "data",
    list(Gender),
)
def test_gender_enum(data):
    """Testing Genders Enum."""

    assert isinstance(data.value, tuple)
    assert len(data.value) == 2
    assert len(data.value[1]) == 1


@mark.parametrize(
    "data",
    list(Status),
)
def test_status_enum(data):
    """Testing Statuss Enum."""

    assert isinstance(data.value, str)


@mark.parametrize(
    "data",
    list(Role),
)
def test_role_enum(data):
    """Testing Roles Enum."""

    assert isinstance(data.value, str)


@mark.parametrize(
    "data",
    list(Verification),
)
def test_verification_enum(data):
    """Testing Verification Enum."""

    assert isinstance(data.value, str)


@mark.parametrize(
    "data",
    list(DevicePermission),
)
def test_devicepermission_enum(data):
    """Testing Device Permission Enum."""

    assert isinstance(data.value, str)


@mark.parametrize(
    "data",
    list(Communication),
)
def test_communication_enum(data):
    """Testing Communication Enum."""

    assert isinstance(data.value, str)


@mark.parametrize(
    "data",
    list(Occupation),
)
def test_occupation_enum(data):
    """Testing Occupation Enum."""

    assert isinstance(data.value, str)


@mark.parametrize(
    "data",
    list(Country),
)
def test_country_enum(data):
    """Testing Country Enum."""

    assert isinstance(data.value, tuple)
    assert len(data.value) == 2
    assert len(data.value[1]) == 2


@mark.parametrize(
    "data",
    list(Language),
)
def test_language_enum(data):
    """Testing Language Enum."""

    assert isinstance(data.value, tuple)
    assert len(data.value) == 2
    assert len(data.value[1]) >= 2
