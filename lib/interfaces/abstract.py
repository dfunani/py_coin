"""Interfaces: Base Service."""

class AbstractType:
    """Abstract Service Class."""

    def to_dict(self) -> dict:
        """Returns a Dcitionary Representation."""
        
        return {key: value for key, value in self.__dict__.items() if value}