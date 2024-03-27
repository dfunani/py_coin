from random import randint
from typing import Union
from uuid import uuid4
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.orm import Session, relationship
from config import AppConfig
from lib.interfaces.exceptions import CardValidationError, PaymentInformationError
from lib.utils.constants.users import AccountPaymentType, CardStatus
from models import ENGINE, Base
from models.user.warehouse import AccountCards


class PaymentInformation(Base):
    """Model representing a User's Payment Information.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        payment_id (str): Unique Public Profile ID.
        account_id (str): Reference to the Associated Account.
        card_number (str):

    """

    __tablename__ = "payment_information"
    id = Column(
        "id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    payment_id = Column(
        "payment_id",
        String(256),
        default=text(f"'{str(uuid4())}'"),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    account_id: Column[str] = Column(
        "account_id", ForeignKey("accounts.account_id"), nullable=False
    )
    __card_information = relationship(
        "card_information",
        String(256),
        foreign_keys=ForeignKey("account_cards.card_id"),
    )
    __created_date = Column(
        "expiration_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    __expiration_date = Column(
        "expiration_date",
        DateTime,
        default=func.date_add(func.now(), func.text("INTERVAL 5 YEAR")),
    )
    __billing_address = Column("billing_address", JSON, nullable=False)
    account_type = Column("account_type", Enum(AccountPaymentType), nullable=False)

    def __init__(self, **kwargs):
        """User Payment Information Constructor."""
        super().__init__(**kwargs)
        self.__set_card_number()
        self.__set_cvv_number()

    @property
    def card_number(self):
        """Getter for the Card Number Property.

        Returns:
            str: Representation of the Card Number.
        """
        if not self.__card_number and len(self.__card_number) != 16:
            raise PaymentInformationError("Invalid Card Information.")
        return "x" * 6 + self.__card_number[-4:]

    def __set_card_number(self) -> PaymentInformationError:
        """Sets the Private Attribute."""
        self.__card_information = PaymentInformation.__get_card_number()
        

    def __set_cvv_number(self) -> PaymentInformationError:
        """Sets the Private Attribute."""
        cvv_number = "".join([randint(0, 9) for _ in AppConfig().cvv_length])
        if len(cvv_number) != AppConfig().cvv_length:
            raise PaymentInformationError("Invalid Payment Information.")
        self.__cvv_number = cvv_number

    @staticmethod
    def __get_card_number() -> Union[CardValidationError, str]:
        """Gets a Valid Card ID.

        Raises:
            CardValidationError: Invalid Card ID.

        Returns:
            str: Valid Card ID.
        """
        with Session(ENGINE) as session:
            card = (
                session.query(AccountCards)
                .filter(AccountCards.card_status == CardStatus.INACTIVE)
                .order_by(AccountCards.card_id)
                .first()
                .card_id
            )
            if not card:
                raise CardValidationError('No card found.')
            return card
