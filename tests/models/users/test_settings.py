"""Settings Module: Testing the Settings Class."""

from pytest import raises

from sqlalchemy.orm import Session

from models import ENGINE
from models.user.settings import SettingsProfile
from lib.utils.constants.users import Verification


def test_settings_invalid_no_args():
    """Testing User With Missing Attributes."""
    with Session(ENGINE) as session:
        settings_profile = SettingsProfile()
        session.add(settings_profile)
        session.commit()
        assert settings_profile.id is not None
        assert settings_profile.email_status == Verification.UNVERIFIED


def test_settings_profile_invalid_args(email, password):
    """Testing Constructor, for Invalid Arguments."""
    with Session(ENGINE) as session:
        with raises(TypeError):
            settings_profile = SettingsProfile(email, password)
            session.add(settings_profile)
            session.commit()
