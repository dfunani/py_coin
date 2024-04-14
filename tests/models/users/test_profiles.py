"""Users Module: Testing the User Profile Class."""

from datetime import date
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.utils.constants.users import Gender
from models import ENGINE
from models.user.accounts import Account
from models.user.profiles import UserProfile
from models.user.users import User
from tests.conftest import run_test_teardown, setup_test_commit


def test_user_profile_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            user_profile = UserProfile()
            session.add(user_profile)
            session.commit()


def test_user_profile_profile_invalid_args(email, password):
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            user_profile = UserProfile(email, password)
            session.add(user_profile)
            session.commit()


def test_user_profile__(get_account):
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        user_profile = UserProfile()

        user_profile.account_id = get_account.id
        user_profile.first_name = "firstname"
        user_profile.last_name = "lastnaame"
        user_profile.username = "username_fl"
        user_profile.date_of_birth = date(1991, 12, 31)
        user_profile.gender = Gender.FEMALE

        setup_test_commit(user_profile, session)

        assert user_profile.interests == []
        assert user_profile.account_id is not None

        run_test_teardown(user_profile.id, UserProfile, session)
        run_test_teardown(user_profile.account_id, Account, session)
        run_test_teardown(get_account.user_id, User, session)
