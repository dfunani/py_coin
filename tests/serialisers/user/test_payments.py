"""Serialisers Module: Testing Payments Serialiser."""

import json
from re import compile as regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.utils.constants.users import CardType
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.user.payments import PaymentProfileSerialiser
from lib.interfaces.exceptions import CardValidationError, PaymentProfileError
from models import ENGINE
from serialisers.warehouse.cards import CardSerialiser
from tests.conftest import run_test_teardown


def test_paymentprofileserialiser_create(name, description):
    """Testing PaymentProfile Serialiser: Create PaymentProfile."""
    card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
    regex = regex_compile(r"^Card ID: (.*)$")
    regex_match = regex.match(card)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    card_id = matches[0]
    card = CardSerialiser().get_card(card_id)
    card_data = json.loads(decrypt_data(card))
    payment_profile = PaymentProfileSerialiser().create_payment_profile(
        name, description, card_data.get("id")
    )
    regex = regex_compile(r"^Payment Profile ID: (.*)$")
    regex_match = regex.match(payment_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    payment_id = matches[0]
    with Session(ENGINE) as session:
        payment = (
            session.query(PaymentProfile)
            .filter(PaymentProfile.payment_id == payment_id)
            .one_or_none()
        )
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        run_test_teardown(payment.id, PaymentProfile, session)
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_get(name, description):
    """Testing PaymentProfile Serialiser: Get PaymentProfile."""
    card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
    regex = regex_compile(r"^Card ID: (.*)$")
    regex_match = regex.match(card)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    card_id = matches[0]
    card = CardSerialiser().get_card(card_id)
    card_data = json.loads(decrypt_data(card))
    payment_profile = PaymentProfileSerialiser().create_payment_profile(
        name, description, card_data.get("id")
    )
    regex = regex_compile(r"^Payment Profile ID: (.*)$")
    regex_match = regex.match(payment_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    payment_id = matches[0]
    profile = PaymentProfileSerialiser().get_payment_profile(payment_id)
    assert profile.get("id") is not None
    with Session(ENGINE) as session:
        payment = (
            session.query(PaymentProfile)
            .filter(PaymentProfile.payment_id == payment_id)
            .one_or_none()
        )
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        run_test_teardown(payment.id, PaymentProfile, session)
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_delete(name, description):
    """Testing PaymentProfile Serialiser: Delete PaymentProfile."""
    card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
    regex = regex_compile(r"^Card ID: (.*)$")
    regex_match = regex.match(card)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    card_id = matches[0]
    card = CardSerialiser().get_card(card_id)
    card_data = json.loads(decrypt_data(card))
    payment_profile = PaymentProfileSerialiser().create_payment_profile(
        name, description, card_data.get("id")
    )
    regex = regex_compile(r"^Payment Profile ID: (.*)$")
    regex_match = regex.match(payment_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    payment_id = matches[0]
    payment_data = PaymentProfileSerialiser().get_payment_profile(payment_id)
    assert PaymentProfileSerialiser().delete_payment_profile(payment_data.get("id"))
    with Session(ENGINE) as session:
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_update_valid_balance(name, description):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""
    card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
    regex = regex_compile(r"^Card ID: (.*)$")
    regex_match = regex.match(card)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    card_id = matches[0]
    card = CardSerialiser().get_card(card_id)
    card_data = json.loads(decrypt_data(card))
    payment_profile = PaymentProfileSerialiser().create_payment_profile(
        name, description, card_data.get("id")
    )
    regex = regex_compile(r"^Payment Profile ID: (.*)$")
    regex_match = regex.match(payment_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    payment_id = matches[0]
    payment_data = PaymentProfileSerialiser().get_payment_profile(payment_id)
    assert PaymentProfileSerialiser().update_payment_profile(
        payment_data.get("id"), balance=5.0
    )
    with Session(ENGINE) as session:
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        PaymentProfileSerialiser().delete_payment_profile(payment_data.get("id"))
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_update_valid_name(name, description):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""
    card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
    regex = regex_compile(r"^Card ID: (.*)$")
    regex_match = regex.match(card)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    card_id = matches[0]
    card = CardSerialiser().get_card(card_id)
    card_data = json.loads(decrypt_data(card))
    payment_profile = PaymentProfileSerialiser().create_payment_profile(
        name, description, card_data.get("id")
    )
    regex = regex_compile(r"^Payment Profile ID: (.*)$")
    regex_match = regex.match(payment_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    payment_id = matches[0]
    payment_data = PaymentProfileSerialiser().get_payment_profile(payment_id)
    assert PaymentProfileSerialiser().update_payment_profile(
        payment_data.get("id"), name="Hello World"
    )
    with Session(ENGINE) as session:
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        PaymentProfileSerialiser().delete_payment_profile(payment_data.get("id"))
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_update_valid_description(name, description):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""
    card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
    regex = regex_compile(r"^Card ID: (.*)$")
    regex_match = regex.match(card)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    card_id = matches[0]
    card = CardSerialiser().get_card(card_id)
    card_data = json.loads(decrypt_data(card))
    payment_profile = PaymentProfileSerialiser().create_payment_profile(
        name, description, card_data.get("id")
    )
    regex = regex_compile(r"^Payment Profile ID: (.*)$")
    regex_match = regex.match(payment_profile)
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    payment_id = matches[0]
    payment_data = PaymentProfileSerialiser().get_payment_profile(payment_id)
    assert PaymentProfileSerialiser().update_payment_profile(
        payment_data.get("id"), description="Longer Description Hello World"
    )
    with Session(ENGINE) as session:
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        PaymentProfileSerialiser().delete_payment_profile(payment_data.get("id"))
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_create_inavild_name(description):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Name]."""
    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().create_payment_profile(
            "name", description, "private_id"
        )


def test_paymentprofileserialiser_create_inavild_description(name):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Description]."""
    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().create_payment_profile(
            name, "desc", "private_id"
        )


def test_paymentprofileserialiser_create_inavild_private_id(name, description):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""
    with raises(CardValidationError):
        assert PaymentProfileSerialiser().create_payment_profile(
            name, description, "private_id"
        )


def test_paymentprofileserialiser_get_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""
    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().get_payment_profile("id")


def test_paymentprofileserialiser_delete_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""
    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().delete_payment_profile("id")


def test_paymentprofileserialiser_update_inavild_kwargs(name, description):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""
    with raises(PaymentProfileError):
        card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
        regex = regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(decrypt_data(card))
        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            name, description, card_data.get("id")
        )
        regex = regex_compile(r"^Payment Profile ID: (.*)$")
        regex_match = regex.match(payment_profile)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        payment_id = matches[0]
        payment_data = PaymentProfileSerialiser().get_payment_profile(payment_id)
        assert PaymentProfileSerialiser().update_payment_profile(
            payment_data.get("id"), email="Longer Description Hello World"
        )
    with Session(ENGINE) as session:
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        PaymentProfileSerialiser().delete_payment_profile(payment_data.get("id"))
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_update_inavild_kwargs_name(name, description):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Name]."""
    with raises(PaymentProfileError):
        card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
        regex = regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(decrypt_data(card))
        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            name, description, card_data.get("id")
        )
        regex = regex_compile(r"^Payment Profile ID: (.*)$")
        regex_match = regex.match(payment_profile)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        payment_id = matches[0]
        payment_data = PaymentProfileSerialiser().get_payment_profile(payment_id)
        assert PaymentProfileSerialiser().update_payment_profile(
            payment_data.get("id"), name="short"
        )
    with Session(ENGINE) as session:
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        PaymentProfileSerialiser().delete_payment_profile(payment_data.get("id"))
        run_test_teardown(card.id, Card, session)


def test_paymentprofileserialiser_update_inavild_kwargs_description(name, description):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""
    with raises(PaymentProfileError):
        card = CardSerialiser().create_card(CardType.SAVINGS, "123456")
        regex = regex_compile(r"^Card ID: (.*)$")
        regex_match = regex.match(card)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        card_id = matches[0]
        card = CardSerialiser().get_card(card_id)
        card_data = json.loads(decrypt_data(card))
        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            name, description, card_data.get("id")
        )
        regex = regex_compile(r"^Payment Profile ID: (.*)$")
        regex_match = regex.match(payment_profile)
        matches = regex_match.groups()
        assert regex_match is not None
        assert len(matches) == 1
        payment_id = matches[0]
        payment_data = PaymentProfileSerialiser().get_payment_profile(payment_id)
        assert PaymentProfileSerialiser().update_payment_profile(
            payment_data.get("id"), description="Longer"
        )
    with Session(ENGINE) as session:
        card = session.query(Card).filter(Card.card_id == card_id).one_or_none()
        PaymentProfileSerialiser().delete_payment_profile(payment_data.get("id"))
        run_test_teardown(card.id, Card, session)
