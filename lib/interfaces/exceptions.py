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


class ApplicationError(Exception):
    """Custom Error For Application Operations."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserError(Exception):
    """Custom Error For Invalid User Operations."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class AccountError(Exception):
    """Custom Error For User Account (Users) Model."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserProfileError(Exception):
    """Custom Error For User Profile Model."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class FernetError(Exception):
    """Custom Error For Fernet Keys."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserIdDataError(Exception):
    """Custom Error For Invalid ID Data."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserSocialMediaLinkError(Exception):
    """Custom Error For Invalid Social Media Links."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class PaymentProfileError(Exception):
    """Custom Error For Invalid Payment Information."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class CardValidationError(Exception):
    """Custom Error For Invalid Card Information."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class SettingsProfileError(Exception):
    """Custom Error For User Settings Error."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
