"""Users Module: Contains User Model for Mapping Users."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, text
from sqlalchemy.orm import relationship

from lib.utils.constants.users import Role, Status
from models import Base
from models.model import BaseModel
from models.warehouse.logins import LoginHistory


class User(Base, BaseModel):
    """Model representing a User."""

    __tablename__ = "users"
    __table_args__ = ({"schema": "users"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: str | Column[str] = Column(
        "id", String(256), primary_key=True, nullable=False
    )
    user_id: str | Column[str] = Column(
        "user_id", String(256), nullable=False, unique=True
    )
    email: str | Column[str] = Column(
        "email", String(256), unique=True, nullable=False
    )
    password: str | Column[str] = Column("password", String(256), nullable=False)
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
    status: Status | Column[Status] = Column(
        "status", Enum(Status, name="user_status"), nullable=False, default=Status.NEW
    )
    salt_value: str | Column[str] = Column(
        "salt_value", String(256), nullable=False
    )
    role: Role | Column[Role] = Column(
        "role", Enum(Role), nullable=False, default=Role.USER
    )
    login_history = relationship(
        LoginHistory, backref="User", cascade="all, delete-orphan"
    )

    def __init__(self) -> None:
        """User Object Constructor."""

        self.id = str(uuid4())
        self.salt_value = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the User Object."""

        return f"User ID: {self.user_id}"

    def __repr__(self) -> str:
        """String Representation of the User Object."""

        return f"Application Model: {self.__class__.__name__}"
