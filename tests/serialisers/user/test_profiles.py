"""Serialisers Module: Testing User Profile Serialiser."""

from datetime import date
from re import compile as regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import UserError, UserProfileError
from lib.utils.constants.users import (
    Communication,
    Country,
    Gender,
    Interest,
    Language,
    Occupation,
    ProfileVisibility,
    SocialMediaLink,
    Status,
)
from models.user.accounts import Account
from models.user.profiles import UserProfile
from models.user.users import User
from serialisers.user.profiles import UserProfileSerialiser
from models import ENGINE
from tests.conftest import run_test_teardown, setup_test_commit
from tests.serialisers.user.conftest import clear_profile_ids


def test_userprofileserialiser_create(get_account, regex_account, regex_user_profile):
    """Testing UserProfile Serialiser: Create UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user_profile = UserProfileSerialiser().create_user_profile(get_account.id)
        user_profile_id = get_id_by_regex(regex_user_profile, str(user_profile))
        user_profile_data = (
            session.query(UserProfile)
            .filter(UserProfile.profile_id == user_profile_id)
            .one_or_none()
        )
        run_test_teardown(user_profile_data.id, UserProfile, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_create_kwargs(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Create UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user_profile = UserProfileSerialiser().create_user_profile(get_account.id)
        user_profile_id = get_id_by_regex(regex_user_profile, str(user_profile))
        user_profile_data = (
            session.query(UserProfile)
            .filter(UserProfile.profile_id == user_profile_id)
            .one_or_none()
        )
        assert user_profile_data.interests == []
        assert user_profile_data.social_media_links == {}
        run_test_teardown(user_profile_data.id, UserProfile, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_create_kwargs_invalid():
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises(UserProfileError):
        UserProfileSerialiser().create_user_profile(
            "account.i",
        )


def test_userprofileserialiser_get(
    get_account, regex_account, regex_user_profile, user_profile_keys
):
    """Testing UserProfile Serialiser: Get UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user_profile = UserProfileSerialiser().create_user_profile(get_account.id)
        user_profile_id = get_id_by_regex(regex_user_profile, str(user_profile))
        user_profile_data = UserProfileSerialiser().get_user_profile(user_profile_id)

        assert isinstance(user_profile_data, dict)
        for key in user_profile_data:
            assert key not in UserProfile.__EXCLUDE_ATTRIBUTES__

        assert user_profile_data.get("id") is not None
        run_test_teardown(user_profile_data.get("id"), UserProfile, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_get_kwargs_invalid():
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises(UserProfileError):
        UserProfileSerialiser().get_user_profile("account.id")


def test_userprofileserialiser_delete(get_account, regex_account, regex_user_profile):
    """Testing UserProfile Serialiser: Delete UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user_profile = UserProfileSerialiser().create_user_profile(get_account.id)
        user_profile_id = get_id_by_regex(regex_user_profile, str(user_profile))
        user_profile_data = UserProfileSerialiser().get_user_profile(user_profile_id)

        UserProfileSerialiser().delete_user_profile(user_profile_data.get("id"))

        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_delete_kwargs_invalid():
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises(UserProfileError):
        UserProfileSerialiser().delete_user_profile("account.id")


def test_userprofileserialiser_update_valid_firstname(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)
        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["first_name"] = "validfirstname"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_firstname_invalid(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(get_account.id)
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["first_name"] = "12 valid"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_valid_lasttname(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["last_name"] = "validlastname"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_lasttname_invalid(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["first_name"] = "12 valid"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_valid_username(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["username"] = "validusername_123-dave"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_username_invalid(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["username"] = "12short"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_valid_date_of_birth(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["date_of_birth"] = date(1991, 12, 31)

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_date_of_birth_invalid(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["date_of_birth"] = date.today()

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserProfileError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_date_of_birth_invalid_type(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["date_of_birth"] = "12short"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserProfileError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_valid_mobile(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["mobile_number"] = "+27685642078"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_mobile_invalid(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["mobile_number"] = "0685642078"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserProfileError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_mobile_invalid_type(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["mobile_number"] = 564

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserProfileError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_valid_biography(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["biography"] = (
            "The description of what we testing being the biograpgy."
        )

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_biograpgy_invalid(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["biography"] = "The."

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises(UserProfileError):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_enums(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["country"] = Country.AFGHANISTAN
        user_data["language"] = Language.AFRIKAANS
        user_data["occupation"] = Occupation.ACCOUNTANT
        user_data["status"] = Status.ACTIVE
        user_data["gender"] = Gender.FEMALE

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_enum_invalid_type(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["country"] = "Country.AFGHANISTAN"
        user_data["language"] = "Language.AFRIKAANS"
        user_data["occupation"] = "Occupation.ACCOUNTANT"
        user_data["status"] = "Status.DISABLED"
        user_data["gender"] = "Gender.FEMALE"

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises((UserProfileError, TypeError)):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_interests(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["interests"] = [Interest.ANIMALS]

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_interest_invalid_type(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["interests"] = Interest.ANIMALS
        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises((UserProfileError, TypeError)):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_socials(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["social_media_links"] = {
            SocialMediaLink.GITHUB: "https://github.com/mailhog/MailHog"
        }

        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_socials_invalid_type(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["social_media_links"] = {
            "SocialMediaLink.GITHUB": "https://github.com/mailhog/MailHog"
        }
        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises((AttributeError)):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_socials_invalid_type_value(
    get_account, regex_account, regex_user_profile
):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user = UserProfileSerialiser().create_user_profile(
            get_account.id,
        )
        user_id = get_id_by_regex(regex_user_profile, user)
        user_data = UserProfileSerialiser().get_user_profile(user_id)
        user_data["social_media_links"] = (
            '{"SocialMediaLink.GITHUB": "https://github.com/mailhog/MailHog"}'
        )
        user_private_id = user_data["id"]
        clear_profile_ids(user_data)

        with raises((UserProfileError)):
            UserProfileSerialiser().update_user_profile(user_private_id, **user_data)

        UserProfileSerialiser().delete_user_profile(user_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_userprofileserialiser_update_kwargs_invalid():
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises(UserProfileError):
        UserProfileSerialiser().update_user_profile(
            "account.id",
        )
