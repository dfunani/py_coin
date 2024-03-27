"""Testing the library of types"""

from lib.interfaces.exceptions import UserAccountError, UserEmailError, UserPasswordError, FernetError


def test_user_account_error():
    """Testing the Custo User Account Exception"""
    try:
        raise UserAccountError("Testing Account Error.")
    except UserAccountError as error:
        assert str(error) == "Testing Account Error."


def test_user_email_error():
    """Testing the Custom User Email Exception"""

    try:
        raise UserEmailError("Testing Email Error.")
    except UserEmailError as error:
        assert str(error) == "Testing Email Error."


def test_user_password_error():
    """Testing the Custom User Password Exception"""

    try:
        raise UserPasswordError("Testing Password Error.")
    except UserPasswordError as error:
        assert str(error) == "Testing Password Error."

def test_fernet_key_error():
    """Testing the Custom Fernet Exception"""

    try:
        raise FernetError("Testing Fernet Error.")
    except FernetError as error:
        assert str(error) == "Testing Fernet Error."
