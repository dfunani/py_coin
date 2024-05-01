"""Testing Application Config Validators."""

from datetime import datetime, timedelta
from uuid import uuid4

from pytest import raises

from lib.interfaces.exceptions import ApplicationError
from lib.validators.config import (
    validate_salt_value,
    validate_fernet_key,
    validate_start_date,
    validate_session_id,
    validate_card_length,
    validate_cvv_length,
    validate_end_date,
)


def test_validate_salt_value_invalid():
    """Tests Validate SALT_VALUE"""

    with raises(ApplicationError):
        validate_salt_value(1)


def test_validate_salt_value():
    """Tests Validating Salt Value."""

    assert validate_salt_value("salt_value")


def test_validate_fernet_key_invalid():
    """Tests Validate FERNET_KEY"""

    with raises(ApplicationError):
        validate_fernet_key(1)


def test_validate_fernet_key():
    """Tests Validating Fernet Key."""

    assert validate_fernet_key("fernet_key") == "fernet_key"


def test_validate_start_date_invalid():
    """Tests Validate START_DATE"""

    with raises(ApplicationError):
        validate_start_date("test_validate_start_date")


def test_validate_start_date():
    """Tests Validating Start Date."""

    test_now = datetime.now()
    assert validate_start_date(test_now) == test_now


def test_validate_end_date_invalid():
    """Tests Validate END_DATE"""

    with raises(ApplicationError):
        validate_end_date("test_validate_end_date", datetime.now())


def test_validate_end_date_invalid_start():
    """Tests Validate END_DATE"""

    with raises(ApplicationError):
        validate_end_date(datetime.now(), "datetime.now()")


def test_validate_end_date():
    """Tests Validating End Date."""

    test_now = datetime.now() + timedelta(days=1)
    assert validate_end_date(test_now, datetime.now()) == test_now


def test_validate_card_length_invalid():
    """Tests Validate CARD_LENGTH"""

    with raises(ApplicationError):
        validate_card_length("test_validate_card_length")


def test_validate_card_length():
    """Tests Validating Card length."""

    assert validate_card_length(9) == 9


def test_validate_cvv_length_invalid():
    """Tests Validate CVV_LENGTH"""

    with raises(ApplicationError):
        validate_cvv_length("test_validate_cvv_length")


def test_validate_cvv_length():
    """Tests Validating CVV Length."""

    assert validate_cvv_length(3) == 3


def test_validate_session_id_invalid():
    """Tests Validate SESSION_ID"""

    with raises(ApplicationError):
        validate_session_id("test_validate_session_id")


def test_validate_session_id():
    """Tests Validating Session ID."""

    test_uuid = uuid4()
    assert validate_session_id(test_uuid) == test_uuid
