"""Testing Application Helpers"""

from pytest import raises
from lib.utils.encryption.encoders import get_hash_value


def test_get_hash_value():
    """Get Hash Value"""

    assert len(get_hash_value("1")) == 64
    assert (
        get_hash_value("1")
        == "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"
    )


def test_get_hash_value_salted():
    """Get Hash Value"""

    assert len(get_hash_value("1")) == 64
    assert (
        get_hash_value("1", "1")
        == "4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8"
    )

def test_get_hash_value_invalid_value():
    with raises(ValueError, match="Value must be a String."):
        get_hash_value(1)

def test_get_hash_value_invalid_salt():
    with raises(ValueError, match="Salt must be a String."):
        get_hash_value("1", 1)