"""Controllers Module: Testing Card Serialiser."""

from datetime import date
import json
from re import compile as regex_regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.utils.encryption.encoders import get_hash_value
from serialisers.warehouse.cards import CardSerialiser
from lib.interfaces.exceptions import CardValidationError, UserError
from lib.utils.constants.users import Status, CardType
from models import ENGINE
from models.warehouse.cards import Card
from tests.conftest import get_id_by_regex, run_test_teardown


def test_cardserialiser_create():
    """Testing Card Serialiser: Create Card."""

    with Session(ENGINE) as session:
        card = CardSerialiser().create_card(CardType.CHEQUE, "123456")
        card_id = get_id_by_regex(card)
        card_data = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        assert card_data.id is not None
        run_test_teardown(card_data.id, Card, session)


def test_cardserialiser_create_invalid_card_type():
    """Testing Card Serialiser: Create Card."""

    with raises(CardValidationError):
        CardSerialiser().create_card("key", "1")
        CardSerialiser().create_card("key", 1)


def test_cardserialiser_get(card, app):
    """Testing Card Serialiser: Get Card."""

    card = CardSerialiser().get_card(card.card_id)
    card_data = json.loads(app.fernet.decrypt(card.encode()).decode())

    assert isinstance(card_data, dict)
    for key in card_data:
        assert key not in Card.__EXCLUDE_ATTRIBUTES__


def test_cardserialiser_get_invalid():
    """Testing Card Serialiser: Get Card."""

    with raises(CardValidationError):
        CardSerialiser().get_card("Card.id")


def test_cardserialiser_delete(card):
    """Testing Card Serialiser: Delete Card."""

    CardSerialiser().delete_card(card.id)


def test_cardserialiser_delete_invalid():
    """Testing Card Serialiser: Delete Card."""

    with raises(CardValidationError):
        CardSerialiser().delete_card('card_data.get("id")')


def test_cardserialiser_update(card):
    """Testing Card Serialiser: Update Card."""

    with Session(ENGINE) as session:
        pin = str(get_hash_value("654321", str(card.salt_value)))
        CardSerialiser().update_card(card.id, pin="654321", status=Status.ACTIVE)
        card = session.get(Card, card.id)
        assert card.id is not None
        assert card.pin == pin
        assert card.status == Status.ACTIVE


def test_cardserialiser_update_invalid(card):
    """Testing Card Serialiser: Update Card."""

    with raises(CardValidationError):
        CardSerialiser().update_card(card.id, pin="dfdhghg", status=Status.DISABLED)
        CardSerialiser().update_card(card.id, pin=1, status="Status.DISABLED")
