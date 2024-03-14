"""Test Module for the AppConfig."""

from datetime import datetime

from pytest import raises
from config import AppConfig
from lib.utils.constants.users import DateFormat


def test_app_config():
    """Test AppConfig Initializes."""
    assert AppConfig().start_date == datetime.now().strftime(DateFormat.LONG.value)
    assert AppConfig().start_date == AppConfig().end_date


def test_app_config_invalid_start_setter():
    """Test AppConfig Raises An Error when Start Date is Updated."""
    with raises(AttributeError):
        AppConfig().start_date = datetime.now()


def test_app_config_valid_end_setter():
    """Test AppConfig Can Update EndDate."""
    appc = AppConfig()
    dt = datetime.now()
    appc.end_date = dt
    assert appc.end_date == dt.strftime(DateFormat.LONG.value)


def test_app_config_valid_salt_setter():
    """Test AppConfig Raises an Error when Salt Value is Updated."""
    appc = AppConfig()
    with raises(AttributeError):
        appc.salt_value = "Fail"


def test_app_config_valid_salt_get():
    """Test AppConfig Salt Value is Consistent between Restarts."""
    appc = AppConfig()
    assert (
        appc.salt_value
        == "8adf9f249e6beb03900af0fd51fd2a3e55034d926357e5ed4b6ecea1ec4796e3"
    )
