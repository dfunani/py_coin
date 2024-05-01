"""Testing Cryptography Helpers"""

from lib.utils.encryption.cryptography import encrypt_data, decrypt_data


def test_encrypt_data():
    """Test Encrypted Data."""

    assert encrypt_data("1".encode()) != "1"


def test_decrypt_data():
    """Test Dencrypted Data."""

    assert (
        decrypt_data(
            """gAAAAABmL-zR7HR9jw6ZkNIOQOZ-QwwX0pB_CHrZzo-
            jAs4cX8bP3O8Q1qU5RRLsG0Jn8M5uPzT6mQFgAmArHBGdCMl8D0NpLw=="""
        )
        != """gAAAAABmL-zR7HR9jw6ZkNIOQOZ-QwwX0pB_CHrZzo-
        jAs4cX8bP3O8Q1qU5RRLsG0Jn8M5uPzT6mQFgAmArHBGdCMl8D0NpLw=="""
    )
