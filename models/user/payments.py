"""Users Module: Contains User Payment Profile."""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String, text
from sqlalchemy.orm import relationship
from lib.utils.constants.users import Status
from models import Base
from models.model import BaseModel
from models.warehouse.cards import Card


class PaymentProfile(Base, BaseModel):
    """Model representing a User's Payment Information."""

    __tablename__ = "payment_profiles"
    __table_args__ = ({"schema": "users"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: str | Column[str] = Column("id", String(256), primary_key=True)
    payment_id: str | Column[str] = Column("payment_id", String(256), nullable=False)
    account_id: str | Column[str] = Column(
        "account_id", ForeignKey("users.accounts.id"), nullable=False
    )
    card_id: str | Column[str] = Column(
        "card_id", String(256), ForeignKey("warehouse.cards.id"), nullable=False
    )
    name: str | Column[str] = Column(
        "name", String(256), nullable=False, default="New Payment Account."
    )
    description: str | Column[str] = Column(
        "description",
        String(256),
        nullable=False,
        default="New Payment Account Created for Block Chain Transactions.",
    )
    status: Status | Column[Status] = Column(
        "status", Enum(Status, name="card_status"), default=Status.NEW, nullable=False
    )
    balance: float | Column[float] = Column(
        "balance", Float, default=0.0, nullable=False
    )
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

    def __init__(self):
        """User Payment Information Constructor."""

        self.id = str(uuid4())
        self.payment_id = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Payment Profile Object."""

        return f"Payment Profile ID: {self.payment_id}"

    def __repr__(self) -> str:
        """String Representation of the Payment Profile Object."""

        return f"Application Model: {self.__class__.__name__}"
