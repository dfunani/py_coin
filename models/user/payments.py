from datetime import datetime, timedelta
import json
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
    column,
    func,
    select,
    text,
)
from lib.utils.constants.users import CardType, Regex, CardStatus
from sqlalchemy.orm import Session, relationship
from config import AppConfig
from lib.interfaces.exceptions import CardValidationError, PaymentProfileError
from lib.utils.helpers.users import get_hash_value
from models import ENGINE, Base
from models.warehouse.users.payments.cards import Card


class PaymentProfile(Base):
    """Model representing a User's Payment Information.

    Args:
        Base (class): SQLAlchemy Base Model,
        from which Application Models are derived.

    Properties:
        payment_id (str): Unique Public Profile ID.
        account_id (str): Reference to the Associated Account.
        card_number (str):

    """

    __tablename__ = "payment_profiles"
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
    )
    # account_id: Column[str] = Column(
    #     "account_id", ForeignKey("accounts.id"), nullable=False
    # )
    __card_id = Column("card_id", String(256), ForeignKey("cards.id"), nullable=False)
    __name = Column("name", String(256), nullable=False, default="New Payment Account.")
    __description = Column(
        "description",
        String(256),
        nullable=False,
        default="New Payment Account Created for Block Chain Transactions.",
    )
    __created_date = Column(
        "created_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    __expiration_date = Column("expiration_date", DateTime)
    __pin = Column("pin", String(256), nullable=False)

    def __init__(self, name: str, description: str, card_type: CardType, pin: str):
        """User Payment Information Constructor.

        Args:
            name (str): Custom Name for the Payment Profile.
            description (str): Short Description for the Payment Profile.
        """
        self.__expiration_date = datetime.now() + timedelta(days=365 * 5)
        self.__set_card_id__(card_type)
        self.__set_name__(name)
        self.__set_deccription__(description)
        self.__set_pin__(pin)

    def __str__(self) -> str:
        """String Representation of the Payment Profile Object.

        Returns:
            str: Representation of a Payment Profile Object.
        """
        return f"Payment ID: {self.payment_id}"

    @property
    def name(self) -> str:
        """Getter for the Payment Profile Name.

        Returns:
            str: Representation of the Payment Profile Name.
        """
        return self.__name

    @property
    def description(self) -> str:
        """Getter for the Payment Profile Description.

        Returns:
            str: Representation of the Payment Profile Description.
        """
        return self.__description

    @property
    def pin(self) -> str:
        """Getter for the Payment Profile Pin.

        Raises:
            UserPasswordError: Representation of the Payment Profile Pin.
        """
        raise PaymentProfileError("Can Not Access Private Attribute: [PIN].")

    @property
    def card_information(self) -> Union[str, PaymentProfileError]:
        """Getter for the Payment Profile Card Information.

        Raises:
            UserPasswordError: Encrypted Card Data.
        """
        data = {
            "card_number": self.__get_card_number__(),
            "ccv_number": self.__get_ccv_number__(),
            "card_pin": self.__pin,
            "card_type": self.__get_card_type__(),
            "expiration_date": self.__expiration_date,
        }
        fernet = AppConfig().fernet
        if not fernet:
            raise PaymentProfileError("Invalid Payment Information.")
        return fernet.decrypt(json.dumps(data).encode()).decode()

    @name.setter
    def name(self, value: str) -> PaymentProfileError:
        """Setter for the Payment Profile Name.

        Returns:
            str: Representation of the Payment Profile Name.
        """
        self.__set_name__(value)

    @description.setter
    def description(self, value: str) -> PaymentProfileError:
        """Setter for the Payment Profile Description.

        Returns:
            str: Representation of the Payment Profile Description.
        """
        self.__set_deccription__(value)

    @pin.setter
    def pin(self, value: str) -> PaymentProfileError:
        """Setter for the Payment Profile Pin.

        Returns:
            str: Representation of the Payment Profile Pin.
        """
        self.__set_pin__(value)

    def __get_card_number__(self) -> str:
        """Gets Valid Card Number.

        Raises:
            CardValidationError: Invalid Card Number.

        Returns:
            str: Valid Card Number.
        """
        return self.__get_card_information__().card_number

    def __get_ccv_number__(self) -> str:
        """Gets Valid CVV Number.

        Raises:
            CardValidationError: Invalid CVV Number.

        Returns:
            str: Valid CVV Number.
        """
        return self.__get_card_information__().cvv_number

    def __get_card_type__(self) -> str:
        """Gets Valid Card Type.

        Raises:
            CardValidationError: Invalid Card Type.

        Returns:
            str: Valid Card Type.
        """
        return self.__get_card_information__().card_type

    def __get_card_information__(self) -> Union[CardValidationError, Card]:
        """Gets Valid Card Information.

        Raises:
            CardValidationError: Invalid Card Information.

        Returns:
            str: Valid Card Information.
        """
        with Session(ENGINE) as session:
            card = (
                session.query(Card).filter(Card.card_id == self.__card_id).one_or_none()
            )
            return card

    def __set_card_id__(self, card_type) -> PaymentProfileError:
        """Sets Valid Card ID.

        Raises:
            PaymentProfileError: Invalid Card ID.
        """
        self.__card_id = self.__assign_card_id__(card_type)

    def __set_name__(self, value: str) -> PaymentProfileError:
        """Sets Valid Card Name.

        Raises:
            PaymentProfileError: Invalid Card Name.
        """
        self.__validate_name__(value)
        self.__name = value

    def __set_deccription__(self, value: str) -> PaymentProfileError:
        """Sets Valid Card Description.

        Raises:
            PaymentProfileError: Invalid Card Description.
        """
        self.__validate_description__(value)
        self.__description = value

    def __set_pin__(self, value: str) -> PaymentProfileError:
        """Sets Valid Card Pin.

        Raises:
            PaymentProfileError: Invalid Card Pin.
        """
        self.__validate_pin__(value)
        self.__pin = str(get_hash_value(value, AppConfig().salt_value))

    def __validate_name__(self, value: str) -> PaymentProfileError:
        """Validates Card Name.

        Raises:
            PaymentProfileError: Invalid Card Name.
        """
        if not isinstance(value, str):
            raise PaymentProfileError("Invalid Type for this Attribute.")
        if not Regex.TITLE.value.match(value):
            raise PaymentProfileError("Invalid Payment Information.")

    def __validate_description__(self, value: str) -> PaymentProfileError:
        """Validates Card Description.

        Raises:
            PaymentProfileError: Invalid Card Description.
        """
        if not isinstance(value, str):
            raise PaymentProfileError("Invalid Type for this Attribute.")
        if not Regex.DESCRIPTION.value.match(value):
            raise PaymentProfileError("Invalid Payment Information.")

    def __validate_pin__(self, value: str) -> PaymentProfileError:
        """Validates Card Pin.

        Raises:
            PaymentProfileError: Invalid Card Pin.
        """
        if not isinstance(value, str):
            raise PaymentProfileError("Invalid Type for this Attribute.")
        if not Regex.PIN.value.match(value):
            raise PaymentProfileError("Invalid Payment Information.")

    @staticmethod
    def __assign_card_id__(
        card_type: CardType,
    ) -> Union[CardValidationError, str]:
        """Assigns a Valid Card ID.

        Raises:
            CardValidationError: Invalid Card ID.

        Returns:
            str: Valid Card ID.
        """
        with Session(ENGINE) as session:
            card_id = (
                session.query(Card)
                .filter(Card.__table__.c.card_type == card_type)
                .filter(Card.__table__.c.card_status == CardStatus.INACTIVE)
                .order_by(Card.__table__.c.card_type)
                .first()
            )
            if not card_id:
                raise CardValidationError("No Card Found.")
            return card_id.id
