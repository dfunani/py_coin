"""Helpers Module: Containing utility functions
for the User Models in the application"""

from hashlib import sha256
from typing import Union

from sqlalchemy import Column
from lib.utils.constants.users import AccountStatus


def check_account_status(
    old_account_status: Union[AccountStatus, Column[AccountStatus]],
    new_account_status: AccountStatus,
) -> bool:
    """Verifies the new account_status provided based on the existing

    Args:
        old_account_status (str): Existing db account status for the user.
        new_account_status (str): New account status for the user.

    Returns:
        bool: Indicates whethere the Account status can be set.
    """
    if not isinstance(old_account_status, AccountStatus):
        return False
    return new_account_status in __get_valid_account_status()[old_account_status]


def get_hash_value(
    value: Union[str, Column[str]], salt_value: Union[str, Column[str]] = ""
) -> Union[str, ValueError]:
    """Generates a new Hash Value.

    Args:
        value (str): Value to Hash.

    Returns:
        str: Hash value as a UTF-8 decoded string.
    Raises:
        ValueError: Invalid Hashing Values.
    """
    if not isinstance(value, str):
        raise ValueError("Value must be a String")

    if not isinstance(salt_value, str):
        raise ValueError("Salt must be a String")

    sha256_value = sha256(salt_value.encode("utf-8"))
    sha256_value.update(value.encode("utf-8"))
    return sha256_value.hexdigest()


def __get_valid_account_status() -> dict[AccountStatus, list]:
    """Defines Account Status Relationships.

    Returns:
        dict: 'old_status': 'Allowable new status'
    """
    return {
        AccountStatus.NEW: [AccountStatus.VERIFIED, AccountStatus.UNVERIFIED],
        AccountStatus.UNVERIFIED: [AccountStatus.VERIFIED, AccountStatus.DELETED],
        AccountStatus.VERIFIED: [
            AccountStatus.ACTIVE,
            AccountStatus.DISABLED,
            AccountStatus.DELETED,
        ],
        AccountStatus.ACTIVE: [AccountStatus.DISABLED, AccountStatus.DELETED],
        AccountStatus.DISABLED: [AccountStatus.ACTIVE, AccountStatus.DELETED],
        AccountStatus.SUSPENDED: [],
        AccountStatus.DELETED: [],
    }
