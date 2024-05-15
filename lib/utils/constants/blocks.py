"""Constants: Contains Constants, Enumerations and Other Static data."""

from enum import Enum


class BlockType(Enum):
    """Enumeration of Transaction Statuses."""

    TRANSACTION = "Transaction Block"
    CONTRACT = "Contract Block"
    UNIT = "Unit Block"
