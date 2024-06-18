"""BlockChain: Testing Transaction Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.utils.constants.transactions import TransactionStatus
from models import ENGINE
from models.blockchain.transactions import Transaction
from tests.conftest import run_test_teardown


def test_transaction_invalid_no_args():
    """Testing Transaction With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            transaction = Transaction()
            session.add(transaction)
            session.commit()


def test_transaction_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            transaction = Transaction("email", "password")
            session.add(transaction)
            session.commit()


def test_transaction_valid(get_payments):
    """Testing a Valid Transaction Constructor, with Required Arguments."""

    for sender, receiver in zip(get_payments, list(reversed(get_payments))):
        with Session(ENGINE) as session:
            transaction = Transaction()
            transaction.sender = sender.id
            transaction.receiver = receiver.id
            transaction.amount = 5.0
            session.add(transaction)
            session.commit()

            assert transaction.id is not None
            assert transaction.transaction_status == TransactionStatus.DRAFT
            assert transaction.amount == 5.0
            assert isinstance(transaction.to_dict(), dict)

            run_test_teardown({transaction}, session)
