"""Testing Application Validators."""

from pytest import raises
from lib.interfaces.exceptions import TransactionError
from lib.utils.constants.transactions import TransactionStatus
from lib.validators.transactions import validate_transaction_amount, validate_transaction_status
from models.blockchain.transactions import Transaction


def test_validate_transaction_amount(transaction):
    """Tests Validating Transaction Amount."""

    assert validate_transaction_amount(amount=5.0, model=transaction) == 5.0


def test_validate_transaction_amount_invalid_negative(transaction):
    """Tests Validating Transaction Amount."""

    with raises(TransactionError):
        validate_transaction_amount(amount=-5.0, model=transaction)


def test_validate_transaction_amount_invalid_zero(transaction):
    """Tests Validating Transaction Amount."""

    with raises(TransactionError):
        assert validate_transaction_amount(amount=0.0, model=transaction)

def test_validate_transaction_amount_invalid_type(transaction):
    """Tests Validating Transaction Amount."""

    with raises(TransactionError):
        assert validate_transaction_amount(amount=5, model=transaction)

def test_validate_transaction_amount_invalid_type(transaction):
    """Tests Validating Transaction Amount."""

    with raises(TransactionError):
        assert validate_transaction_amount(amount="0.0", model=transaction)


def test_validate_transaction_status(transaction):
    """Tests Validating Transaction Amount."""

    assert validate_transaction_status(TransactionStatus.APPROVED, model=transaction) == TransactionStatus.APPROVED

