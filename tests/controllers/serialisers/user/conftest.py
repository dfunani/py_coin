"""Controllers Module: User Serialiser Testing Configuration."""

from pytest import fixture


@fixture
def user_keys():
    """Testing User Serialiser: Create User."""
    return ["id", "created_date", "updated_date", "email", "password", "salt_value"]
