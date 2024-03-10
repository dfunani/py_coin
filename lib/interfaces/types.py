"""
Module containing Enumerations for the application.

This module defines various enums that are used
throughout the application to ensure consistency in data representation.

Custom Types:
    - Add any additional custom types here.

Example:
    >>> from types import Gender
    >>> user_gender = Gender.MALE
"""


class UserAccountError(Exception):
    """Custom Error For User Account (Users) Model"""

    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


class UserEmailError(Exception):
    """Custom Error For User Email (Users) Model"""

    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


class UserPasswordError(Exception):
    """Custom Error For User Password (Users) Model"""

    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


class FernetError(Exception):
    """Custom Error For Fernet Keys."""

    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message
