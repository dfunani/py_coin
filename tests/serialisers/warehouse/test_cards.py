"""Controllers Module: Testing Card Serialiser."""

from datetime import date
import json
from re import compile as regex_regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from serialisers.warehouse.cards import CardSerialiser
from lib.interfaces.exceptions import CardValidationError, UserError
from lib.utils.constants.users import Status, CardType
from models import ENGINE
from models.warehouse.cards import Card
from tests.conftest import get_id_by_regex, run_test_teardown


def test_cardserialiser_create(regex_card):
    """Testing Card Serialiser: Create Card."""

    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        card_id = get_id_by_regex(regex_card, card)
        with Session(ENGINE) as session:
            card_data = (
                session.query(Card).filter(Card.card_id == card_id).one_or_none()
            )
            assert card_data.id is not None
            run_test_teardown(card_data.id, Card, session)


def test_cardserialiser_create_invalid_card_type():
    """Testing Card Serialiser: Create Card."""

    with raises(CardValidationError):
        CardSerialiser().create_card("key", "123456")


def test_cardserialiser_create_invalid_pin():
    """Testing Card Serialiser: Create Card."""

    with raises(CardValidationError):
        CardSerialiser().create_card("key", "1")


def test_cardserialiser_get(app, card_keys, regex_card):
    """Testing Card Serialiser: Get Card."""

    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        card_id = get_id_by_regex(regex_card, card)

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


def test_cardserialiser_get_invalid():
    """Testing Card Serialiser: Get Card."""

    with raises(CardValidationError):
        CardSerialiser().get_card("Card.id")


def test_cardserialiser_delete(app, regex_card):
    """Testing Card Serialiser: Delete Card."""

    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        card_id = get_id_by_regex(regex_card, card)

        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())
        CardSerialiser().delete_card(card_data.get("id"))


def test_cardserialiser_delete_invalid():
    """Testing Card Serialiser: Delete Card."""

    with raises(CardValidationError):
        CardSerialiser().delete_card('card_data.get("id")')


def test_cardserialiser_update_pin(app, card_keys, regex_card):
    """Testing Card Serialiser: Update Card."""

    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        card_id = get_id_by_regex(regex_card, card)

        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())

        CardSerialiser().update_card(card_data["id"], pin="654321")

        with Session(ENGINE) as session:
            run_test_teardown(card_data["id"], Card, session)


def test_cardserialiser_update_pin_invalid(app, regex_card):
    """Testing Card Serialiser: Update Card."""

    for key in CardType:
        with Session(ENGINE) as session:
            card = CardSerialiser().create_card(key, "123456")
            card_id = get_id_by_regex(regex_card, card)

            card = CardSerialiser().get_card(card_id)
            card_data = json.loads(app.fernet.decrypt(card.encode()).decode())

            with raises(CardValidationError):
                CardSerialiser().update_card(card_data["id"], pin="dfdhghg")

            run_test_teardown(card_data["id"], Card, session)


def test_cardserialiser_update_pin_invalid_id():
    """Testing Card Serialiser: Update Card."""

    with raises(CardValidationError):
        CardSerialiser().update_card("card_data.id", pin="654321")


def test_cardserialiser_update_status(app, regex_card):
    """Testing Card Serialiser: Update Card."""

    for key in CardType:
        card = CardSerialiser().create_card(key, "123456")
        card_id = get_id_by_regex(regex_card, card)

        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(app.fernet.decrypt(card.encode()).decode())

        CardSerialiser().update_card(card_data["id"], status=Status.ACTIVE)

        with Session(ENGINE) as session:
            run_test_teardown(card_data["id"], Card, session)


def test_cardserialiser_update_status_invalid(app, regex_card):
    """Testing Card Serialiser: Update Card."""

    for key in CardType:
        with Session(ENGINE) as session:
            card = CardSerialiser().create_card(key, "123456")
            card_id = get_id_by_regex(regex_card, card)

            card = CardSerialiser().get_card(card_id)
            card_data = json.loads(app.fernet.decrypt(card.encode()).decode())

            with raises(UserError):
                CardSerialiser().update_card(card_data["id"], status="dfdhghg")

            run_test_teardown(card_data["id"], Card, session)
