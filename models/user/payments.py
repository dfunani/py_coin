"""Users: Payments Profile Model."""

from datetime import datetime
from uuid import uuid4, UUID as uuid
from sqlalchemy import UUID, Column, DateTime, Enum, Float, ForeignKey, String, text
from lib.utils.constants.users import Status
from models import Base
from models.model import BaseModel


class PaymentProfile(Base, BaseModel):
    """Model representing a User's Payment Information."""

    __tablename__ = "payment_profiles"
    __table_args__ = ({"schema": "users"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: uuid | Column[uuid] = Column("id", UUID(as_uuid=True), primary_key=True)
    payment_id: uuid | Column[uuid] = Column(
        "payment_id", UUID(as_uuid=True), nullable=False
    )
    account_id: uuid | Column[uuid] = Column(
        "account_id",
        UUID(as_uuid=True),
        ForeignKey("users.accounts.id"),
        nullable=False,
    )
    card_id: uuid | Column[uuid] = Column(
        "card_id",
        UUID(as_uuid=True),
        ForeignKey("warehouse.cards.id"),
        nullable=False,
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

        self.id = uuid4()
        self.payment_id = uuid4()

    def __str__(self) -> str:
        """String Representation of the Payment Profile Object."""

        return f"Payment Profile ID: {str(self.payment_id)}"

    def __repr__(self) -> str:
        """String Representation of the Payment Profile Object."""

        return f"Application Model: {self.__class__.__name__}"
