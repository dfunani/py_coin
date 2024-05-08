"""Models Module: Contains Transaction Model for Mapping Transactions."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String, text

from lib.utils.constants.transactions import TransactionStatus
from lib.utils.constants.users import Status
from models import Base
from models.model import BaseModel


class Transaction(Base, BaseModel):
    """Model representing a Transaction."""

    __tablename__ = "transactions"
    __table_args__ = ({"schema": "blockchain"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: str | Column[str] = Column("id", String(256), primary_key=True, nullable=False)
    transaction_id: str | Column[str] = Column("transaction_id", String(256), nullable=False)
    sender: str | Column[str] = Column(
        "sender", String(256), ForeignKey("users.payment_profiles.id"), nullable=False
    )
    receiver: str | Column[str] = Column(
        "receiver", String(256), ForeignKey("users.payment_profiles.id"), nullable=False
    )
    amount: str | Column[str] = Column("amount", Float, nullable=False)
    title: str | Column[str] = Column("title", String(256), nullable=True)
    description: str | Column[str] = Column("description", String(256), nullable=True)
    sender_signiture: str | Column[str] = Column("sender_signiture", String(256), nullable=True)
    receiver_signiture: str | Column[str] = Column("receiver_signiture", String(256), nullable=True)
    transaction_status: Status | Column[Status] = Column(
        "transaction_status",
        Enum(TransactionStatus, name="transaction_status"),
        nullable=False,
        default=TransactionStatus.DRAFT,
    )
    salt_value: str | Column[str] = Column("salt_value", String(256), nullable=False)
    created_date: datetime | Column[datetime] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date: datetime | Column[datetime] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    def __init__(self) -> None:
        """Transaction Object Constructor."""

        self.id = str(uuid4())
        self.transaction_id = str(uuid4())
        self.salt_value = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Transaction Object."""

        return f"Transaction ID: {self.transaction_id}"

    def __repr__(self) -> str:
        """String Representation of the Transaction Object."""

        return f"Application Model: {self.__class__.__name__}"
