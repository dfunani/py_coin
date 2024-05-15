"""Interfaces: Contains Custom Types."""

from typing import TypedDict
from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.transactions import TransactionStatus


class TransactionForm(TypedDict):
    """Type Check for Transaction Data."""

    amount: float
    title: str
    description: str
    sender_signiture: str
    receiver_signiture: str
    transaction_status: TransactionStatus


class ContractForm(TypedDict):

    contract: bytes
    title: str
    description: str
    contractor_signiture: str
    contractee_signiture: str
    contract_status: ContractStatus
