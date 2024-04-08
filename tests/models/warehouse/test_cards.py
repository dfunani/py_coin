"""Base Test Module testing the User Abstract Class"""

from datetime import date
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from serialisers.warehouse.cards import CardSerialiser
from lib.utils.constants.users import CardStatus, CardType
from models import ENGINE
from models.warehouse.cards import Card
from tests.conftest import setup_test_commit, run_test_teardown


def test_card_invalid_no_args():
    """Testing Card With Missing Attributes."""
    with Session(ENGINE) as session:
        with raises(IntegrityError):
            card = Card()
            session.add(card)
            session.commit()


def test_card_invalid_args():
    """Testing Constructor, for Invalid Arguments."""
    with Session(ENGINE) as session:
        with raises(TypeError):
            card = Card(CardType.CHEQUE)
            session.add(card)
            session.commit()


def test_card_valid():
    """Testing a Valid Card Constructor, with Required Arguments."""
    for key in CardType:
        with Session(ENGINE) as session:
            card = Card()
            card.card_number = CardSerialiser().generate_card(
                key, "123", date.today().replace(day=1)
            )
            card.cvv_number = "123"
            card.card_type = key
            card.pin = "123456"
            card.expiration_date = date.today().replace(day=1)

            setup_test_commit(card, session)

            assert card.card_status == CardStatus.NEW

            run_test_teardown(card.id, Card, session)
