"""Controllers Module: User Serialiser Testing Configuration."""

from datetime import date
from pytest import fixture
from sqlalchemy.orm import Session

from config import AppConfig
from lib.utils.constants.users import CardType
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.profiles import UserProfile
from models.user.settings import SettingsProfile
from models.user.users import User
from models.warehouse.cards import Card


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
def email():
    """Test Email for User."""

    return "testing123@test.com"


@fixture
def password():
    """Test Password for User."""

    return "testing@123"


def clear_settings_ids(settings_data: dict) -> dict:
    """Testing Settings Serialiser: Create Settings."""

    del settings_data["id"]
    del settings_data["settings_id"]
    del settings_data["account_id"]
    del settings_data["created_date"]
    del settings_data["updated_date"]
    return settings_data


def clear_profile_ids(profile_data: dict) -> dict:
    del profile_data["id"]
    del profile_data["profile_id"]
    del profile_data["account_id"]
    del profile_data["created_date"]
    del profile_data["updated_date"]
    return profile_data
