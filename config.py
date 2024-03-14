"""Application's (Global) Configurations and Settings.

Returns:
    AppConfig (Singleton): Singleton Class Managing the 
    Application's Configurations and Settings.

"""

from datetime import datetime
from lib.utils.constants.users import DateFormat
from lib.utils.helpers.users import get_hash_value


class AppConfig:
    """AppConfig Singleton Class."""

    __SALT_VALUE__ = get_hash_value("py coin salt value")

    __START_DATE__ = datetime.now()
    __END_DATE__ = datetime.now()

    @property
    def start_date(self) -> str:
        """App Initialization Datetime.

        Returns:
            str: 2024/03/14 20:05:12
        """
        return AppConfig.__START_DATE__.strftime(DateFormat.LONG.value)

    @property
    def end_date(self) -> str:
        """App Shut Down Datetime.

        Returns:
            str: 2024/03/14 20:05:12
        """
        return AppConfig.__END_DATE__.strftime(DateFormat.LONG.value)

    @end_date.setter
    def end_date(self, value: datetime) -> ValueError:
        """Setter for End Datetime.

        Args:
            value (datetime): New End Date.

        Raises:
            ValueError: New End Date must be datetime.
        """
        if not isinstance(value, datetime):
            raise ValueError("Not a valid Datetime.")
        AppConfig.__END_DATE__ = value

    @property
    def salt_value(self) -> str:
        """Applications SALT VALUE.

        Returns:
            str: AppConfig Salt Value.
        """
        return AppConfig.__SALT_VALUE__
