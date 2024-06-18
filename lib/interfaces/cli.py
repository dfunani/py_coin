"""CLI: Command Line Types, Data-Classes and Typed Dicts."""

# from argparse import Namespace
from typing import Optional
from dataclasses import dataclass


@dataclass
class DataArgs:
    """Type Check for CLI Arguments."""

    uuid: Optional[str]
    sender: Optional[str]
    receiver: Optional[str]
    sender_signiture: Optional[str]
    receiver_signiture: Optional[str]
    data: Optional[bool]


@dataclass
class TypeArgs:
    """Type Check for CLI Arguments."""

    transaction: bool
    contract: bool
    block: bool
    user: bool


@dataclass
class Args(TypeArgs, DataArgs):
    """Type Check for CLI Arguments."""

    command: str


class CLIError(Exception):
    """Custom Error For User CLI Errors."""

    def __init__(self, message: str) -> None:
        """CLIError Constructor."""

        super().__init__(message)
        self.message = message
