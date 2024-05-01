"""Users Module: Testing the Payments Profile Class."""

from datetime import datetime
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.utils.constants.users import CardType, Status
from models import ENGINE
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.users import User
from models.warehouse.cards import Card
from tests.conftest import run_test_teardown


def test_user_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            payment_profile = PaymentProfile()
            session.add(payment_profile)
            session.commit()


def test_payment_profile_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            payment_profile = PaymentProfile("email", "password")
            session.add(payment_profile)
            session.commit()


def test_payment_profile_valid():
    """Testing a Valid User Constructor, with Required Arguments."""

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

        card = Card()
        card.card_number = "1991123456789"
        card.cvv_number = "123"
        card.pin = "123456"
        card.card_type = CardType.CHEQUE
        card.expiration_date = datetime.now()
        session.add(card)
        session.commit()

        payment_profile = PaymentProfile()
        payment_profile.card_id = card.id
        payment_profile.account_id = account.id
        payment_profile.name = "Delali Funani Test Profile"
        payment_profile.description = (
            "Longer Description of the Delali Funani Test Profile"
        )
        session.add(payment_profile)
        session.commit()

        assert payment_profile.id is not None
        assert payment_profile.balance == 0.0
        assert payment_profile.status == Status.NEW

        run_test_teardown(payment_profile.id, PaymentProfile, session)
        run_test_teardown(card.id, Card, session)
        run_test_teardown(account.id, Account, session)
        run_test_teardown(user.id, User, session)
