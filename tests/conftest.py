"""App Module: Testing Configuration."""

from re import compile as regex_compile
from typing import Any
from datetime import date
from pytest import fixture
from sqlalchemy.orm import Session

from config import AppConfig
from lib.utils.constants.users import CardType
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.blockchain.blocks import Block
from models.blockchain.contracts import Contract
from models.blockchain.transactions import Transaction
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.profiles import UserProfile
from models.user.settings import SettingsProfile
from models.user.users import User
from models.warehouse.cards import Card
from models.warehouse.logins import LoginHistory


@fixture
def app() -> AppConfig:
    """Initializes the Application Config."""

    return AppConfig()


def setup_test_commit(model: Any, session: Session):
    """Abstraction of the persistence functionality."""

    session.add(model)
    session.commit()


def run_test_teardown(private_id: str, model: Any, session: Session):
    """Abstraction of the Clearing of the Test Database."""

    model = session.get(model, private_id)
    session.delete(model)
    session.commit()


def get_id_by_regex(value: str) -> str:
    """Get Model ID By Regex."""

    regex = regex_compile(r"^.*: (.*)$")
    regex_match = regex.match(value)
    assert regex_match is not None
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    return matches[0]


@fixture
def user():
    """Creates a test User."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        yield user

        session.delete(user)
        session.commit()


@fixture
def account():
    """Creates a Test Account."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        yield account

        session.delete(account)
        session.delete(user)
        session.commit()


@fixture
def settings():
    """Creates a Test Setting."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        settings = SettingsProfile()
        settings.account_id = account.id
        session.add(settings)
        session.commit()

        yield settings

        session.delete(settings)
        session.delete(account)
        session.delete(user)
        session.commit()


@fixture
def card():
    """Creates a Test Card"""

    with Session(ENGINE) as session:
        card = Card()
        card.card_number = "1991123456789"
        card.card_type = CardType.CHEQUE
        card.cvv_number = "123"
        card.expiration_date = date.today()
        card.pin = "123456"

        session.add(card)
        session.commit()

        yield card

        session.delete(card)
        session.commit()


@fixture
def card2():
    """Creates a Test Card"""

    with Session(ENGINE) as session:
        card = Card()
        card.card_number = "1991123456788"
        card.card_type = CardType.CHEQUE
        card.cvv_number = "123"
        card.expiration_date = date.today()
        card.pin = "123456"

        session.add(card)
        session.commit()

        yield card

        session.delete(card)
        session.commit()


@fixture
def payment():
    """Creates a Test Account."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        card = Card()
        card.card_number = "1991123456789"
        card.card_type = CardType.CHEQUE
        card.cvv_number = "123"
        card.expiration_date = date.today()
        card.pin = "123456"

        session.add(card)
        session.commit()

        payment = PaymentProfile()
        payment.account_id = account.id
        payment.card_id = card.id

        session.add(payment)
        session.commit()

        yield payment

        session.delete(payment)
        session.delete(account)
        session.delete(user)
        session.delete(card)
        session.commit()


@fixture
def payment2():
    """Creates a Test Account."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test2@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test2@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        card = Card()
        card.card_number = "1991123456788"
        card.card_type = CardType.CHEQUE
        card.cvv_number = "123"
        card.expiration_date = date.today()
        card.pin = "123456"

        session.add(card)
        session.commit()

        payment = PaymentProfile()
        payment.account_id = account.id
        payment.card_id = card.id

        session.add(payment)
        session.commit()

        yield payment

        session.delete(payment)
        session.delete(account)
        session.delete(user)
        session.delete(card)
        session.commit()


@fixture
def profile():
    """Creates a Test Account."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        profile = UserProfile()
        profile.account_id = account.id
        session.add(profile)
        session.commit()

        yield profile

        session.delete(profile)
        session.delete(account)
        session.delete(user)
        session.commit()


@fixture
def login():
    """Creates a Test Login History."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        login = LoginHistory()
        login.user_id = user.id
        session.add(login)
        session.commit()

        yield login

        session.delete(login)
        session.delete(user)
        session.commit()


@fixture
def transaction():
    """Creates a Test Transaction."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        card1 = Card()
        card1.card_number = "1991123456789"
        card1.card_type = CardType.CHEQUE
        card1.cvv_number = "123"
        card1.expiration_date = date.today()
        card1.pin = "123456"

        session.add(card1)
        session.commit()

        card2 = Card()
        card2.card_number = "1991123456788"
        card2.card_type = CardType.CHEQUE
        card2.cvv_number = "123"
        card2.expiration_date = date.today()
        card2.pin = "123456"

        session.add(card2)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        payment1 = PaymentProfile()
        payment1.account_id = account.id
        payment1.card_id = card1.id
        session.add(payment1)
        session.commit()

        payment2 = PaymentProfile()
        payment2.account_id = account.id
        payment2.card_id = card2.id
        session.add(payment2)
        session.commit()

        transaction = Transaction()
        transaction.sender = payment1.id
        transaction.receiver = payment2.id
        transaction.amount = 5.0
        transaction.sender_signiture = get_hash_value(
            card1.card_id, transaction.salt_value
        )
        transaction.receiver_signiture = get_hash_value(
            card2.card_id, transaction.salt_value
        )
        session.add(transaction)
        session.commit()

        yield transaction

        session.delete(transaction)
        session.delete(payment1)
        session.delete(payment2)
        session.delete(account)
        session.delete(card1)
        session.delete(card2)
        session.delete(user)
        session.commit()


@fixture
def contract():
    """Creates a Test Transaction."""

    with Session(ENGINE) as session:
        user = User()
        user.email = encrypt_data("test@test.com".encode())
        user.password = get_hash_value("password123@", str(user.salt_value))
        user.user_id = get_hash_value(
            str("test@test.com") + "password123@", str(AppConfig().salt_value)
        )
        session.add(user)
        session.commit()

        card1 = Card()
        card1.card_number = "1991123456789"
        card1.card_type = CardType.CHEQUE
        card1.cvv_number = "123"
        card1.expiration_date = date.today()
        card1.pin = "123456"

        session.add(card1)
        session.commit()

        card2 = Card()
        card2.card_number = "1991123456788"
        card2.card_type = CardType.CHEQUE
        card2.cvv_number = "123"
        card2.expiration_date = date.today()
        card2.pin = "123456"

        session.add(card2)
        session.commit()

        account = Account()
        account.user_id = user.id
        session.add(account)
        session.commit()

        payment1 = PaymentProfile()
        payment1.account_id = account.id
        payment1.card_id = card1.id
        session.add(payment1)
        session.commit()

        payment2 = PaymentProfile()
        payment2.account_id = account.id
        payment2.card_id = card2.id
        session.add(payment2)
        session.commit()

        contract = Contract()
        contract.contract_id = get_hash_value(
            "Testing a string contract", contract.salt_value
        )
        contract.contractor = payment1.id
        contract.contractee = payment2.id
        contract.contract = "Testing a string contract"
        contract.contractor_signiture = get_hash_value(
            card1.card_id, contract.salt_value
        )
        contract.contractee_signiture = get_hash_value(
            card2.card_id, contract.salt_value
        )
        session.add(contract)
        session.commit()

        yield contract

        session.delete(contract)
        session.delete(payment1)
        session.delete(payment2)
        session.delete(account)
        session.delete(card1)
        session.delete(card2)
        session.delete(user)
        session.commit()


@fixture
def blocks():
    """Creates a Test Block."""

    with Session(ENGINE) as session:
        block = Block()
        session.add(block)
        session.commit()

        block2 = Block()
        session.add(block2)
        session.commit()

        block3 = Block()
        session.add(block3)
        session.commit()

        yield block, block2, block3

        session.delete(block)
        session.delete(block2)
        session.delete(block3)
        session.commit()
