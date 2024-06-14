"""Interfaces: Contains Custom Response Types."""

from lib.decorators.utils import validate_function_signature
from lib.interfaces.abstract import AbstractType
from lib.utils.constants.responses import ServiceStatus


class ServiceResponse(AbstractType):
    """Manages Custom Service Responses."""

    @validate_function_signature(True)
    def __init__(self, message: str, status: ServiceStatus, data: dict = {}) -> None:
        """ServiceResponse Constructor."""

        self.message = message
        self.status = status
        self.data = data

    def __str__(self) -> str:
        """String representation of the Service Response."""

        return f"Response: {self.__class__.__name__}"
