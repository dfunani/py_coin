"""Serialisers Module: Testing Blocks Serialiser."""

from pytest import raises
from sqlalchemy.orm import Session

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
from tests.conftest import get_id_by_regex, run_test_teardown


def test_blockserialiser_create(blocks):
    """Testing Block Serialiser: Create Block."""

    with Session(ENGINE) as session:
        block = BlockSerialiser().create_Block(
            blocks[0].id, blocks[1].id
        )
        block_id = get_id_by_regex(block)
        block = (
            session.query(Block)
            .filter(Block.block_id == block_id)
            .one_or_none()
        )
        assert block.id is not None
        assert block.block_id is not None
        assert block.previous_block_id == blocks[0].id
        assert block.next_block_id == blocks[1].id
        assert block.block_type == BlockType.UNIT

        run_test_teardown(block.id, Block, session)


def test_blocker_create_invalid():
    """Testing Block Serialiser: Create Block."""

    with Session(ENGINE) as session:
        block = BlockSerialiser().create_Block(
            None, None
        )
        block_id = get_id_by_regex(block)
        block = (
            session.query(Block)
            .filter(Block.block_id == block_id)
            .one_or_none()
        )
        assert block.id is not None
        assert block.block_id is not None
        assert block.previous_block_id is None
        assert block.next_block_id is None
        assert block.block_type == BlockType.UNIT

        run_test_teardown(block.id, Block, session)



def test_blockileserialiser_get(blocks):
    """Testing Block Serialiser: Get Block."""

    block = blocks[0]
    block_data = BlockSerialiser().get_Block(
        block.block_id
    )

    assert isinstance(block_data, dict)
    for key in block_data:
        assert key not in block.__EXCLUDE_ATTRIBUTES__


def test_blockliser_get_invalid():
    """Testing Block Serialiser: Get Block."""

    with raises(BlockError):
        BlockSerialiser().get_Block("block_id")


def test_blockserialiser_delete(blocks):
    """Testing Block Serialiser: Delete Block."""

    BlockSerialiser().delete_block(blocks[0].id)
    BlockSerialiser().delete_block(blocks[1].id)
    BlockSerialiser().delete_block(blocks[2].id)


def test_blocker_delete_invalid():
    """Testing Block Serialiser: Delete Block."""

    with raises(BlockError):
        BlockSerialiser().delete_block("block_data.id")


def test_blockdate_valid_status(blocks):
    """Testing Block Serialiser: Update Block."""

    with Session(ENGINE) as session:
        BlockSerialiser().update_block(
            blocks[0].id,
            next_block_id=blocks[1].id,
            previous_block_id=blocks[2].id,
            block_type=BlockType.CONTRACT,
        )
        block = session.get(Block, blocks[0].id)
        assert block.id is not None
        assert block.block_type == BlockType.CONTRACT


