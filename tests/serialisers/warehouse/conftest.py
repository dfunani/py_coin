"""Controllers Module: Card Serialiser Testing Configuration."""

from pytest import fixture


@fixture
def card_keys():
    """Testing Card Serialiser: Create Card."""
    return [
        "id",
        'card_id',
        "updated_date",
        "created_date",
        "card_number",
        "cvv_number",
        "status",
        "card_type",
        "pin",
        "expiration_date",
        "salt_value",
    ]
