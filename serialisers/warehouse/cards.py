"""Cards Serialiser Module: Serialiser for Card Model."""

from datetime import date, timedelta
from json import dumps
from random import randint
from typing import Union
from sqlalchemy import Column, Date, Enum, String, cast, select
from sqlalchemy.orm import Session

from config import AppConfig
from lib.interfaces.exceptions import CardValidationError
from lib.utils.constants.users import CardStatus, CardType, DateFormat, Regex
from lib.utils.helpers.cards import decrypt_data, encrypt_data
from lib.utils.helpers.users import get_hash_value
from models import ENGINE
from models.warehouse.cards import Card


class CardSerialiser(Card):
    """
    Serialiser for the Card Model.

    Args:
        Card (class): Access Point to the Card Model.
    """

    __MAX_RETRIES__ = 3
    __CARD_VALID_YEARS__ = 365 * 5

    @classmethod
    def get_card(cls, card_id: str) -> Union[str, CardValidationError]:
        """CRUD Operation: Get Card.

        Args:
            card_id (str): Public Card ID.

        Returns:
            str: Card Object.
        """
        with Session(ENGINE) as session:
            query = select(Card).filter(cast(Card.card_id, String) == card_id)
            card = session.execute(query).scalar_one_or_none()

            if not card:
                raise CardValidationError("No Card Found.")

            return cls.__get_encrypted_card_data__(card)

    @classmethod
    def create_card(
        cls, card_type: CardType, pin: str
    ) -> Union[str, CardValidationError]:
        """CRUD Operation: Add Card.

        Args:
            card_type (str): Card Type.

        Returns:
            str: Card Object.
        """
        card = cls()

        card.__validate_card_type__(card_type)
        card.card_type = card_type
        card.cvv_number = card.__get_cvv_number__()
        card.expiration_date = (
            date.today() + timedelta(days=cls.__CARD_VALID_YEARS__)
        ).replace(day=1)
        card.card_number = card.__get_card_number__()
        card.pin = card.__get_pin__(pin)
        card.card_id = card.get_card_id(
            decrypt_data(str(card.cvv_number)),
            decrypt_data(str(card.card_number)),
            card.expiration_date,
        )

        with Session(ENGINE) as session:
            card_id = str(card)
            session.add(card)
            session.commit()
            return card_id

    @classmethod
    def update_card(cls, private_id: str, **kwargs) -> Union[str, CardValidationError]:
        """CRUD Operation: Update Card.

        Args:
            id (str): Private Card ID.

        Returns:
            str: Card Object.
        """
        with Session(ENGINE) as session:
            card = session.get(cls, private_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            for key, value in kwargs.items():
                if key not in ["card_status", "pin"]:
                    raise CardValidationError("Invalid attribute to Update.")

                if key == "pin":
                    valid_pin = card.__get_pin__(value)
                    setattr(card, key, valid_pin)
                if key == "card_status":
                    card.__validate_card_status__(value)
                    setattr(card, key, value)

            card_id = str(card)
            session.add(card)
            session.commit()

            return card_id

    @classmethod
    def delete_card(cls, private_id: str) -> Union[str, CardValidationError]:
        """CRUD Operation: Delete Card.

        Args:
            id (str): Private Card ID.

        Returns:
            str: Card Object.
        """
        with Session(ENGINE) as session:
            card = session.get(Card, private_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            session.delete(card)
            session.commit()

            return f"Deleted: {private_id}"

    def __get_card_number__(self) -> Union[str, CardValidationError]:
        """Sets the Private Attribute.

        Returns:
            str: Valid Card Number.

        Raises:
            CardValidationError: Invalid Card Number.
        """
        for retries in range(self.__MAX_RETRIES__):
            try:
                card_number = self.generate_card(
                    self.card_type, self.cvv_number, self.expiration_date
                )
                break
            except CardValidationError:
                if retries == self.__MAX_RETRIES__ - 1:
                    raise

        self.__validate_card_number__(str(card_number))
        return encrypt_data(str(card_number).encode())

    def __get_pin__(self, pin: str) -> Union[str, CardValidationError]:
        """Sets Valid Card Pin.

        Raises:
            CardValidationError: Invalid Card Pin.
        """
        self.__validate_pin__(pin)
        return str(get_hash_value(pin, self.salt_value))

    @staticmethod
    def get_card_id(
        cvv_number: str,
        card_number: str,
        expiration_date: Union[date, Column[date]],
    ) -> Union[str, CardValidationError]:
        """Sets Valid Card ID.

        args:
            - cvv_number (str): CVV Number.
            - card_number (str):: Card Number.
            - expiration_date (date): Expiration Date.

        Raises:
            CardValidationError: Invalid Card ID.
        """
        salt_value = AppConfig().salt_value
        if not isinstance(salt_value, str):
            raise CardValidationError("Invalid Salt Value.")
        return str(
            get_hash_value(
                card_number
                + cvv_number
                + expiration_date.strftime(DateFormat.SHORT.value),
                salt_value,
            )
        )

    @classmethod
    def __get_cvv_number__(cls) -> Union[str, CardValidationError]:
        """Sets the Private Attribute.

        Args:
            value (str): Valid CVV Number.

        Raises:
            CardValidationError: Invalid CVV Number.
        """
        cvv_length = AppConfig().cvv_length
        if not isinstance(cvv_length, int):
            raise CardValidationError("Invalid CVV Number Length")
        cvv_number = "".join([str(randint(0, 9)) for _ in range(cvv_length)])
        CardSerialiser.__validate_cvv_number__(cvv_number)
        return encrypt_data(cvv_number.encode())

    @classmethod
    def __get_encrypted_card_data__(cls, card: Card) -> Union[str, CardValidationError]:
        """Get Card Information.

        Returns:
            str: Encrypted Card Data.
        """
        cls.__vallidate_card__(card)
        data = {
            "id": card.id,
            "card_id": card.card_id,
            "updated_date": card.updated_date.strftime(DateFormat.HYPHEN.value),
            "created_date": card.created_date.strftime(DateFormat.HYPHEN.value),
            "card_number": card.card_number,
            "cvv_number": card.cvv_number,
            "card_status": card.card_status.value,
            "card_type": card.card_type.value[0],
            "pin": card.pin,
            "expiration_date": card.expiration_date.strftime(DateFormat.SHORT.value),
            "salt_value": card.salt_value,
        }
        return encrypt_data(dumps(data).encode())

    @staticmethod
    def __validate_card_type__(card_type: CardType) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            card_type (str): Valid Card Type.

        Raises:
            CardValidationError: Invalid Card Type.
        """
        if not isinstance(card_type, CardType):
            raise CardValidationError("Invalid Type for this Attribute.")

    @staticmethod
    def __validate_card_number__(card_number: str) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Card Number.

        Raises:
            CardValidationError: Invalid Card Number.
        """
        if not isinstance(card_number, str):
            raise CardValidationError("Invalid Type for this Attribute.")
        if len(card_number) != AppConfig().card_length:
            raise CardValidationError("Invalid Card Number.")

    @staticmethod
    def __validate_cvv_number__(value: str) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid CVV.

        Raises:
            CardValidationError: Invalid CVV.
        """
        if not isinstance(value, str):
            raise CardValidationError("Invalid Type for this Attribute.")
        if len(value) != AppConfig().cvv_length:
            raise CardValidationError("Invalid CVV Number.")

    @staticmethod
    def __validate_card_status__(value: CardStatus) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Card Status.

        Raises:
            CardValidationError: Invalid Card Status.
        """
        if not isinstance(value, CardStatus):
            raise CardValidationError("Invalid Type for this Attribute.")
        if value not in [CardStatus.ACTIVE, CardStatus.DELETED]:
            raise CardValidationError("Invalid Card Status.")

    @staticmethod
    def __validate_pin__(pin: str) -> CardValidationError:
        """Validates Card Pin.

        Raises:
            CardValidationError: Invalid Card Pin.
        """
        if not isinstance(pin, str):
            raise CardValidationError("Invalid Type for this Attribute.")
        if not Regex.PIN.value.match(pin):
            raise CardValidationError("Invalid Pin.")

    @staticmethod
    def __vallidate_card__(card: Card) -> CardValidationError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid Card Data.

        Raises:
            CardEmailError: Invalid Card Data.
        """
        for key in [
            card.id,
            card.updated_date,
            card.created_date,
            card.card_number,
            card.cvv_number,
            card.card_status,
            card.card_type,
            card.pin,
            card.expiration_date,
        ]:
            if not key:
                raise CardValidationError("Invalid Card Data.")

    @staticmethod
    def generate_card(
        card_type: Union[CardType, Column[CardType]],
        cvv_number: Union[str, Column[str]],
        expiration_date: Union[date, Column[date]],
    ) -> Union[str, CardValidationError]:
        """Generates a Valid Card.

        Args:
            card_type (str): Valid Card Type.
            cvv_number (str): Valid CVV Number.
            expiration_date (str): Valid Expiration Date.

        Returns:
            str: Valid Card Number.

        Raises:
            CardValidationError: Invalid Card Number.
        """
        card_length = AppConfig().card_length
        if not isinstance(card_length, int):
            raise CardValidationError("Invalid Card Number Length.")
        card_number = "".join(
            [str(randint(0, 9)) for _ in range(card_length - len(card_type.value[1]))]
        )
        card_number = card_type.value[1] + card_number
        with Session(ENGINE) as session:
            cards_count = (
                session.query(Card)
                .filter(
                    cast(Card.card_status, Enum(CardStatus, name="card_status"))
                    != CardStatus.INACTIVE,
                    cast(Card.card_number, String) == card_number,
                    cast(Card.card_type, Enum(CardType, name="card_type")) == card_type,
                    cast(Card.cvv_number, String) == cvv_number,
                    cast(Card.expiration_date, Date) == expiration_date,
                )
                .count()
            )
            if cards_count != 0:
                raise CardValidationError("Card Number Already Exists.")
            return card_number
