"""App Module: Testing Configuration."""

from datetime import datetime
from re import Pattern, compile as regex_compile
from typing import Any
from pytest import fixture
from sqlalchemy.orm import Session
from config import AppConfig
from lib.utils.constants.users import CardType, DateFormat
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.users import validate_email, validate_password
from models import ENGINE
from models.user.accounts import Account
from models.user.users import User
from models.warehouse.cards import Card


EMAIL = "testing123@test.com"
PASSWORD = "testing@123"


@fixture
def app() -> AppConfig:
    """Initializes the Application Config."""

    return AppConfig()


@fixture
def email() -> str:
    """Initializes the Test Email."""

    validate_email(EMAIL)
    return EMAIL


@fixture
def password() -> str:
    """Initializes the Test Password."""

    validate_password(PASSWORD)
    return PASSWORD


@fixture
def get_user() -> User:
    """Initializes the Test User."""

    return __generate_user__()


def __generate_user__() -> User:
    """Initializes the Test User."""

    validate_email(EMAIL)
    validate_password(PASSWORD)
    user = User()
    user.email = encrypt_data(EMAIL.encode())
    user.password = encrypt_data(PASSWORD.encode())
    user.user_id = str(
        get_hash_value(str(EMAIL) + PASSWORD, str(AppConfig().salt_value))
    )
    return user


@fixture
def get_account() -> Account:
    """Initializes the Test Account."""

    account = Account()
    user = __generate_user__()

    with Session(ENGINE) as session:
        setup_test_commit(user, session)
        user_id = get_id_by_regex(regex_compile(r"^User ID: (.*)$"), str(user))
        private_id = session.query(User).filter(User.user_id == user_id).one_or_none()
        assert private_id is not None
        account.user_id = str(private_id.id)
    return account


@fixture
def get_card() -> Card:
    """Initializes the Test Card."""

    card = Card()

    card.card_number = "1991123456789"
    card.card_type = CardType.CHEQUE
    card.cvv_number = "123"
    card.expiration_date = datetime.now()
    card.pin = "123456"
    card.card_id = str(get_hash_value("123" + "1991123456789" + datetime.now().strftime(DateFormat.LONG.value)))

    return card


def get_id_by_regex(regex: Pattern, model: str):
    """Initializes the Test Get ID."""

    regex_match = regex.match(model)
    assert regex_match is not None
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    return matches[0]


def setup_test_commit(model: Any, session: Session):
    """Abstraction of the persistence functionality.

    Args:
        model (Model): Model to Persist
        session (Session): Database Session
    """

    session.add(model)
    session.commit()


def run_test_teardown(private_id: str, model: Any, session: Session):
    """Abstraction of the Clearing of the Test Database.

    Args:
        private_id (str): Model Private ID.
        model (Model): Model to Persist
        session (Session): Database Session
    """

    model = session.get(model, private_id)
    session.delete(model)
    session.commit()


@fixture
def name() -> str:
    """Initializes the Test Name."""

    return "testing123"


@fixture
def description() -> str:
    """Initializes the Test Description."""

    return "Longer Description for testing 123."


@fixture
def regex_user():
    """Initializes the Test Regex User."""

    return regex_compile(r"^User ID: (.*)$")


@fixture
def regex_account():
    """Initializes the Test Regex Account."""

    return regex_compile(r"^Account ID: (.*)$")


@fixture
def regex_settings():
    """Initializes the Test Regex Settings."""

    return regex_compile(r"^Settings Profile ID: (.*)$")


@fixture
def regex_user_profile():
    """Initializes the Test Regex User Profile."""

    return regex_compile(r"^User Profile ID: (.*)$")


@fixture
def regex_card():
    """Initializes the Test Regex Card."""

    return regex_compile(r"^Card ID: (.*)$")

@fixture
def regex_payment():
    """Initializes the Test Regex Payment Profile."""

    return regex_compile(r"^Payment Profile ID: (.*)$")
