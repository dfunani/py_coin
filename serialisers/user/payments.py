"""Payments Serialiser Module: Serialiser for Payment Profile Model."""

from typing import Union
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from lib.interfaces.exceptions import (
    CardValidationError,
    FernetError,
    PaymentProfileError,
)
from lib.utils.constants.users import PaymentStatus, Regex
from models import ENGINE
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card


class PaymentProfileSerialiser(PaymentProfile):
    """
    Serialiser for the Payment Profile Model.

    Args:
        PaymentProfile (class): Access Point to the PaymentProfile Model.
    """

    @classmethod
    def get_payment_profile(
        cls, payment_id: str
    ) -> Union[dict, PaymentProfileError, FernetError]:
        """CRUD Operation: Get Payment Profile.

        Args:
            payment_id (str): Public Payment Profile ID.

        Returns:
            str: Payment Profile Object.
        """
        with Session(ENGINE) as session:
            query = select(PaymentProfile).filter(
                cast(cls.payment_id, String) == payment_id
            )
            payment_profile = session.execute(query).scalar_one_or_none()

            if not payment_profile:
                raise PaymentProfileError("No Payment Profile Found.")

            return cls.__get_payment_data__(payment_profile)

    @classmethod
    def create_payment_profile(
        cls, name: str, description: str, private_card_id: str
    ) -> str:
        """CRUD Operation: Add Payment Profile.

        Args:
            name (str): Payment Profile Name.
            description (str): Payment Profile Description.
            card_id (str): Payment Profile's Card ID.

        Returns:
            dict: Payment Profile Object.
        """
        with Session(ENGINE) as session:
            payment_profile = cls()

            cls.__validate_name__(name)
            cls.__validate_description__(description)
            cls.__validate_card_id__(private_card_id)
            payment_profile.card_id = private_card_id
            payment_profile.name = name
            payment_profile.description = description

            if not payment_profile:
                raise PaymentProfileError("Payment Profile not created.")

            payment_id = str(payment_profile)
            session.add(payment_profile)
            session.commit()

            return payment_id

    @classmethod
    def update_payment_profile(cls, private_id: str, **kwargs) -> str:
        """CRUD Operation: Update Payment Profile.

        Args:
            id (str): Private Payment Profile ID.

        Returns:
            str: Payment Profile Object.
        """
        with Session(ENGINE) as session:
            payment_profile = session.get(cls, private_id)

            if payment_profile is None:
                raise PaymentProfileError("Payment Profile Not Found.")

            for key, value in kwargs.items():
                if key not in ["name", "description", "payment_status"]:
                    raise PaymentProfileError("Invalid attribute to Update.")

                if key == "name":
                    cls.__validate_name__(value)
                    setattr(payment_profile, key, value)
                if key == "description":
                    cls.__validate_description__(value)
                    setattr(payment_profile, key, value)
                if key == "payment_status":
                    cls.__validate_payment_status__(value)
                    setattr(payment_profile, key, value)

            payment_id = str(payment_profile)
            session.add(payment_profile)
            session.commit()

            return payment_id

    @classmethod
    def delete_payment_profile(cls, private_id: str) -> str:
        """CRUD Operation: Delete Payment Profile.

        Args:
            id (str): Private Payment Profile ID.

        Returns:
            str: Payment Profile Object.
        """
        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, private_id)

            if not payment_profile:
                raise PaymentProfileError("Payment Profile Not Found")

            session.delete(payment_profile)
            session.commit()

            return f"Deleted: {private_id}"

    @classmethod
    def __get_payment_data__(cls, payment_data: PaymentProfile):
        cls.__vallidate_payment_profile__(payment_data)
        return {
            "id": payment_data.id,
            "payment_id": payment_data.payment_id,
            # "account_id":  payment_data.
            "card_id": payment_data.card_id,
            "name": payment_data.name,
            "description": payment_data.description,
            "payment_status": payment_data.payment_status,
        }

    @staticmethod
    def __validate_name__(name: str) -> PaymentProfileError:
        """Validates Card Name.

        Raises:
            PaymentProfileError: Invalid Card Name.
        """
        if not isinstance(name, str):
            raise PaymentProfileError("Invalid Type for this Attribute.")
        if not Regex.TITLE.value.match(name):
            raise PaymentProfileError("Invalid Payment Information.")

    @staticmethod
    def __validate_description__(description: str) -> PaymentProfileError:
        """Validates Card Description.

        Raises:
            PaymentProfileError: Invalid Card Description.
        """
        if not isinstance(description, str):
            raise PaymentProfileError("Invalid Type for this Attribute.")
        if not Regex.DESCRIPTION.value.match(description):
            raise PaymentProfileError("Invalid Payment Information.")

    @staticmethod
    def __validate_card_id__(private_card_id: str) -> CardValidationError:
        with Session(ENGINE) as session:
            card = session.get(Card, private_card_id)

            if not card:
                raise CardValidationError("Invalid Card Information.")

    @staticmethod
    def __validate_payment_status__(
        payment_status: PaymentStatus,
    ) -> PaymentProfileError:
        if not isinstance(payment_status, PaymentStatus):
            raise PaymentProfileError("Invalid Type for this Attribute.")
        if payment_status not in [PaymentStatus.ACTIVE, PaymentStatus.DELETED]:
            raise PaymentProfileError("Invalid Payment Information.")

    @staticmethod
    def __vallidate_payment_profile__(
        payment_profile: PaymentProfile,
    ) -> PaymentProfileError:
        """Validates the Private Attribute.

        Args:
            value (str): Valid User Data.

        Raises:
            UserEmailError: Invalid User Data.
        """
        for key in [
            payment_profile.id,
            payment_profile.payment_id,
            #   payment_profile.account_id
            payment_profile.card_id,
            payment_profile.name,
            payment_profile.description,
            payment_profile.payment_status,
        ]:
            if not key:
                raise PaymentProfileError("Invalid Payment Profile Data.")
