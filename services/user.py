"""Services: User Service."""

from typing import Optional
from uuid import UUID
from lib.decorators.utils import validate_function_signature
from lib.interfaces.responses import ServiceResponse
from lib.interfaces.users import UserData
from lib.utils.constants.responses import ServiceStatus
from serialisers.user.accounts import AccountSerialiser
from serialisers.user.profiles import UserProfileSerialiser
from serialisers.user.settings import SettingsProfileSerialiser
from services.abstract import AbstractService


class AbstractService(AbstractService):
    """Manages User Operations."""

    __instance__ = None

    def __new__(cls, *args, **kwargs) -> "AbstractService":
        """Singleton Class Constructor."""

        if not cls.__instance__:
            return super().__new__(cls, *args, **kwargs)
        return cls.__instance__

    @classmethod
    @validate_function_signature(True)
    def create_user_account(cls, user_id: UUID, user_data: UserData):
        response = AccountSerialiser().create_account(user_id)
        account_id = cls.get_public_id(response)
        account = AccountSerialiser().get_account(account_id)

        response = UserProfileSerialiser().create_user_profile(account["id"])
        profile_id = cls.get_public_id(response)
        profile = UserProfileSerialiser().get_user_profile(profile_id)

        response = SettingsProfileSerialiser().create_settings_profile(account_id)
        settings_id = cls.get_public_id(response)
        settings = SettingsProfileSerialiser().get_settings_profile(settings_id)

        updated_data = cls.update_user_account(
            user_data, account["id"], profile["id"], settings["id"]
        )
        account = cls.get_user_account(account["account_id"])
        return ServiceResponse(
            "User Account Successfully Created.",
            ServiceStatus.SUCCESS,
            {"account": account.data, "updated": updated_data},
        )

    @classmethod
    @validate_function_signature(True)
    def update_user_account(
        cls,
        user_data: UserData,
        account_id: Optional[str],
        profile_id: Optional[str],
        settings_id: Optional[str],
    ):
        if account_id:
            AccountSerialiser().update_account(
                account_id, **user_data.account.to_dict()
            )
        if profile_id:
            UserProfileSerialiser().update_user_profile(
                profile_id, **user_data.profile.to_dict()
            )
        if settings_id:
            SettingsProfileSerialiser().update_settings_profile(
                settings_id, **user_data.settings.to_dict()
            )
        return ServiceResponse(
            "User Account Successfully Updated.",
            ServiceStatus.SUCCESS,
            {
                "account": user_data.account.to_dict(),
                "profile": user_data.profile.to_dict(),
                "settings": user_data.settings.to_dict(),
            },
        )

    @classmethod
    @validate_function_signature(True)
    def get_user_account(cls, account_id: str) -> ServiceResponse:
        account = AccountSerialiser().get_account(account_id)
        return ServiceResponse(
            "User Account Successfully Retrieved.", ServiceStatus.SUCCESS, account
        )

    def add_payment_profile():
        pass

    def remove_payment_profile():
        pass
