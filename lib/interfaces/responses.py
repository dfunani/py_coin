"""Interfaces: Contains Custom Response Types."""


class ServiceResponse:
    """Manages Custom Service Responses."""

    def __init__(self, message: str, status: ServiceStatus) -> None:
        """ServiceResponse Constructor."""

        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String representation of the Service Response."""

        return f"Response: {self.__class__.__name__}"

    def to_dict(self) -> dict[str, str]:
        """Returns Service Response as a Dictionary."""

        return {"message": self.message, "status": self.status}
    
