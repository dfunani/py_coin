"""Warehouse Module: Contains Card Model for Mapping Cards to Accounts."""

from datetime import date, datetime
from typing import Union
from uuid import uuid4
from sqlalchemy import Column, Date, DateTime, Enum, String, text
from lib.utils.constants.users import CardType, Status
from models import Base
from models.model import BaseModel


class Card(Base, BaseModel):
    """Model representing an Account Card."""

    __tablename__ = "cards"
    __table_args__ = ({"schema": "warehouse"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: str | Column[str] = Column(
        "id",
        String(256),
        primary_key=True,
    )
    card_id: str | Column[str] = Column(
        "card_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
    )
    card_number: str | Column[str] = Column(
        "card_number", String(256), nullable=False
    )
    cvv_number: str | Column[str] = Column(
        "cvv_number", String(256), nullable=False
    )
    card_type: CardType | Column[CardType] = Column(
        "card_type", Enum(CardType, name="card_type"), nullable=False
    )
    status: Status | Column[Status] = Column(
        "status", Enum(Status, name="card_status"), nullable=False, default=Status.NEW
    )
    pin: str | Column[str] = Column("pin", String(256), nullable=False)
    expiration_date: date | Column[date] = Column(
        "expiration_date", Date, nullable=False
    )
    salt_value: str | Column[str] = Column(
        "salt_value", String(256), nullable=False
    )
    created_date: datetime | Column[datetime] = Column(
        "created_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    updated_date: datetime | Column[datetime] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __init__(self):
        """Card Object Constructor."""

        self.id = str(uuid4())
        self.salt_value = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Card Object."""

        return f"Card ID: {self.card_id}"

    def __repr__(self) -> str:
        """String Representation of the Card Object."""

        return f"Application Model: {self.__class__.__name__}"
