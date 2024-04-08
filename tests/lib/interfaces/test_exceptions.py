"""Exceptions: Testing Module."""

from lib.interfaces.exceptions import ApplicationError


def test_application_error():
    """Testing Custom Application Error."""
    try:
        raise ApplicationError("Testing ApplicationError.")
    except ApplicationError as e:
        assert str(e) == "Testing ApplicationError."
