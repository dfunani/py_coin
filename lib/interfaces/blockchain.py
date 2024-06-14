"""Interfaces: Custom Types."""

from lib.decorators.utils import validate_function_signature
from lib.interfaces.abstract import AbstractType
from lib.interfaces.types import ContractDict, TransactionDict


class TransactionData(AbstractType):
    """Type Check for Transaction Data."""

    @validate_function_signature(True)
    def __init__(
        self, receiver_signiture: str, sender_signiture: str, data: TransactionDict
    ):
        self.receiver_signiture = receiver_signiture
        self.sender_signiture = sender_signiture
        self.amount = data['amount']
        self.title = data['title']
        self.description = data['description']
        self.transaction_status = data['transaction_status']


class ContractData(AbstractType):
    """Type Check for Contract Data."""

    @validate_function_signature(True)
    def __init__(
        self, contractor_signiture: str, contractee_signiture: str, data: ContractDict
    ):
        self.contractor_signiture = contractor_signiture
        self.contractee_signiture = contractee_signiture
        self.contract = data['contract']
        self.title = data['title']
        self.description = data['description']
        self.contract_status = data['contract_status']
