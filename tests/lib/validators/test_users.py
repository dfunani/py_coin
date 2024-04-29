from datetime import date

from pytest import raises
from lib.interfaces.exceptions import (
    CardValidationError,
    PaymentProfileError,
    SettingsProfileError,
    UserError,
    UserProfileError,
)
from lib.utils.constants.users import (
    CardType,
    DataSharingPreference,
    Interest,
    ProfileVisibility,
    SocialMediaLink,
    Status,
)
from lib.validators.users import (
    validate_email,
    validate_balance,
    validate_biography,
    validate_card_number,
    validate_card_type,
    validate_cvv_number,
    validate_data_sharing_preferences,
    validate_date_of_birth,
    validate_description,
    validate_first_name,
    validate_interests,
    validate_last_name,
    validate_mobile_number,
    validate_name,
    validate_password,
    validate_pin,
    validate_profile_visibility_preference,
    validate_social_media_links,
    validate_status,
    validate_username,
)


def test_validate_email_invalid():
    """Tests Validating Email."""

    with raises(UserError):
        validate_email("test#bad#email")


def test_validate_email():
    """Tests Validating Email."""

    assert validate_email("dfunani@test.com") == "dfunani@test.com"


def test_validate_password_invalid():
    """Tests Validating Password."""

    with raises(UserError):
        validate_password("password")


def test_validate_password():
    """Tests Validating Password."""

    assert validate_password("password@1234") == "password@1234"


def test_validate_status_invalid():
    """Tests Validating User Status."""

    with raises(UserError):
        validate_status(Status.DISABLED)


def test_validate_status_invalid_str():
    """Tests Validating User Status."""

    with raises(UserError):
        validate_status("Status.DISABLED")


def test_validate_status():
    """Tests Validating User Status."""

    assert validate_status(Status.DELETED) == Status.DELETED


def test_validate_data_sharing_preferences_invalid():
    """Tests Validating User Data Sharing."""

    with raises(SettingsProfileError):
        validate_data_sharing_preferences([1, 2])


def test_validate_data_sharing_preferences():
    """Tests Validating User Data Sharing."""

    assert validate_data_sharing_preferences(
        [DataSharingPreference.ACCOUNT, DataSharingPreference.TRANSACTIONS]
    )[0] in [DataSharingPreference.ACCOUNT, DataSharingPreference.TRANSACTIONS]


def test_validate_profile_visibility_preference_invalid():
    """Tests Validating Profile Visibility."""

    with raises(SettingsProfileError):
        validate_profile_visibility_preference(ProfileVisibility.ADMIN)


def test_validate_profile_visibility_preference():
    """Tests Validating Profile Visibility."""

    assert (
        validate_profile_visibility_preference(ProfileVisibility.PUBLIC)
        == ProfileVisibility.PUBLIC
    )


def test_validate_first_name_invalid():
    """Tests Validating First Name."""

    with raises(UserProfileError):
        validate_first_name("")


def test_validate_first_name():
    """Tests Validating First Name."""

    assert validate_first_name("firstname") == "firstname"


def test_validate_last_name_invalid():
    """Tests Validating Last Name."""

    with raises(UserProfileError):
        validate_last_name("1")


def test_validate_last_name():
    """Tests Validating Last Name."""

    assert validate_last_name("lastname") == "lastname"


def test_validate_username_invalid():
    """Tests Validating Username."""

    with raises(UserError):
        validate_username("1")


def test_validate_username():
    """Tests Validating Username."""

    assert validate_username("username@1234") == "username@1234"


def test_validate_date_of_birth_invalid():
    """Tests Validating Date Of Birth."""

    with raises(UserProfileError):
        validate_date_of_birth("1991-12-31")


def test_validate_date_of_birth():
    """Tests Validating Date Of Birth."""

    assert validate_date_of_birth(date(1991, 12, 31)) == date(1991, 12, 31)


def test_validate_mobile_number_invalid():
    """Tests Validating Mobile Number."""

    with raises(UserProfileError):
        validate_mobile_number("0685642078")


def test_validate_mobile_number():
    """Tests Validating Mobile Number."""

    assert validate_mobile_number("+27685642078") == "+27685642078"


def test_validate_biography_invalid():
    """Tests Validating Biography."""

    with raises(UserProfileError):
        validate_biography("1")


def test_validate_biography():
    """Tests Validating Biography."""

    assert (
        validate_biography("Longer Description That serves as atest Biography.")
        == "Longer Description That serves as atest Biography."
    )


def test_validate_interests_invalid():
    """Tests Validating Profile Interests."""

    with raises(UserProfileError):
        validate_interests(["1"])


def test_validate_interests():
    """Tests Validating Profile Interests."""

    assert validate_interests([Interest.ANIME, Interest.ANIMALS])[0] in [
        Interest.ANIMALS,
        Interest.ANIME,
    ]

def test_validate_social_media_links_invalid_dict_key():
    """Tests Validating Social Media Links."""

    with raises(UserProfileError):
        validate_social_media_links('{"git": "value"}')

def test_validate_social_media_links_invalid_dict():
    """Tests Validating Social Media Links."""

    assert validate_social_media_links({SocialMediaLink.GITHUB: "value"}) == {}

def test_validate_social_media_links():
    """Tests Validating Social Media Links."""

    assert validate_social_media_links(
        {SocialMediaLink.GITHUB: "https://github.com/dfunani"}
    ) == {SocialMediaLink.GITHUB.name: "https://github.com/dfunani"}


def test_validate_name_invalid():
    """Tests Validating Card Name."""

    with raises(UserError):
        validate_name("1")


def test_validate_name():
    """Tests Validating Card Name."""

    assert validate_name("username#@1") == "username#@1"


def test_validate_description_invalid():
    """Tests Validating Card Description."""

    with raises(UserError):
        validate_description("1")


def test_validate_description():
    """Tests Validating Card Description."""

    assert (
        validate_description("Description for the test Card.")
        == "Description for the test Card."
    )


def test_validate_balance_invalid():
    """Tests Validating Card Balance."""

    with raises(PaymentProfileError):
        validate_balance(-1.0)

def test_validate_balance_invalid_str():
    """Tests Validating Card Balance."""

    with raises(PaymentProfileError):
        validate_balance("-1.0")


def test_validate_balance():
    """Tests Validating Card Balance."""

    assert validate_balance(5.0) == 5.0


def test_validate_card_type_invalid():
    """Tests Validating Card Type."""

    with raises(CardValidationError):
        validate_card_type("CardType")


def test_validate_card_type():
    """Tests Validating Card Type."""

    assert validate_card_type(CardType.CHEQUE) == CardType.CHEQUE


def test_validate_card_number_invalid():
    """Tests Validating Card Number."""

    with raises(CardValidationError):
        validate_card_number("19911234")


def test_validate_card_number():
    """Tests Validating Card Number."""

    assert validate_card_number("1991123456789") == "1991123456789"


def test_validate_cvv_number_invalid():
    """Tests Validating CVV Number."""

    with raises(CardValidationError):
        validate_cvv_number("123456")


def test_validate_cvv_number():
    """Tests Validating CVV Number."""

    assert validate_cvv_number("123") == "123"


def test_validate_pin_invalid():
    """Tests Validating Card Pin."""

    with raises(CardValidationError):
        validate_pin(123456)


def test_validate_pin():
    """Tests Validating Card Pin."""

    assert validate_pin("123456") == "123456"
