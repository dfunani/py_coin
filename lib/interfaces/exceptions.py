"""Interfaces Module: Contains Custom Excptions."""


class ApplicationError(Exception):
    """Custom Error For Application Operations."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class FernetError(Exception):
    """Custom Error For Fernet Keys."""

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


class LoginHistoryError(Exception):
    """Custom Error For User Login History Error."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
