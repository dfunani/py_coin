"""App Module: Testing Application Configuration."""

from datetime import datetime, timedelta

from pytest import raises
from config import AppConfig
from lib.utils.constants.users import DateFormat


def test_app_config_str_repr(app: AppConfig):
    """Test AppConfig Init - Class Representaion."""
    assert str(app).startswith("Application Session: ")


def test_app_config_session_id(app: AppConfig):
    """Test AppConfig Init - Session ID."""
    assert app.session_id is not None


def test_app_config_start_date(app: AppConfig):
    """Test AppConfig Init - Start Date."""
    assert str(app.start_date) < (
        (datetime.now() + timedelta(seconds=2)).strftime(DateFormat.LONG.value)
    ) and str(app.start_date) > (datetime.now() - timedelta(seconds=2)).strftime(
        DateFormat.LONG.value
    )


def test_app_config_start_date_setter(app: AppConfig):
    """Test AppConfig Start Date Setter."""
    with raises(AttributeError):
        app.start_date = datetime.now().strftime(DateFormat.LONG.value)


def test_app_config_end_date(app: AppConfig):
    """Test AppConfig Init - End Date."""
    assert datetime.strptime(
        str(app.end_date), DateFormat.LONG.value
    ) >= datetime.strptime(str(app.start_date), DateFormat.LONG.value)


def test_app_config_end_date_setter(app: AppConfig):
    """Test AppConfig End Date Setter."""
    now = datetime.now()
    setattr(app, "end_date", now)
    assert app.end_date is not None


def test_app_config_salt_value(app: AppConfig):
    """Test AppConfig Init - Salt Value."""
    assert app.salt_value is not None


def test_app_config_salt_value_setter(app: AppConfig):
    """Test AppConfig Salt Value Setter."""
    with raises(AttributeError):
        app.salt_value = "Testing Setter"


def test_app_config_card_length(app: AppConfig):
    """Test AppConfig Init - Salt Value."""
    assert app.card_length is not None


def test_app_config_card_length_setter(app: AppConfig):
    """Test AppConfig Salt Value Setter."""
    with raises(AttributeError):
        app.card_length = 12


def test_app_config_cvv_length(app: AppConfig):
    """Test AppConfig Init - Salt Value."""
    assert app.cvv_length is not None


def test_app_config_cvv_length_setter(app: AppConfig):
    """Test AppConfig Salt Value Setter."""
    with raises(AttributeError):
        app.cvv_length = 5
