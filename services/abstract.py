from re import compile as regex_compile

from lib.interfaces.exceptions import UserError


class AbstractService:

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def get_public_id(value: str) -> str:
        """Retrieve the Public ID from String Representation."""

        regex = regex_compile(r"^.*: (.*)$")
        regex_match = regex.match(value)
        matches = regex_match.groups()
        if not matches:
            raise UserError("No Valid Public User ID.")
        return matches[0]
