"""Users Module: Testing the Settings Class."""

from pytest import raises

from sqlalchemy.orm import Session

from models import ENGINE
from models.user.accounts import Account
from models.user.settings import SettingsProfile
from models.user.users import User
from tests.conftest import run_test_teardown, setup_test_commit


def test_settings_invalid_no_args(get_account):
    """Testing Settings With Missing Attributes."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings_profile = SettingsProfile()
        settings_profile.account_id = get_account.id
        setup_test_commit(settings_profile, session)

        assert settings_profile.id is not None

        run_test_teardown(settings_profile.id, SettingsProfile, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_settings_profile_invalid_args(email, password):
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            settings_profile = SettingsProfile(email, password)
            session.add(settings_profile)
            session.commit()
