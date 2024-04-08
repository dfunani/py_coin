"""Controllers Module: Testing Card Serialiser."""

from datetime import date
import json
from re import compile as regex_regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from serialisers.warehouse.cards import CardSerialiser
from lib.interfaces.exceptions import CardValidationError
from lib.utils.constants.users import Status, CardType
from models import ENGINE
from models.warehouse.cards import Card
from tests.conftest import run_test_teardown


def test_cardserialiser_create():
    """Testing Card Serialiser: Create Card."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        card_id = matches[0]
        with Session(ENGINE) as session:
            card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
            run_test_teardown(card.id, Card, session)


def test_cardserialiser_get(app, card_keys):
    """Testing Card Serialiser: Get Card."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]

        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())

        assert isinstance(card_data, dict)
        for key in card_keys:
            assert key in card_data
            assert card_data[key] is not None

        for key in card_data:
            assert key in card_keys

        with Session(ENGINE) as session:
            run_test_teardown(card_data["id"], Card, session)


def test_cardserialiser_delete():
    """Testing Card Serialiser: Delete Card."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]
        with Session(ENGINE) as session:
            card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
            CardSerialiser().delete_card(card.id)


def test_cardserialiser_update_pin(app):
    """Testing Card Serialiser: Update Card."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())
        assert CardSerialiser().update_card(card_data.get("id"), pin="254635")
        CardSerialiser().delete_card(card_data.get("id"))


def test_cardserialiser_update_card_status(app):
    """Testing Card Serialiser: Update Card."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())
        assert CardSerialiser().update_card(
            card_data.get("id"), card_status=Status.ACTIVE
        )
        CardSerialiser().delete_card(card_data.get("id"))


def test_cardserialiser_update_card_number(app):
    """Testing Card Serialiser: Update Card."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())
        with raises(CardValidationError):
            assert CardSerialiser().update_card(
                card_data.get("id"), card_number="254635"
            )
        CardSerialiser().delete_card(card_data.get("id"))


def test_cardserialiser_create_invalid_card_type():
    """Testing Card Serialiser: Invalid Create Card [Card Type]."""
    with raises(CardValidationError):
        CardSerialiser().create_card("card_type", "123456")


def test_cardserialiser_create_invalid_pin():
    """Testing Card Serialiser: Invalid Create Card [Pin]."""
    with raises(CardValidationError):
        CardSerialiser().create_card(CardType.CHEQUE, "pin")


def test_cardserialiser_get_invalid_card_id():
    """Testing Card Serialiser: Invalid Get Card [Card ID]."""
    with raises(CardValidationError):
        CardSerialiser().get_card("card_id")


def test_cardserialiser_update_invalid_id():
    """Testing Card Serialiser: Invalid Update Card."""
    with raises(CardValidationError):
        CardSerialiser().update_card("id")


def test_cardserialiser_update_invalid_key(app):
    """Testing Card Serialiser: Invalid Update Card [Key]."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())
        with raises(CardValidationError):
            CardSerialiser().update_card(card_data.get("id"), card_number="password")
        CardSerialiser().delete_card(card_data.get("id"))


def test_cardserialiser_update_invalid_pin(app):
    """Testing Card Serialiser: Invalid Update Card [Pin]."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())
        with raises(CardValidationError):
            CardSerialiser().update_card(card_data.get("id"), pin="password")
        CardSerialiser().delete_card(card_data.get("id"))


def test_cardserialiser_update_invalid_card_status(app):
    """Testing Card Serialiser: Invalid Update Card [Card Status]."""
    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        regex = regex_regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())
        with raises(CardValidationError):
            CardSerialiser().update_card(
                card_data.get("id"), card_status=Status.DISABLED
            )
        CardSerialiser().delete_card(card_data.get("id"))


def test_cardserialiser_delete_invalid():
    """Testing Card Serialiser: Invalid Delete Card."""
    with raises(CardValidationError):
        CardSerialiser().delete_card("id")


def test_cardserialiser_get_validated_card_id():
    """Testing Card Serialiser: Invalid Card ID [Email]."""
    CardSerialiser().get_card_id("123", "1991123123123", date.today())
