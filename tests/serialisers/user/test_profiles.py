"""Serialisers Module: Testing User Profile Serialiser."""

from datetime import date
import json
from re import compile as regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import UserProfileError
from lib.utils.constants.users import CardType, Communication, Gender, ProfileVisibility
from lib.utils.helpers.cards import decrypt_data
from models.user.profiles import UserProfile
from models.warehouse.cards import Card
from serialisers.user.profiles import UserProfileSerialiser
from models import ENGINE
from models.user.users import User
from serialisers.warehouse.cards import CardSerialiser
from tests.conftest import run_test_teardown


def test_userprofileserialiser_create():
    """Testing UserProfile Serialiser: Create UserProfile."""
    user_profile = (
        UserProfileSerialiser().create_user_profile(
            first_name="firstname",
            last_name="lastnaame",
            username="username_f1",
            date_of_birth=date(1991, 12, 31),
            gender=Gender.FEMALE,
        ),
    )
    assert user_profile is not None


def test_userprofileserialiser_create_kwargs():
    """Testing UserProfile Serialiser: Create UserProfile."""
    user_profile = UserProfileSerialiser().create_user_profile(
        first_name="firstname",
        last_name="lastnaame",
        username="username_f1",
        date_of_birth=date(1991, 12, 31),
        gender=Gender.FEMALE,
    )
    regex = regex_compile(r"^User Profile ID: (.*)$")
    regex_match = regex.match(user_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    profile_id = matches[0]
    with Session(ENGINE) as session:
        user_data = (
            session.query(UserProfile)
            .filter(UserProfile.profile_id == profile_id)
            .one_or_none()
        )
        assert user_data.gender == Gender.FEMALE
        assert user_profile is not None
        session.delete(user_data)
        session.commit()


def test_userprofileserialiser_get():
    """Testing UserProfile Serialiser: Get UserProfile."""
    user_profile = UserProfileSerialiser().create_user_profile(
        first_name="firstname",
        last_name="lastnaame",
        username="username_f1",
        date_of_birth=date(1991, 12, 31),
        gender=Gender.FEMALE,
    )
    regex = regex_compile(r"^User Profile ID: (.*)$")
    regex_match = regex.match(user_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    profile_id = matches[0]
    user_data = UserProfileSerialiser().get_user_profile(profile_id)
    assert user_data.get("first_name") == "firstname"
    assert user_data.get("id") is not None
    with Session(ENGINE) as session:
        user_data = (
            session.query(UserProfile)
            .filter(UserProfile.profile_id == profile_id)
            .one_or_none()
        )
        session.delete(user_data)
        session.commit()


def test_userprofileserialiser_delete():
    """Testing UserProfile Serialiser: Delete UserProfile."""
    user_profile = UserProfileSerialiser().create_user_profile(
        first_name="firstname",
        last_name="lastnaame",
        username="username_f1",
        date_of_birth=date(1991, 12, 31),
        gender=Gender.FEMALE,
    )
    regex = regex_compile(r"^User Profile ID: (.*)$")
    regex_match = regex.match(user_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    profile_id = matches[0]
    user_data = UserProfileSerialiser().get_user_profile(profile_id)
    user_data = UserProfileSerialiser().delete_user_profile(user_data.get("id"))


def test_userprofileserialiser_update_valid_balance():
    """Testing UserProfile Serialiser: Update UserProfile."""
    user_profile = UserProfileSerialiser().create_user_profile(
        first_name="firstname",
        last_name="lastnaame",
        username="username_f1",
        date_of_birth=date(1991, 12, 31),
        gender=Gender.FEMALE,
    )
    regex = regex_compile(r"^User Profile ID: (.*)$")
    regex_match = regex.match(user_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    profile_id = matches[0]
    user_data = UserProfileSerialiser().get_user_profile(profile_id)
    assert user_data.get("gender") == Gender.FEMALE
    user_data = UserProfileSerialiser().update_user_profile(
        user_data.get("id"), gender=Gender.MALE
    )
    user_data = UserProfileSerialiser().get_user_profile(profile_id)
    assert user_data.get("gender") == Gender.MALE
    user_data = UserProfileSerialiser().delete_user_profile(user_data.get("id"))


def test_userprofileserialiser_update_valid_name():
    """Testing UserProfile Serialiser: Update UserProfile."""
    user_profile = UserProfileSerialiser().create_user_profile(
        first_name="firstname",
        last_name="lastnaame",
        username="username_f1",
        date_of_birth=date(1991, 12, 31),
        gender=Gender.FEMALE,
    )
    regex = regex_compile(r"^User Profile ID: (.*)$")
    regex_match = regex.match(user_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    profile_id = matches[0]
    user_data = UserProfileSerialiser().get_user_profile(profile_id)
    assert user_data.get("gender") == Gender.FEMALE
    with raises(UserProfileError):
        UserProfileSerialiser().update_user_profile(
            user_data.get("id"),
            profile_visibility_preference=ProfileVisibility.PRIVATE,
            communication_preference=Communication.SLACK,
            name="name",
        )


def test_userprofileserialiser_create_inavild_name():
    """Testing UserProfile Serialiser: Create UserProfile Invalid [Name]."""
    user_profile = UserProfileSerialiser().create_user_profile(
        first_name="firstname",
        last_name="lastnaame",
        username="username_f1",
        date_of_birth=date(1991, 12, 31),
        gender=Gender.FEMALE,
    )
    regex = regex_compile(r"^User Profile ID: (.*)$")
    regex_match = regex.match(user_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    profile_id = matches[0]
    user_data = UserProfileSerialiser().get_user_profile(profile_id)
    assert user_data.get("gender") == Gender.FEMALE
    with raises(UserProfileError):
        UserProfileSerialiser().update_user_profile(
            user_data.get("id"),
            profile_visibility_preference=ProfileVisibility.ADMIN,
            communication_preference="SLACK",
        )


def test_userprofileserialiser_get_inavild_private_id():
    """Testing UserProfile Serialiser: Create UserProfile Invalid [Card ID]."""
    with raises(UserProfileError):
        assert UserProfileSerialiser().get_user_profile("id")


def test_userprofileserialiser_delete_inavild_private_id():
    """Testing UserProfile Serialiser: Create UserProfile Invalid [Card ID]."""
    with raises(UserProfileError):
        assert UserProfileSerialiser().delete_user_profile("id")


def test_userprofileserialiser_update_inavild_kwargs():
    """Testing UserProfile Serialiser: Create UserProfile Invalid [Card ID]."""
    with raises(UserProfileError):
        assert UserProfileSerialiser().delete_user_profile("id")
