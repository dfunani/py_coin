"""Testing the library of types"""

from lib.interfaces.exceptions import (
    AccountError,
    FernetError,
)


def test_user_account_error():
    """Testing the Custo User Account Exception"""
    try:
        raise AccountError("Testing Account Error.")
    except AccountError as error:
        assert str(error) == "Testing Account Error."


def test_fernet_key_error():
    """Testing the Custom Fernet Exception"""

    try:
        raise FernetError("Testing Fernet Error.")
    except FernetError as error:
        assert str(error) == "Testing Fernet Error."
