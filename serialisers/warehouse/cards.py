"""Warehouse Serialiser Module: Serialiser for Card Model."""

from datetime import date, timedelta
from json import dumps
from random import randint
from typing import Union
from sqlalchemy import Column, Date, Enum, String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from lib.interfaces.exceptions import CardValidationError
from lib.utils.constants.users import Status, CardType, DateFormat, Regex
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.users import (
    validate_card_number,
    validate_card_type,
    validate_cvv_number,
    validate_pin,
    validate_status,
)
from models import ENGINE
from models.warehouse.cards import Card


class CardSerialiser(Card):
    """Serialiser for the Card Model."""

    __MAX_RETRIES__ = 3
    __CARD_VALID_YEARS__ = 365 * 5

    def get_card(self, card_id: str) -> Union[str, CardValidationError]:
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
                raise CardValidationError("Card not Found.")

            return self.__get_encrypted_card_data__(card)

    def create_card(
        self, card_type: CardType, pin: str
    ) -> Union[str, CardValidationError]:
        """CRUD Operation: Add Card.

        Args:
            card_type (CardType): Card Type.
            pin (str): Card Pin.

        Returns:
            str: Card Object.
        """

        with Session(ENGINE) as session:
            validate_card_type(card_type)
            self.card_type = card_type
            self.cvv_number = str(self.__get_cvv_number__())
            self.expiration_date = (
                date.today() + timedelta(days=self.__CARD_VALID_YEARS__)
            ).replace(day=1)
            self.card_number = str(self.__get_card_number__())
            self.pin = str(self.__get_pin__(pin))
            self.card_id = str(
                self.get_card_id(
                    str(decrypt_data(str(self.cvv_number))),
                    str(decrypt_data(str(self.card_number))),
                    self.expiration_date,
                )
            )
            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Created.") from exc

            return str(self)

    def update_card(self, private_id: str, **kwargs) -> Union[str, CardValidationError]:
        """CRUD Operation: Update Card.

        Args:
            id (str): Private Card ID.

        Returns:
            str: Card Object.
        """

        with Session(ENGINE) as session:
            card = session.get(Card, private_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            for key, value in kwargs.items():
                if key not in ["status", "pin"]:
                    raise CardValidationError("Invalid attribute to Update.")

                if key == "pin":
                    valid_pin = self.__get_pin__(value)
                    setattr(card, key, valid_pin)
                if key == "status":
                    value = validate_status(value)
                    setattr(card, key, value)

            try:
                session.add(card)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Created.") from exc

            return str(card)

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

            try:
                session.delete(card)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Deleted.") from exc

            return f"Deleted: {private_id}"

    def __get_card_number__(self) -> Union[str, CardValidationError]:
        """Sets the Private Attribute.

        Returns:
            str: Valid Card Number.
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

        validate_card_number(str(card_number))
        return encrypt_data(str(card_number).encode())

    def __get_pin__(self, pin: str) -> Union[str, CardValidationError]:
        """Sets Valid Card Pin.

        Args:
            pin (str): Card Pin.

        Return:
            str: Valid Card Pin.
        """

        validate_pin(pin)
        return str(get_hash_value(pin, self.salt_value))

    def __get_cvv_number__(self) -> Union[str, CardValidationError]:
        """Sets the Private Attribute.

        Returns:
            str: Valid CVV Number.
        """

        cvv_length = AppConfig().cvv_length
        if not isinstance(cvv_length, int):
            raise CardValidationError("Invalid CVV Number Length")
        cvv_number = "".join([str(randint(0, 9)) for _ in range(cvv_length)])
        validate_cvv_number(cvv_number)
        return encrypt_data(cvv_number.encode())

    def __get_encrypted_card_data__(
        self, card: Card
    ) -> Union[str, CardValidationError]:
        """Get Card Information.

        Returns:
            str: Encrypted Card Data.
        """

        data = {
            "id": card.id,
            "card_id": card.card_id,
            "updated_date": card.updated_date.strftime(DateFormat.HYPHEN.value),
            "created_date": card.created_date.strftime(DateFormat.HYPHEN.value),
            "card_number": card.card_number,
            "cvv_number": card.cvv_number,
            "status": card.status.value,
            "card_type": card.card_type.value[0],
            "pin": card.pin,
            "expiration_date": card.expiration_date.strftime(DateFormat.SHORT.value),
            "salt_value": card.salt_value,
        }
        return encrypt_data(dumps(data).encode())

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
                    cast(Card.status, Enum(Status, name="card_status"))
                    != Status.INACTIVE,
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

    @staticmethod
    def get_card_id(
        cvv_number: str,
        card_number: str,
        expiration_date: Union[date, Column[date]],
    ) -> Union[str, CardValidationError]:
        """Sets Valid Card ID.

        args:
            cvv_number (str): CVV Number.
            card_number (str):: Card Number.
            expiration_date (date): Expiration Date.
        """

        salt_value = AppConfig().salt_value
        if not isinstance(salt_value, str):
            raise CardValidationError("Invalid Card Information.")
        return str(
            get_hash_value(
                card_number
                + cvv_number
                + expiration_date.strftime(DateFormat.SHORT.value),
                salt_value,
            )
        )
