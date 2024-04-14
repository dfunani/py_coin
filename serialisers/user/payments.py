"""Users Serialiser Module: Serialiser for Payment Profile Model."""

from typing import Union
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from lib.interfaces.exceptions import (
    FernetError,
    PaymentProfileError,
)
from lib.utils.constants.users import Status
from lib.validators.users import (
    validate_balance,
    validate_description,
    validate_name,
    validate_status,
    validate_username,
)
from models import ENGINE
from models.user.payments import PaymentProfile


class PaymentProfileSerialiser(PaymentProfile):
    """Serialiser for the Payment Profile Model."""

    __MUTABLE_ATTRIBUTES__ = {
        "name": (str, False, validate_username),
        "description": (str, False, validate_description),
        "status": (Status, False, validate_status),
        "balance": (float, False, validate_balance),
    }

    def get_payment_profile(self, payment_id: str) -> Union[dict, PaymentProfileError]:
        """CRUD Operation: Get Payment Profile.

        Args:
            payment_id (str): Public Payment Profile ID.

        Returns:
            dict: Payment Profile Object.
        """

        with Session(ENGINE) as session:
            query = select(PaymentProfile).filter(
                cast(PaymentProfile.payment_id, String) == payment_id
            )
            payment_profile = session.execute(query).scalar_one_or_none()

            if not payment_profile:
                raise PaymentProfileError("Payment Profile not Found.")

            return self.__get_payment_data__(payment_profile)

    def create_payment_profile(
        self, account_id: str, card_id: str
    ) -> Union[str, PaymentProfileError]:
        """CRUD Operation: Add Payment Profile.

        Args:
            account_id (str): Payment Profile's Card ID.
            card_id (str): Payment Profile's Card ID.

        Returns:
            str: Payment Profile Object.
        """

        with Session(ENGINE) as session:
            self.card_id = card_id
            self.account_id = account_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Created.") from exc

            return str(self)

    def update_payment_profile(
        self, private_id: str, **kwargs
    ) -> Union[str, PaymentProfileError]:
        """CRUD Operation: Update Payment Profile.

        Args:
            id (str): Private Payment Profile ID.

        Returns:
            str: Payment Profile Object.
        """

        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, private_id)

            if payment_profile is None:
                raise PaymentProfileError("Payment Profile Not Found.")

            for key, value in kwargs.items():
                if key not in PaymentProfileSerialiser.__MUTABLE_ATTRIBUTES__:
                    raise PaymentProfileError("Invalid User Profile.")

                data_type, nullable, validator = (
                    PaymentProfileSerialiser.__MUTABLE_ATTRIBUTES__[key]
                )
                if not nullable and value is None:
                    raise PaymentProfileError("Invalid Type for this Attribute.")

                if not isinstance(value, data_type) and value is not None:
                    raise PaymentProfileError("Invalid Type for this Attribute.")

                if validator and value is not None and hasattr(validator, "__call__"):
                    value = validator(value)

                setattr(payment_profile, key, value)
            try:
                session.add(payment_profile)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Updated.") from exc

            return str(payment_profile)

    def delete_payment_profile(self, private_id: str) -> Union[str, PaymentProfileError]:
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

            try:
                session.delete(payment_profile)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Deleted.") from exc

            return f"Deleted: {private_id}"

    def __get_payment_data__(self, payment_data: PaymentProfile):
        """ "Gets the User Payment Profile Data.

        Args:
            user_profile (UserProfile): User Payment Profile Object.

        Returns:
            dict: Representation of the User Payment Profile Object.
        """

        return {
            "id": payment_data.id,
            "payment_id": payment_data.payment_id,
            "account_id": payment_data.account_id,
            "card_id": payment_data.card_id,
            "name": payment_data.name,
            "description": payment_data.description,
            "status": payment_data.status,
            "balance": payment_data.balance,
        }
