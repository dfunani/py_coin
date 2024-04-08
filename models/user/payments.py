"""Payments Module: Contains User Payment Profile."""

from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    text,
)
from lib.utils.constants.users import PaymentStatus
from models import Base


class PaymentProfile(Base):
    """Model representing a User's Payment Information.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        id (str): Unique Private Profile ID.
        payment_id (str): Unique Public Profile ID.
        account_id (str): Reference to the Associated Account.
        card_id (str): Reference to the Associated Card.
        name (str): Payment Profile Name.
        description (str): Payment Profile Description.

    """

    __tablename__ = "payment_profiles"

    id: Union[str, Column[str]] = Column("id", String(256), primary_key=True)
    payment_id: Union[str, Column[str]] = Column(
        "payment_id", String(256), nullable=False
    )
    # account_id: Column[str] = Column(
    #     "account_id", ForeignKey("accounts.id"), nullable=False
    # )
    card_id: Union[str, Column[str]] = Column(
        "card_id", String(256), ForeignKey("cards.id"), nullable=False
    )
    name: Union[str, Column[str]] = Column(
        "name", String(256), nullable=False, default="New Payment Account."
    )
    description: Union[str, Column[str]] = Column(
        "description",
        String(256),
        nullable=False,
        default="New Payment Account Created for Block Chain Transactions.",
    )
    payment_status: Union[PaymentStatus, Column[PaymentStatus]] = Column(
        "payment_status", Enum(PaymentStatus), default=PaymentStatus.NEW
    )
    created_date: Union[datetime, Column[datetime]] = Column(
        "created_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    updated_date: Union[datetime, Column[datetime]] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __init__(self):
        """User Payment Information Constructor."""
        self.id = str(uuid4())
        self.payment_id = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Payment Profile Object.

        Returns:
            str: Representation of a Payment Profile Object.
        """
        return f"Payment Profile ID: {self.payment_id}"

    def __repr__(self) -> str:
        """String Representation of the Payment Profile Object.

        Returns:
            str: Representation of a Payment Profile Object.
        """
        return f"Application Model: {self.__class__.__name__}"
