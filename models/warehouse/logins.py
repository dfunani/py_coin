"""Logins: Login History Model."""

from uuid import uuid4, UUID as uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, text, Enum

from lib.utils.constants.users import Country, LoginMethod
from models import Base
from models.model import BaseModel


class LoginHistory(Base, BaseModel):
    """Model representing User Login History."""

    __tablename__ = "login_history"
    __table_args__ = ({"schema": "warehouse"},)
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    id: uuid | Column[uuid] = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
    )
    login_id: uuid | Column[uuid] = Column(
        "login_id",
        UUID(as_uuid=True),
        default=text(f"'{str(uuid4())}'"),
        nullable=False,
    )
    user_id: uuid | Column[uuid] = Column(
        "user_id", UUID(as_uuid=True), ForeignKey("users.users.id"), nullable=False
    )
    session_id = Column(
        "session_id",
        UUID(as_uuid=True),
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
    logged_in = Column("logged_in", Boolean, nullable=False, default=True)
    logout_date = Column("logout_date", DateTime, nullable=True)
    authentication_token = Column("authentication_token", String, nullable=True)

    def __init__(self):
        """Login History Object Constructor."""

        self.id = uuid4()
        self.login_id = uuid4()

    def __str__(self) -> str:
        """String Representation of the Login History Object."""

        return f"Login History ID: {str(self.login_id)}"

    def __repr__(self) -> str:
        """String Representation of the Login History Object."""

        return f"Application Model: {self.__class__.__name__}"
