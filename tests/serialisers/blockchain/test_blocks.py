"""BlockChain: Testing Block Serialiser."""

from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from config import AppConfig
from lib.interfaces.exceptions import BlockError
from lib.utils.constants.blocks import BlockType
from lib.utils.constants.users import Status
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models.blockchain.blocks import Block
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.blockchain.blocks import BlockSerialiser
from models import ENGINE
from tests.conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids, get_id_by_regex


def test_blockserialiser_create(get_blocks):
    """Testing Block Serialiser: Create Block."""

    for block, block1 in zip(get_blocks, list(reversed(get_blocks))):
        with Session(ENGINE) as session:
            block_id = BlockSerialiser().create_block(block.id, block1.id)
            block_id = get_id_by_regex(block_id)
            block_data = (
                session.query(Block).filter(Block.block_id == block_id).one_or_none()
            )
            assert block_data.id is not None
            assert block_data.block_id is not None
            assert block_data.previous_block_id == block.id
            assert block_data.next_block_id == block1.id
            assert block_data.block_type == BlockType.UNIT

            run_test_teardown([block_data], session)


@mark.parametrize(
    "data",
    zip(check_invalid_ids(), list(reversed(check_invalid_ids()))),
)
def test_block_create_invalid(data):
    """Testing Contract Serialiser: Create Contract."""

    with raises((BlockError, DataError, ProgrammingError)):
        BlockSerialiser().create_block(data[0], data[1])


def test_blockileserialiser_get(get_blocks):
    """Testing Block Serialiser: Get Block."""

    for block in get_blocks:
        block_data = BlockSerialiser().get_block(block.block_id)

        assert isinstance(block_data, dict)
        for key in block_data:
            assert key not in block.__EXCLUDE_ATTRIBUTES__


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_blockliser_get_invalid(data):
    """Testing Block Serialiser: Get Block."""

    with raises((BlockError, DataError, ProgrammingError)):
        BlockSerialiser().get_block(data)


def test_blockserialiser_delete(get_blocks):
    """Testing Block Serialiser: Delete Block."""

    for block in get_blocks:
        assert BlockSerialiser().delete_block(block.id).startswith("Deleted: ")


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_blocker_delete_invalid(data):
    """Testing Block Serialiser: Delete Block."""

    with raises((BlockError, DataError, ProgrammingError)):
        BlockSerialiser().delete_block(data)


@mark.parametrize(
    "data",
    list(BlockType),
)
def test_block_update_valid_type(get_blocks, data):
    """Testing Block Serialiser: Update Block."""

    for block in get_blocks:
        with Session(ENGINE) as session:
            BlockSerialiser().update_block(
                block.id,
                block_type=data,
            )
            block_data = session.get(Block, block.id)
            assert block_data.id is not None
            assert block_data.block_type == data

@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_block_update_invalid_type(get_blocks, data):
    """Testing Block Serialiser: Update Block."""

    for block in get_blocks:
        with raises((BlockError, DataError, ProgrammingError)):
            BlockSerialiser().update_block(
                block.id,
                block_type=data,
            )

def test_block_update_valid_id(get_blocks):
    """Testing Block Serialiser: Update Block."""

    for block, block1 in zip(get_blocks, list(reversed(get_blocks))):
        with Session(ENGINE) as session:
            BlockSerialiser().update_block(
                block.id, previous_block_id=block.id, next_block_id=block1.id
            )
            block_data = session.get(Block, block.id)
            assert block_data.id is not None
            assert block_data.block_type == BlockType.UNIT
