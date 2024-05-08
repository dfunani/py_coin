"""Models Module: Contains Block Model for Mapping Blocks."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    LargeBinary,
    String,
    text,
)

from lib.utils.constants.blocks import BlockType
from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.users import Status
from models import Base
from models.model import BaseModel


class Block(Base, BaseModel):
    """Model representing a Block."""

    __tablename__ = "blocks"
    __table_args__ = ({"schema": "blockchain"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: str | Column[str] = Column("id", String(256), primary_key=True, nullable=False)
    block_id: str | Column[str] = Column("block_id", String(256), nullable=False)
    transaction_id: str | Column[str] = Column(
        "transaction_id",
        String(256),
        ForeignKey("blockchain.transactions.id"),
        nullable=True,
    )
    contract_id: str | Column[str] = Column(
        "contract_id", String(256), ForeignKey("blockchain.contracts.id"), nullable=True
    )
    previous_block_id: str | Column[str] = Column(
        "previous_block_id", String(256), nullable=True
    )
    next_block_id: str | Column[str] = Column(
        "next_block_id", String(256), nullable=True
    )
    block_type: Status | Column[Status] = Column(
        "block_type",
        Enum(BlockType, name="block_type"),
        nullable=False,
        default=BlockType.UNIT,
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

    def __init__(self) -> None:
        """Contract Object Constructor."""

        self.id = str(uuid4())
        self.block_id = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Block ID: {self.block_id}"

    def __repr__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Application Model: {self.__class__.__name__}"
