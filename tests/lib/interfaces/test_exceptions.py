"""Exceptions: Testing Module."""

from lib.interfaces.exceptions import (
    AccountError,
    ApplicationError,
    CardValidationError,
    FernetError,
    LoginHistoryError,
    PaymentProfileError,
    UserError,
    UserProfileError,
)


def test_application_error():
    """Testing Custom Application Error."""

    try:
        raise ApplicationError("Testing ApplicationError.")
    except ApplicationError as e:
        assert str(e) == "Testing ApplicationError."


def test_FernetError():
    """Testing Custom Fernet Error."""

    try:
        raise FernetError("Testing FernetError.")
    except FernetError as e:
        assert str(e) == "Testing FernetError."


def test_UserError():
    """Testing Custom User Error."""

    try:
        raise UserError("Testing UserError.")
    except UserError as e:
        assert str(e) == "Testing UserError."


def test_AccountError():
    """Testing Custom Account Error."""

    try:
        raise AccountError("Testing AccountError.")
    except AccountError as e:
        assert str(e) == "Testing AccountError."


def test_UserProfileError():
    """Testing Custom User Profile Error."""

    try:
        raise UserProfileError("Testing UserProfileError.")
    except UserProfileError as e:
        assert str(e) == "Testing UserProfileError."


def test_PaymentProfileError():
    """Testing Custom Payment Profile Error."""

    try:
        raise PaymentProfileError("Testing PaymentProfileError.")
    except PaymentProfileError as e:
        assert str(e) == "Testing PaymentProfileError."


def test_CardValidationError():
    """Testing Custom Card Validation Error."""

    try:
        raise CardValidationError("Testing CardValidationError.")
    except CardValidationError as e:
        assert str(e) == "Testing CardValidationError."


def test_LoginHistoryError():
    """Testing Custom Login History Error."""

    try:
        raise LoginHistoryError("Testing LoginHistoryError.")
    except LoginHistoryError as e:
        assert str(e) == "Testing LoginHistoryError."
