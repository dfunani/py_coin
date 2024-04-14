"""Helpers Module: Containing utility functions
for the User Models in the application"""

from hashlib import sha256
from typing import Union

from sqlalchemy import Column


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
