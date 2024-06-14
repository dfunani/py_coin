from argparse import Namespace
from typing import Optional


class Args(Namespace):
    """Type Check for Transaction Data."""

    command: str
    transaction: bool
    contract: bool
    block: bool
    user: bool
    uuid: Optional[str]
    sender: Optional[str]
    receiver: Optional[str]
    sender_signiture: Optional[str]
    receiver_signiture: Optional[str]
    data: Optional[bool]


class CLIError(Exception):
    """Custom Error For User CLI Errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
