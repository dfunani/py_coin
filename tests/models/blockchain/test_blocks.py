"""BlockChain Module: Testing the Block Class."""

import base64
from datetime import date
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from lib.utils.constants.blocks import BlockType
from lib.utils.constants.users import CardType, Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.blockchain.blocks import Block
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.users import User
from models.warehouse.cards import Card
from tests.conftest import run_test_teardown


def test_block_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            block = Block("email", "password")
            session.add(block)
            session.commit()


def test_block_valid():
    """Testing a Valid Block Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        block = Block()
        block.block_type = BlockType.CONTRACT
        session.add(block)
        session.commit()

        assert block.id is not None
        assert block.block_type == BlockType.CONTRACT
        assert isinstance(block.to_dict(), dict)

        run_test_teardown(block.id, Block, session)
