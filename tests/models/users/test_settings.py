"""Users Module: Testing the Settings Class."""

from pytest import raises

from sqlalchemy.orm import Session

from lib.utils.constants.users import Communication, Status, Verification
from models import ENGINE
from models.user.accounts import Account
from models.user.settings import SettingsProfile
from models.user.users import User
from tests.conftest import run_test_teardown, setup_test_commit


def test_settings_invalid_no_args():
    """Testing Settings With Missing Attributes."""

    with Session(ENGINE) as session:
        user = User()
        user.email = "email@test.com"
        user.password = "password@123455"
        user.user_id = "test_user_id"
        session.add(user)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        settings_profile = SettingsProfile()
        settings_profile.account_id = account.id
        session.add(settings_profile)
        session.commit()

        assert settings_profile.id is not None
        assert settings_profile.mfa_enabled == False
        assert settings_profile.communication_status == Verification.UNVERIFIED
        assert settings_profile.communication_preference == Communication.EMAIL
        assert settings_profile.cookies_enabled == False

        run_test_teardown(settings_profile.id, SettingsProfile, session)
        run_test_teardown(account.id, Account, session)
        run_test_teardown(user.id, User, session)


def test_settings_profile_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            settings_profile = SettingsProfile("email", "password")
            session.add(settings_profile)
            session.commit()
