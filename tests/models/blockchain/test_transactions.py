"""BlockChain Module: Testing the Transactions Class."""

from datetime import date
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from lib.utils.constants.transactions import TransactionStatus
from lib.utils.constants.users import CardType, Status
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.blockchain.transactions import Transaction
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.users import User
from models.warehouse.cards import Card
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


def test_transaction_valid(payment, payment2):
    """Testing a Valid Transaction Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        transaction = Transaction()
        transaction.sender = payment.id
        transaction.receiver = payment2.id
        transaction.amount = 5.0
        session.add(transaction)
        session.commit()

        assert transaction.id is not None
        assert transaction.transaction_status == TransactionStatus.DRAFT
        assert transaction.amount == 5.0
        assert isinstance(transaction.to_dict(), dict)
        
        run_test_teardown(transaction.id, Transaction, session)
