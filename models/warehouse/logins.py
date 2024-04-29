"""Warehouse Module: Contains Login History Model for Mapping User Login Hostory."""

from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, text, Enum

from lib.utils.constants.users import Country, LoginMethod
from models import Base
from models.model import BaseModel


class LoginHistory(Base, BaseModel):
    """Model representing User Login History."""

    __tablename__ = "login_history"
    __table_args__ = ({"schema": "warehouse"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: str | Column[str] = Column(
        "id",
        String(256),
        primary_key=True,
    )
    login_id: str | Column[str] = Column(
        "login_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
    )
    user_id: str | Column[str] = Column(
        "user_id", String(256), ForeignKey("users.users.id"), nullable=False
    )
    session_id = Column(
        "session_id",
        String(256),
        nullable=True,
    )
    login_date = Column(
        "login_date", DateTime, nullable=False, default=text("CURRENT_TIMESTAMP")
    )
    login_location: Country | Column[Country] = Column(
        "login_location", Enum(Country, name="login_country"), nullable=True
    )
    login_device: str | Column[str] = Column("login_device", String(256), nullable=True)
    login_method: LoginMethod | Column[LoginMethod] = Column(
        "login_method",
        Enum(LoginMethod, name="login_method"),
        nullable=True,
        default=LoginMethod.EMAIL,
    )
    logged_in = Column("logged_in", Boolean, nullable=False, default=False)
    logout_date = Column("logout_date", DateTime, nullable=True)
    authentication_token = Column("authentication_token", String, nullable=True)

    def __init__(self):
        """Login History Object Constructor."""

        self.id = str(uuid4())
        self.login_id = str(uuid4())

    def __str__(self) -> str:
        """String Representation of the Login History Object."""

        return f"Login History ID: {self.login_id}"

    def __repr__(self) -> str:
        """String Representation of the Login History Object."""

        return f"Application Model: {self.__class__.__name__}"
