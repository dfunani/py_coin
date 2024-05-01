"""Serialisers Module: Testing User Profile Serialiser."""

from base64 import b64encode
from datetime import date
from re import compile as regex_compile

from pytest import raises
from sqlalchemy import cast, String
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
from tests.conftest import get_id_by_regex, run_test_teardown


def test_userprofileserialiser_create(account):
    """Testing UserProfile Serialiser: Create UserProfile."""

    with Session(ENGINE) as session:
        user_profile = UserProfileSerialiser().create_user_profile(account.id)
        user_profile_id = get_id_by_regex(user_profile)
        user_profile = (
            session.query(UserProfile)
            .filter(cast(UserProfile.profile_id, String) == user_profile_id)
            .one_or_none()
        )
        assert user_profile.id is not None
        run_test_teardown(user_profile.id, UserProfile, session)


def test_userprofileserialiser_create_kwargs_invalid():
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises(UserProfileError):
        UserProfileSerialiser().create_user_profile(
            "account.i",
        )


def test_userprofileserialiser_get(profile):
    """Testing UserProfile Serialiser: Get UserProfile."""

    user_profile_data = UserProfileSerialiser().get_user_profile(profile.profile_id)

    assert isinstance(user_profile_data, dict)
    for key in user_profile_data:
        assert key not in UserProfile.__EXCLUDE_ATTRIBUTES__


def test_userprofileserialiser_get_kwargs_invalid():
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises(UserProfileError):
        UserProfileSerialiser().get_user_profile("account.id")


def test_userprofileserialiser_delete(profile: UserProfile):
    """Testing UserProfile Serialiser: Delete UserProfile."""

    UserProfileSerialiser().delete_user_profile(profile.id)


def test_userprofileserialiser_delete_kwargs_invalid():
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises(UserProfileError):
        UserProfileSerialiser().delete_user_profile("account.id")


def test_userprofileserialiser_update_valid(profile):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with Session(ENGINE) as session:
        with open("tests/test_profile.png", "rb") as file:
            UserProfileSerialiser().update_user_profile(
                profile.id,
                first_name="validfirstname",
                last_name="validlastname",
                username="validusername_123-dave",
                date_of_birth=date(1991, 12, 31),
                mobile_number="+27685642078",
                biography="Longer Description for a Biography for testing.",
                country=Country.AFGHANISTAN,
                language=Language.AFRIKAANS,
                occupation=Occupation.ACCOUNTANT,
                status=Status.ACTIVE,
                gender=Gender.FEMALE,
                interests=[Interest.ANIMALS],
                social_media_links={
                    SocialMediaLink.GITHUB: "https://github.com/testing"
                },
                profile_picture=b64encode(file.read()),
            )
        profile = session.get(UserProfile, profile.id)

        assert profile.profile_id is not None
        assert profile.first_name == "validfirstname"
        assert profile.last_name == "validlastname"
        assert profile.username == "validusername_123-dave"
        assert profile.date_of_birth == date(1991, 12, 31)
        assert profile.mobile_number == "+27685642078"
        assert profile.biography == "Longer Description for a Biography for testing."
        assert profile.country == Country.AFGHANISTAN
        assert profile.language == Language.AFRIKAANS
        assert profile.occupation == Occupation.ACCOUNTANT
        assert profile.status == Status.ACTIVE
        assert profile.gender == Gender.FEMALE
        assert profile.interests == [Interest.ANIMALS]
        assert profile.social_media_links == {
            SocialMediaLink.GITHUB.name: "https://github.com/testing"
        }
        assert profile.profile_picture is not None


def test_userprofileserialiser_update_invalid(profile):
    """Testing UserProfile Serialiser: Update UserProfile."""

    with raises((UserProfileError, UserError)):
        UserProfileSerialiser().update_user_profile(
            profile.id,
            first_name="invalid",
            last_name="invalid",
            username="invalid",
            date_of_birth=date(2024, 1, 31),
            mobile_number="0685642078",
            biography="invalid",
            country="Country.AFGHANISTAN",
            language="Language.AFRIKAANS",
            occupation="Occupation.ACCOUNTANT",
            status="Status.ACTIVE",
            gender="Gender.FEMALE",
            interests=["Interest.ANIMALS"],
            social_media_links="invalid",
            profile_picture="None",
        )
        UserProfileSerialiser().update_user_profile(
            "profile.id",
            first_name=1,
            last_name=1,
            username=1,
            date_of_birth=1,
            mobile_number=1,
            biography=1,
            interests='["Interest.ANIMALS"]',
            social_media_links=1,
        )
