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
from models.warehouse.users.cards import AccountCards


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
    __id = Column(
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
    )
    account_id: Column[str] = Column(
        "account_id", ForeignKey("accounts.account_id"), nullable=False
    )
    __card_id = Column(
        "card_id",
        String(256),
        foreign_keys=ForeignKey("account_cards.card_id"),
    )
    __cvv_number = Column("cvv_number", String(256), nullable=False)
    __created_date = Column(
        "created_date",
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
        self.__set_card_id()
        self.__set_cvv_number()

    @property
    def card_number(self):
        """Getter for the Card Number Property.

        Returns:
            str: Representation of the Card Number.
        """
        if not self.__card_id:
            raise PaymentInformationError("Invalid Card Information.")
        card_number = self.__get_card_number()
        return (
            card_number[:4] + ("x" * (AppConfig().card_length - 8)) + card_number[-4:]
        )

    @property
    def cvv_number(self):
        """Getter for the CVV Number Property.

        Returns:
            str: Representation of the CVV Number.
        """
        if not self.__cvv_number:
            raise PaymentInformationError("Invalid CVV Number.")
        return "x" * AppConfig().cvv_length

    @property
    def card_type(self):
        """Getter for the Card Type Property.

        Returns:
            str: Representation of the Card Type.
        """
        if not self.__card_id:
            raise PaymentInformationError("Invalid Card Information.")
        return self.__get_card_type()
    
    @property
    def card_information(self):
        salt_value = 

    def __set_card_id(self) -> PaymentInformationError:
        """Sets the Private Attribute."""
        self.__card_id = PaymentInformation.__assign_card_id()

    def __set_cvv_number(self) -> PaymentInformationError:
        """Sets the Private Attribute."""
        cvv_number = "".join([randint(0, 9) for _ in AppConfig().cvv_length])
        if len(cvv_number) != AppConfig().cvv_length:
            raise PaymentInformationError("Invalid Payment Information.")
        self.__cvv_number = cvv_number

    def __get_card_number(self) -> str:
        return self.__get_card_information().card_number

    def __get_card_type(self) -> str:
        return self.__get_card_information().card_type

    def __get_card_information(self) -> Union[CardValidationError, AccountCards]:
        """Gets a Valid Card Information.

        Raises:
            CardValidationError: Invalid Card Information.

        Returns:
            str: Valid Card Information.
        """
        with Session(ENGINE) as session:
            card = (
                session.query(AccountCards)
                .filter(AccountCards.card_id == self.__card_information)
                .one_or_none()
            )
            return card

    @staticmethod
    def __assign_card_id(
        payment_type: AccountPaymentType,
    ) -> Union[CardValidationError, str]:
        """Gets a Valid Card ID.

        Raises:
            CardValidationError: Invalid Card ID.

        Returns:
            str: Valid Card ID.
        """
        with Session(ENGINE) as session:
            card_id = (
                session.query(AccountCards)
                .filter(AccountCards.card_status == CardStatus.INACTIVE)
                .filter(AccountCards.card_type == payment_type)
                .order_by(AccountCards.card_id)
                .first()
                .card_id
            )
            if not card_id:
                raise CardValidationError("No Card Found.")
            return card_id
