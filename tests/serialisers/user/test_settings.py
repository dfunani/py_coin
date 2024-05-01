"""Serialisers Module: Testing Accounts Serialiser."""

from datetime import datetime
from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import AccountError, SettingsProfileError, UserError
from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    ProfileVisibility,
    Status,
    Theme,
    Verification,
)
from models.user.accounts import Account
from models.user.settings import SettingsProfile
from models.user.users import User
from models.warehouse.cards import Card
from serialisers.user.settings import SettingsProfileSerialiser
from models import ENGINE
from tests.conftest import get_id_by_regex, run_test_teardown


def test_paymentprofileserialiser_create(account):
    """Testing Account Serialiser: Create Account."""

    with Session(ENGINE) as session:
        settings = SettingsProfileSerialiser().create_settings_profile(account.id)
        settings_id = get_id_by_regex(settings)
        settings = (
            session.query(SettingsProfile)
            .filter(SettingsProfile.settings_id == settings_id)
            .one_or_none()
        )
        assert settings.id is not None

        run_test_teardown(settings.id, SettingsProfile, session)


def test_paymentprofileserialiser_create_invalid():
    """Testing Account Serialiser: Create Account."""

    with raises(SettingsProfileError):
        SettingsProfileSerialiser().create_settings_profile("user.id")


def test_paymentprofileserialiser_get(settings):
    """Testing Account Serialiser: Get Account."""

    settings_data = SettingsProfileSerialiser().get_settings_profile(
        settings.settings_id
    )

    assert isinstance(settings_data, dict)
    for key in settings_data:
        assert key not in SettingsProfile.__EXCLUDE_ATTRIBUTES__


def test_paymentprofileserialiser_get_invalid():
    """Testing Account Serialiser: Get Account."""

    with raises(SettingsProfileError):
        SettingsProfileSerialiser().get_settings_profile("account_id")


def test_paymentprofileserialiser_delete(settings):
    """Testing Account Serialiser: Delete Account."""

    SettingsProfileSerialiser().delete_settings_profile(settings.id)


def test_paymentprofileserialiser_delete_invalid():
    """Testing Account Serialiser: Delete Account."""

    with raises(SettingsProfileError):
        SettingsProfileSerialiser().delete_settings_profile("account_data.id")


def test_paymentprofileserialiser_update_valid(settings):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        test_now = datetime.now()
        SettingsProfileSerialiser().update_settings_profile(
            settings.id,
            mfa_enabled=True,
            location_tracking_enabled=True,
            cookies_enabled=True,
            email_status=Verification.VERIFIED,
            data_sharing_preferences=[DataSharingPreference.PROFILE],
            communication_preference=Communication.SLACK,
            theme_preference=Theme.BLUE,
            profile_visibility_preference=ProfileVisibility.PRIVATE,
            mfa_last_used_date=test_now,
            communication_status=Verification.FAILED,
        )
        settings = session.get(SettingsProfile, settings.id)
        assert settings.id is not None
        assert settings.mfa_enabled == True
        assert settings.location_tracking_enabled == True
        assert settings.cookies_enabled == True
        assert settings.email_status == Verification.VERIFIED
        assert settings.data_sharing_preferences == [DataSharingPreference.PROFILE]
        assert settings.communication_preference == Communication.SLACK
        assert settings.theme_preference == Theme.BLUE
        assert settings.profile_visibility_preference == ProfileVisibility.PRIVATE
        assert settings.mfa_last_used_date == test_now
        assert settings.communication_status == Verification.FAILED


def test_paymentprofileserialiser_update_invalid(settings):
    """Testing Account Serialiser: Update Account."""

    with raises(SettingsProfileError):
        SettingsProfileSerialiser().update_settings_profile(
            "settings.id",
            mfa_enabled="",
            location_tracking_enabled="",
            cookies_enabled="",
            email_status="",
            data_sharing_preferences="",
            communication_preference="",
            theme_preference="",
            profile_visibility_preference="",
            mfa_last_used_date="",
            communication_status="",
        )
        SettingsProfileSerialiser().update_settings_profile(
            settings.id,
            data_sharing_preferences=["DataSharingPreference.PROFILE"],
            profile_visibility_preference=ProfileVisibility.ADMIN,
        )
