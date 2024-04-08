"""Serialisers Module: Testing Payments Serialiser."""

import json
from re import compile as regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import SettingsProfileError
from lib.utils.constants.users import CardType, Communication, ProfileVisibility
from lib.utils.helpers.cards import decrypt_data
from models.user.settings import SettingsProfile
from models.warehouse.cards import Card
from serialisers.user.settings import SettingsProfileSerialiser
from models import ENGINE
from models.user.users import User
from serialisers.warehouse.cards import CardSerialiser
from tests.conftest import run_test_teardown


def test_settingsprofileserialiser_create():
    """Testing SettingsProfile Serialiser: Create SettingsProfile."""
    settings_profile = SettingsProfileSerialiser().create_settings_profile()
    assert settings_profile is not None


def test_settingsprofileserialiser_create_kwargs():
    """Testing SettingsProfile Serialiser: Create SettingsProfile."""
    settings_profile = SettingsProfileSerialiser().create_settings_profile(
        profile_visibility_preference=ProfileVisibility.PRIVATE
    )
    regex = regex_compile(r"^Settings Profile ID: (.*)$")
    regex_match = regex.match(settings_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    settings_id = matches[0]
    with Session(ENGINE) as session:
        settings_data = (
            session.query(SettingsProfile)
            .filter(SettingsProfile.settings_id == settings_id)
            .one_or_none()
        )
        assert settings_data.profile_visibility_preference == ProfileVisibility.PRIVATE
        assert settings_profile is not None
        session.delete(settings_data)
        session.commit()


def test_settingsprofileserialiser_get():
    """Testing SettingsProfile Serialiser: Get SettingsProfile."""
    settings_profile = SettingsProfileSerialiser().create_settings_profile()
    regex = regex_compile(r"^Settings Profile ID: (.*)$")
    regex_match = regex.match(settings_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    settings_id = matches[0]
    settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
    assert (
        settings_data.get("profile_visibility_preference") == ProfileVisibility.PUBLIC
    )
    assert settings_data.get("id") is not None
    with Session(ENGINE) as session:
        settings_data = (
            session.query(SettingsProfile)
            .filter(SettingsProfile.settings_id == settings_id)
            .one_or_none()
        )
        session.delete(settings_data)
        session.commit()


def test_settingsprofileserialiser_delete():
    """Testing SettingsProfile Serialiser: Delete SettingsProfile."""
    settings_profile = SettingsProfileSerialiser().create_settings_profile()
    regex = regex_compile(r"^Settings Profile ID: (.*)$")
    regex_match = regex.match(settings_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    settings_id = matches[0]
    settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
    assert (
        settings_data.get("profile_visibility_preference") == ProfileVisibility.PUBLIC
    )
    settings_data = SettingsProfileSerialiser().delete_settings_profile(
        settings_data.get("id")
    )


def test_settingsprofileserialiser_update_valid_balance(name, description):
    """Testing SettingsProfile Serialiser: Update SettingsProfile."""
    settings_profile = SettingsProfileSerialiser().create_settings_profile()
    regex = regex_compile(r"^Settings Profile ID: (.*)$")
    regex_match = regex.match(settings_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    settings_id = matches[0]
    settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
    assert (
        settings_data.get("profile_visibility_preference") == ProfileVisibility.PUBLIC
    )
    settings_data = SettingsProfileSerialiser().update_settings_profile(
        settings_data.get("id"),
        profile_visibility_preference=ProfileVisibility.PRIVATE,
        communication_preference=Communication.SLACK,
    )
    settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
    assert (
        settings_data.get("profile_visibility_preference") == ProfileVisibility.PRIVATE
    )
    assert settings_data.get("communication_preference") == Communication.SLACK
    settings_data = SettingsProfileSerialiser().delete_settings_profile(
        settings_data.get("id")
    )


def test_settingsprofileserialiser_update_valid_name(name, description):
    """Testing SettingsProfile Serialiser: Update SettingsProfile."""
    settings_profile = SettingsProfileSerialiser().create_settings_profile()
    regex = regex_compile(r"^Settings Profile ID: (.*)$")
    regex_match = regex.match(settings_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    settings_id = matches[0]
    settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
    assert (
        settings_data.get("profile_visibility_preference") == ProfileVisibility.PUBLIC
    )
    with raises(SettingsProfileError):
        SettingsProfileSerialiser().update_settings_profile(
            settings_data.get("id"),
            profile_visibility_preference=ProfileVisibility.PRIVATE,
            communication_preference=Communication.SLACK,
            name="name",
        )


def test_settingsprofileserialiser_create_inavild_name(description):
    """Testing SettingsProfile Serialiser: Create SettingsProfile Invalid [Name]."""
    settings_profile = SettingsProfileSerialiser().create_settings_profile()
    regex = regex_compile(r"^Settings Profile ID: (.*)$")
    regex_match = regex.match(settings_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    settings_id = matches[0]
    settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
    assert (
        settings_data.get("profile_visibility_preference") == ProfileVisibility.PUBLIC
    )
    with raises(SettingsProfileError):
        SettingsProfileSerialiser().update_settings_profile(
            settings_data.get("id"),
            profile_visibility_preference=ProfileVisibility.ADMIN,
            communication_preference="SLACK",
        )


def test_settingsprofileserialiser_get_inavild_private_id():
    """Testing SettingsProfile Serialiser: Create SettingsProfile Invalid [Card ID]."""
    with raises(SettingsProfileError):
        assert SettingsProfileSerialiser().get_settings_profile("id")


def test_settingsprofileserialiser_delete_inavild_private_id():
    """Testing SettingsProfile Serialiser: Create SettingsProfile Invalid [Card ID]."""
    with raises(SettingsProfileError):
        assert SettingsProfileSerialiser().delete_settings_profile("id")


def test_settingsprofileserialiser_update_inavild_kwargs():
    """Testing SettingsProfile Serialiser: Create SettingsProfile Invalid [Card ID]."""
    with raises(SettingsProfileError):
        assert SettingsProfileSerialiser().delete_settings_profile("id")
