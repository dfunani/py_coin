"""Serialisers Module: Testing Payments Serialiser."""

import json
from re import compile as regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.utils.constants.users import CardType, Status
from lib.utils.encryption.cryptography import decrypt_data
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.users import User
from models.warehouse.cards import Card
from serialisers.user.payments import PaymentProfileSerialiser
from lib.interfaces.exceptions import (
    CardValidationError,
    PaymentProfileError,
    UserError,
    UserProfileError,
)
from models import ENGINE
from serialisers.warehouse.cards import CardSerialiser
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit


def test_paymentprofileserialiser_create(card, account):
    """Testing PaymentProfile Serialiser: Create PaymentProfile."""

    with Session(ENGINE) as session:
        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            account.id, card.id
        )
        payment_id = get_id_by_regex(payment_profile)
        payment = (
            session.query(PaymentProfile)
            .filter(PaymentProfile.payment_id == payment_id)
            .one_or_none()
        )
        assert payment.id is not None
        run_test_teardown(payment.id, PaymentProfile, session)


def test_paymentprofileserialiser_create_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises(PaymentProfileError):
        PaymentProfileSerialiser().create_payment_profile("private_id", "card_id")


def test_paymentprofileserialiser_get(payment):
    """Testing PaymentProfile Serialiser: Get PaymentProfile."""

    payment_data = PaymentProfileSerialiser().get_payment_profile(payment.payment_id)

    assert isinstance(payment_data, dict)
    for key in payment_data:
        assert key not in Account.__EXCLUDE_ATTRIBUTES__


def test_paymentprofileserialiser_get_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().get_payment_profile("id")


def test_paymentprofileserialiser_delete(payment):
    """Testing PaymentProfile Serialiser: Delete PaymentProfile."""

    PaymentProfileSerialiser().delete_payment_profile(payment.id)


def test_paymentprofileserialiser_delete_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().delete_payment_profile("id")


def test_paymentprofileserialiser_update_valid(payment):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        PaymentProfileSerialiser().update_payment_profile(
            payment.id,
            balance=5.0,
            name="Well described name for profile",
            description="Longer Description - Well described name for profile.",
            status=Status.ACTIVE,
        )
        payment = session.get(PaymentProfile, payment.id)
        assert payment.id is not None
        assert payment.balance == 5.0
        assert payment.name == "Well described name for profile"
        assert (
            payment.description
            == "Longer Description - Well described name for profile."
        )
        assert payment.status == Status.ACTIVE


def test_paymentprofileserialiser_update_invalid(payment):
    """Testing PaymentProfile Serialiser: Invalid Update PaymentProfile."""

    with raises(PaymentProfileError):
        PaymentProfileSerialiser().update_payment_profile(
            payment.id,
            balance=-5.0,
            name="profile",
            description="Longer",
            status=Status.DISABLED,
        )
        PaymentProfileSerialiser().update_payment_profile(
            payment.id,
            balance="5.0",
            name=1,
            description=1,
            status="Status.DISABLED",
        )
