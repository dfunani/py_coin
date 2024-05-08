"""Users Module: Testing the Settings Class."""

from pytest import raises

from sqlalchemy.orm import Session

from lib.utils.constants.users import Communication, Verification
from models import ENGINE
from models.user.accounts import Account
from models.user.settings import SettingsProfile
from models.user.users import User
from tests.conftest import run_test_teardown


def test_settings_invalid_no_args(account):
    """Testing Settings With Missing Attributes."""

    with Session(ENGINE) as session:
        settings_profile = SettingsProfile()
        settings_profile.account_id = account.id
        session.add(settings_profile)
        session.commit()

        assert settings_profile.id is not None
        assert not settings_profile.mfa_enabled
        assert settings_profile.communication_status == Verification.UNVERIFIED
        assert settings_profile.communication_preference == Communication.EMAIL
        assert not settings_profile.cookies_enabled

        run_test_teardown(settings_profile.id, SettingsProfile, session)


def test_settings_profile_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            settings_profile = SettingsProfile("email", "password")
            session.add(settings_profile)
            session.commit()
