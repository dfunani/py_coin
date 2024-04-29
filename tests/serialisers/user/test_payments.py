"""Serialisers Module: Testing Payments Serialiser."""

import json
from re import compile as regex_compile

from pytest import raises
from sqlalchemy.orm import Session

from lib.utils.constants.users import CardType
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
from tests.conftest import run_test_teardown, setup_test_commit


def test_paymentprofileserialiser_create(get_card, get_account, regex_payment):
    """Testing PaymentProfile Serialiser: Create PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = (
            session.query(PaymentProfile)
            .filter(PaymentProfile.payment_id == payment_id)
            .one_or_none()
        )
        setup_test_commit(payment, session)
        run_test_teardown(payment.id, PaymentProfile, session)
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_create_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises(PaymentProfileError):
        PaymentProfileSerialiser().create_payment_profile("private_id", "private_id")


def test_paymentprofileserialiser_get(get_card, get_account, regex_payment):
    """Testing PaymentProfile Serialiser: Get PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)

        run_test_teardown(payment.get("id"), PaymentProfile, session)
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_get_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().get_payment_profile("id")


def test_paymentprofileserialiser_delete(get_card, get_account, regex_payment):
    """Testing PaymentProfile Serialiser: Delete PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)

        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_delete_inavild_private_id():
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises(PaymentProfileError):
        assert PaymentProfileSerialiser().delete_payment_profile("id")


def test_paymentprofileserialiser_update_valid_balance(
    get_card, get_account, regex_payment
):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)

        PaymentProfileSerialiser().update_payment_profile(
            payment.get("id"), balance=5.0
        )
        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_name(
    get_card, get_account, regex_payment
):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)
        PaymentProfileSerialiser().update_payment_profile(
            payment.get("id"), name="Well described name for profile"
        )
        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_description(
    get_card, get_account, regex_payment
):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)
        PaymentProfileSerialiser().update_payment_profile(
            payment.get("id"),
            description="Longer Description - Well described name for profile.",
        )
        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_balance_invalid(
    get_card, get_account, regex_payment
):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)

        with raises(PaymentProfileError):
            PaymentProfileSerialiser().update_payment_profile(
                payment.get("id"), balance="5.0"
            )
        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_balance_invalid_2(
    get_card, get_account, regex_payment
):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)

        with raises(PaymentProfileError):
            PaymentProfileSerialiser().update_payment_profile(
                payment.get("id"), balance=-5.0
            )
        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_name_type(
    get_card, get_account, regex_payment
):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)

        with raises(UserError):
            PaymentProfileSerialiser().update_payment_profile(
                payment.get("id"), name="Well?"
            )

        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_description(
    get_card, get_account, regex_payment
):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    with Session(ENGINE) as session:
        setup_test_commit(get_card, session)
        setup_test_commit(get_account, session)

        payment_profile = PaymentProfileSerialiser().create_payment_profile(
            get_account.id, get_card.id
        )
        payment_id = get_id_by_regex(regex_payment, payment_profile)
        payment = PaymentProfileSerialiser().get_payment_profile(payment_id)

        with raises(UserError):
            PaymentProfileSerialiser().update_payment_profile(
                payment.get("id"),
                description="Long:",
            )

        PaymentProfileSerialiser().delete_payment_profile(payment.get("id"))
        run_test_teardown(get_card.id, Card, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)
