"""Interfaces: Contains Custom Response Types."""

from lib.utils.constants.responses import ServiceStatus


class ServiceResponse:
    """Manages Custom Service Responses."""

    def __init__(self, message: str, status: ServiceStatus, data: dict = {}) -> None:
        """ServiceResponse Constructor."""

        self.message = message
        self.status = status
        self.data = data

    def __str__(self) -> str:
        """String representation of the Service Response."""

        return f"Response: {self.__class__.__name__}"

    def to_dict(self) -> dict[str, str]:
        """Returns Service Response as a Dictionary."""

        return {"message": self.message, "status": self.status, "data": self.data}
