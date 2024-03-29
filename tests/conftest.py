"""App Module: Testing Configuration."""

from pytest import fixture
from config import AppConfig


@fixture
def app():
    """Initializes the Application Config."""
    return AppConfig()
