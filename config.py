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
    __CARD_LENGTH__ = 16
    __CVV_LENGTH__ = 3
    __CARD_PREFIX__ = 1991

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


    @property
    def card_length(self) -> int:
        """Applications Card Length.

        Returns:
            str: AppConfig Card Length.
        """
        return self.__CARD_LENGTH__
    
    @property
    def card_prefix(self) -> str:
        """Applications Card Prefix.

        Returns:
            str: AppConfig Card Prefix.
        """
        return self.__CARD_PREFIX__
    
    @property
    def cvv_length(self) -> str:
        """Applications CVV Length.

        Returns:
            str: AppConfig CVV Length.
        """
        return self.__CVV_LENGTH__
    
    