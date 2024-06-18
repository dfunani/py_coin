"""Interfaces: Base Service."""

from typing import Any


class AbstractType:
    """Abstract Class, from which all models should inherit."""

    def __init__(self, data: Any):
        """AbstractType Constructor."""

        if data:
            for key, data_item in data.items():
                setattr(self, key, data_item)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"

    def to_dict(self) -> dict:
        """Returns a Dcitionary Representation - Excludes Falsey Values."""

        return {key: value for key, value in self.__dict__.items() if value}
