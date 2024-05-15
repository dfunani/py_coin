from typing import Any, TypedDict

from lib.interfaces.exceptions import ApplicationError


def validate_typed_dict(func) -> dict:
    """Validate a Dictionary against the TypeDict."""

    def wrapper(*args, **kwargs) -> Any:
        for index, data in enumerate(args[1:]):
            data_type = list(func.__annotations__)[index]
            type_dict = func.__annotations__[data_type]
            __validate_typed_dict__(data, type_dict)

        for kwarg, data in kwargs:
            type_dict = func.__annotations__[kwarg]
            __validate_typed_dict__(data, type_dict)

        return func(*args, **kwargs)

    return wrapper


def __validate_typed_dict__(data: dict, typed: dict):
    """Validates the Confirmed Typed Dictionary."""

    if not hasattr(typed, "__annotations__") or not isinstance(data, dict):
        return None

    has_all_keys = all([key in data for key, _ in typed.__annotations__.items()])
    has_all_types = all(
        [isinstance(value, typed.__annotations__[key]) for key, value in data.items()]
    )
    if not has_all_keys or not has_all_types:
        raise ApplicationError("Invalid Typed Dictionary.")
