"""Constants: Testing Block Constants Module."""

from pytest import mark

from lib.utils.constants.blocks import BlockType


@mark.parametrize(
    "data",
    list(BlockType),
)
def test_block_status_enum(data):
    """Testing Block Type Enum."""

    assert isinstance(data.value, str)
