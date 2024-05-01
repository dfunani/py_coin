"""Users Serialiser Module: Serialiser for Payment Profile Model."""

from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from lib.interfaces.exceptions import PaymentProfileError
from models import ENGINE
from models.user.payments import PaymentProfile
from serialisers.serialiser import BaseSerialiser


class PaymentProfileSerialiser(PaymentProfile, BaseSerialiser):
    """Serialiser for the Payment Profile Model."""

    __SERIALISER_EXCEPTION__ = PaymentProfileError
    __MUTABLE_KWARGS__: list[str] = [
        "name",
        "description",
        "status",
        "balance",
    ]

    def get_payment_profile(self, payment_id: str) -> dict:
        """CRUD Operation: Get Payment Profile."""

        with Session(ENGINE) as session:
            query = select(PaymentProfile).filter(
                cast(PaymentProfile.payment_id, String) == payment_id
            )
            payment_profile = session.execute(query).scalar_one_or_none()

            if not payment_profile:
                raise PaymentProfileError("Payment Profile not Found.")

            return self.__get_payment_data__(payment_profile)

    def create_payment_profile(self, account_id: str, card_id: str) -> str:
        """CRUD Operation: Add Payment Profile."""

        with Session(ENGINE) as session:
            self.card_id = card_id
            self.account_id = account_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Created.") from exc

            return str(self)

    def update_payment_profile(self, private_id: str, **kwargs) -> str:
        """CRUD Operation: Update Payment Profile."""

        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, private_id)

            if payment_profile is None:
                raise PaymentProfileError("Payment Profile Not Found.")

            for key, value in kwargs.items():
                if key not in PaymentProfileSerialiser.__MUTABLE_KWARGS__:
                    raise PaymentProfileError("Invalid User Profile.")

                value = self.validate_serialiser_kwargs(key, value)
                setattr(payment_profile, key, value)

            try:
                session.add(payment_profile)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Updated.") from exc

            return str(payment_profile)

    def delete_payment_profile(self, private_id: str) -> str:
        """CRUD Operation: Delete Payment Profile."""

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

    def __get_payment_data__(self, payment_data: PaymentProfile) -> dict:
        """ "Gets the User Payment Profile Data."""

        data = payment_data.to_dict()
        return data
