"""Users Module: Testing the Settings Class."""

from pytest import raises

from sqlalchemy.orm import Session

from models import ENGINE
from models.user.accounts import Account
from models.user.settings import SettingsProfile
from models.user.users import User
from lib.utils.constants.users import Verification
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit


def test_settings_invalid_no_args(get_account, regex_account):
    """Testing Settings With Missing Attributes."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)
        account_id = get_id_by_regex(regex_account, str(get_account))
        account_data = (
            session.query(Account)
            .filter(Account.account_id == account_id)
            .one_or_none()
        )
        settings_profile = SettingsProfile()
        settings_profile.account_id = account_data.id
        setup_test_commit(settings_profile, session)
        assert settings_profile.id is not None
        assert settings_profile.email_status == Verification.UNVERIFIED
        run_test_teardown(settings_profile.id, SettingsProfile, session)
        run_test_teardown(account_data.id, Account, session)
        run_test_teardown(account_data.user_id, User, session)


def test_settings_profile_invalid_args(email, password):
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            settings_profile = SettingsProfile(email, password)
            session.add(settings_profile)
            session.commit()
