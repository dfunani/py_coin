"""Payments Module: Testing the Payments Profile Class."""

import json
from re import compile as regex_compile
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ENGINE
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from lib.utils.helpers.cards import decrypt_data
from lib.utils.constants.users import CardType, PaymentStatus
from serialisers.warehouse.cards import CardSerialiser
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


def test_payment_profile_valid():
    """Testing a Valid User Constructor, with Required Arguments."""
    with Session(ENGINE) as session:
        payment_profile = PaymentProfile()
        card = CardSerialiser().create_card(CardType.CHEQUE, "123456")
        regex = regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        card_id = matches[0]

        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(decrypt_data(card))

        payment_profile.card_id = card_data.get("id")
        payment_profile.name = "Delali Funani Test Profile"
        payment_profile.description = (
            "Longer Description of the Delali Funani Test Profile"
        )

        setup_test_commit(payment_profile, session)

        assert payment_profile.payment_status == PaymentStatus.NEW
        assert payment_profile.id is not None
        assert payment_profile.balance == 0.0

        print(card_data)

        run_test_teardown(payment_profile.id, PaymentProfile, session)
        run_test_teardown(card_data.get("id"), Card, session)
