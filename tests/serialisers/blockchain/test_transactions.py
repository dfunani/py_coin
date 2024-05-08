"""Serialisers Module: Testing Transactions Serialiser."""

from pytest import raises
from sqlalchemy.orm import Session

from config import AppConfig
from lib.interfaces.exceptions import TransactionError
from lib.utils.constants.transactions import TransactionStatus
from lib.utils.constants.users import Status
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models.blockchain.transactions import Transaction
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.blockchain.transactions import TransactionSerialiser
from models import ENGINE
from tests.conftest import get_id_by_regex, run_test_teardown


def test_transactionserialiser_create(payment, payment2):
    """Testing transaction Serialiser: Create transaction."""

    with Session(ENGINE) as session:
        transaction = TransactionSerialiser().create_Transaction(
            payment.id, payment2.id, 50.0
        )
        transaction_id = get_id_by_regex(transaction)
        transaction = (
            session.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .one_or_none()
        )
        assert transaction.id is not None
        assert transaction.amount == 50.0

        run_test_teardown(transaction.id, Transaction, session)


def test_transactioner_create_invalid():
    """Testing transaction Serialiser: Create transaction."""

    with raises(TransactionError):
        TransactionSerialiser().create_Transaction("payment.id", "payment.id", "50")


def test_transactionileserialiser_get(transaction):
    """Testing transaction Serialiser: Get transaction."""

    transaction_data = TransactionSerialiser().get_Transaction(
        transaction.transaction_id
    )

    assert isinstance(transaction_data, dict)
    for key in transaction_data:
        assert key not in transaction.__EXCLUDE_ATTRIBUTES__


def test_transactionliser_get_invalid():
    """Testing transaction Serialiser: Get transaction."""

    with raises(TransactionError):
        TransactionSerialiser().get_Transaction("transaction_id")


def test_transactionserialiser_delete(transaction):
    """Testing transaction Serialiser: Delete transaction."""

    TransactionSerialiser().delete_transaction(transaction.id)


def test_transactioner_delete_invalid():
    """Testing transaction Serialiser: Delete transaction."""

    with raises(TransactionError):
        TransactionSerialiser().delete_transaction("transaction_data.id")


def test_transactiondate_valid_amount(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with Session(ENGINE) as session:
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            amount=55.0,
        )
        transaction = session.get(Transaction, transaction.id)
        assert transaction.id is not None
        assert transaction.amount == 55.0
        assert transaction.transaction_status == TransactionStatus.DRAFT


def test_transactiondate_valid_status(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with Session(ENGINE) as session:
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            transaction_status=TransactionStatus.APPROVED,
        )
        transaction = session.get(Transaction, transaction.id)
        assert transaction.id is not None
        assert transaction.amount == 5.0
        assert transaction.transaction_status == TransactionStatus.APPROVED


def test_transactiondate_valid_status_approved(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with Session(ENGINE) as session:
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.APPROVED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.TRANSFERED,
        )
        transaction = session.get(Transaction, transaction.id)
        assert transaction.id is not None
        assert transaction.amount == 5.0
        assert transaction.transaction_status == TransactionStatus.TRANSFERED


def test_transactiondate_valid_status_approved(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with Session(ENGINE) as session:
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.APPROVED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.INSUFFICIENT,
        )
        transaction = session.get(Transaction, transaction.id)
        assert transaction.id is not None
        assert transaction.amount == 5.0
        assert transaction.transaction_status == TransactionStatus.INSUFFICIENT


def test_transactiondate_valid_status_approved(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with Session(ENGINE) as session:
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.REJECTED,
        )
        transaction = session.get(Transaction, transaction.id)
        assert transaction.id is not None
        assert transaction.amount == 5.0
        assert transaction.transaction_status == TransactionStatus.REJECTED


def test_transactiondate_valid_status_approved(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with Session(ENGINE) as session:
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            title="TransactionStatusAPPROVED",
            description="Longer Description TransactionStatus.APPROVED",
        )
        transaction = session.get(Transaction, transaction.id)
        assert transaction.id is not None
        assert transaction.amount == 5.0
        assert transaction.transaction_status == TransactionStatus.DRAFT
        assert transaction.title == "TransactionStatusAPPROVED"
        assert (
            transaction.description == "Longer Description TransactionStatus.APPROVED"
        )


def test_transactionte_invalid_status(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.REVERSED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.INSUFFICIENT,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.TRANSFERED,
        )


def test_transactionte_invalid_status_app(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.APPROVED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.REVERSED,
        )


def test_transactionte_invalid_status_rej(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.REJECTED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.TRANSFERED,
        )


def test_transactionte_invalid_status_1(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.TRANSFERED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.REJECTED,
        )

def test_transactionte_invalid_status_2(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.APPROVED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.TRANSFERED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.REJECTED,
        )

def test_transactionte_invalid_status_2(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            status=TransactionStatus.APPROVED,
        )
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            amount = 55.5
        )

def test_transactionte_invalid_status_2(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            amount = "55.5"
        )

def test_transactionte_invalid_status_2(transaction):
    """Testing transaction Serialiser: Update transaction."""

    with raises(TransactionError):
        TransactionSerialiser().update_transaction(
            transaction.id,
            transaction.sender_signiture,
            transaction.receiver_signiture,
            amounts = "55.5"
        )