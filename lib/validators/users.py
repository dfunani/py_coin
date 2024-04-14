"""Validators Module: validations for User related Models."""

from lib.interfaces.exceptions import UserError
from lib.utils.constants.users import Regex, Status


def validate_email(email: str) -> UserError:
    """Validates an Email.

    Args:
        email (str): Valid Email.

    Raises:
        UserError: Invalid Email.
    """
    if not isinstance(email, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.EMAIL.value.match(email):
        raise UserError("Invalid Email.")


def validate_password(password: str) -> UserError:
    """Validates the Password.

    Args:
        value (str): Valid Password.

    Raises:
        UserError: Invalid Password.
    """
    if not isinstance(password, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.PASSWORD.value.match(password):
        raise UserError("Invalid Password.")


def validate_status(value: Status):
    """Validates the User Status.

    Args:
        value (str): Valid User Status.

    Raises:
        UserError: Invalid User Status.
    """
    if not isinstance(value, Status):
        raise UserError("Invalid Type for this Attribute.")
    if value not in [Status.ACTIVE, Status.DELETED]:
        raise UserError("Invalid User Status.")
