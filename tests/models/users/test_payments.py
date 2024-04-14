"""Users Module: Testing the Payments Profile Class."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ENGINE
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.users import User
from models.warehouse.cards import Card
from tests.conftest import setup_test_commit, run_test_teardown


def test_user_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            payment_profile = PaymentProfile()
            session.add(payment_profile)
            session.commit()


def test_payment_profile_invalid_args(email, password):
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            payment_profile = PaymentProfile(email, password)
            session.add(payment_profile)
            session.commit()


def test_payment_profile_valid(get_card, get_account):
    """Testing a Valid User Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfile()

        payment_profile.card_id = get_card.id
        payment_profile.account_id = get_account.id
        payment_profile.name = "Delali Funani Test Profile"
        payment_profile.description = (
            "Longer Description of the Delali Funani Test Profile"
        )

        setup_test_commit(payment_profile, session)

        assert payment_profile.id is not None

        run_test_teardown(payment_profile.id, PaymentProfile, session)
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)
