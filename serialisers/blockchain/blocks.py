"""BlockChain Serialiser Module: Serialiser for Block Model."""

from datetime import datetime
from json import loads
import json
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.interfaces.exceptions import BlockError
from lib.utils.constants.blocks import BlockType
from lib.utils.encryption.cryptography import decrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.blockchain.blocks import Block
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.serialiser import BaseSerialiser


class BlockSerialiser(Block, BaseSerialiser):
    """Serialiser for the Block Model."""

    __SERIALISER_EXCEPTION__ = BlockError
    __MUTABLE_KWARGS__: list[str] = ["block_type", "previous_block_id", "next_block_id"]

    def get_Block(self, block_id: str) -> dict:
        """CRUD Operation: Read Block."""

        with Session(ENGINE) as session:
            query = select(Block).filter(cast(Block.block_id, String) == block_id)
            block = session.execute(query).scalar_one_or_none()

            if not block:
                raise BlockError("Block Not Found.")

            return self.__get_model_data__(block)

    def create_Block(
        self,
        previous_block_id: str,
        next_block_id: str,
    ) -> str:
        """CRUD Operation: Create Block."""

        with Session(ENGINE) as session:
            self.previous_block_id = previous_block_id
            self.next_block_id = next_block_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                print(str(exc))
                raise BlockError("Block Not Created.") from exc

            return str(self)

    def update_block(
        self,
        private_id: str,
        **kwargs,
    ) -> str:
        """CRUD Operation: Update Block."""

        with Session(ENGINE) as session:
            block = session.get(Block, private_id)

            if block is None:
                raise BlockError("Block Not Found.")

            for key, value in kwargs.items():
                if key not in BlockSerialiser.__MUTABLE_KWARGS__:
                    raise BlockError("Invalid Block.")

                value = self.validate_serialiser_kwargs(key, value, model=block)
                setattr(block, key, value)

            try:
                session.add(block)
                session.commit()
            except IntegrityError as exc:
                raise BlockError("Block Not Updated.") from exc

            return str(Block)

    def delete_block(self, private_id: str) -> str:
        """CRUD Operation: Delete Block."""

        with Session(ENGINE) as session:
            block = session.get(Block, private_id)

            if not block:
                raise BlockError("Block Not Found")

            try:
                session.delete(block)
                session.commit()
            except IntegrityError as exc:
                raise BlockError("Block Not Deleted.") from exc

            return f"Deleted: {private_id}"
