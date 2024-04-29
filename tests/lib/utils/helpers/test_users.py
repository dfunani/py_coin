"""Testing Application Helpers"""

from lib.utils.encryption.encoders import get_hash_value
from lib.utils.constants.users import Status


def test_get_hash_value():
    """Get Hash Value"""
    assert len(get_hash_value(Status.NEW.value)) == 64
