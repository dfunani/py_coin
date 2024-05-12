"""BlockChain: Contract Model."""

from datetime import datetime
from uuid import uuid4, UUID as uuid

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    LargeBinary,
    String,
    text,
)

from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.users import Status
from models import Base
from models.model import BaseModel


class Contract(Base, BaseModel):
    """Model representing a Contract."""

    __tablename__ = "contracts"
    __table_args__ = ({"schema": "blockchain"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: uuid | Column[uuid] = Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False
    )
    contract_id: str | Column[str] = Column("contract_id", String(256), nullable=False)
    contractor: uuid | Column[uuid] = Column(
        "contractor",
        UUID(as_uuid=True),
        ForeignKey("users.payment_profiles.id"),
        nullable=False,
    )
    contractee: uuid | Column[uuid] = Column(
        "contractee",
        UUID(as_uuid=True),
        ForeignKey("users.payment_profiles.id"),
        nullable=False,
    )
    title: str | Column[str] = Column("title", String(256), nullable=False)
    description: str | Column[str] = Column("description", String(256), nullable=False)
    contract: str | Column[str] = Column("contract", String, nullable=False)
    contract_status: ContractStatus | Column[ContractStatus] = Column(
        "contract_status",
        Enum(ContractStatus, name="contract_status"),
        nullable=False,
        default=ContractStatus.DRAFT,
    )
    contractor_signiture: str | Column[str] = Column(
        "contractor_signiture", String(256), nullable=False
    )
    contractee_signiture: str | Column[str] = Column(
        "contractee_signiture", String(256), nullable=True
    )
    salt_value: uuid | Column[uuid] = Column("salt_value", UUID(as_uuid=True), nullable=False)
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

        self.id = uuid4()
        self.salt_value = uuid4()

    def __str__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Block ID: {str(self.contract_id)}"

    def __repr__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Application Model: {self.__class__.__name__}"
