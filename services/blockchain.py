"""Services: BlockChain Service."""


from lib.interfaces.responses import ServiceResponse
from lib.utils.constants.users import CardType
from models.blockchain.blocks import Block


class BlockChainService:
    """Manages BlockChain Operations."""

    __instance = None

    def __new__(cls, *args, **kwargs) -> "BlockChainService":
        """Singleton Class Constructor."""

        if not cls.__instance:
            cls.CHAIN = []
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    @classmethod
    def add_block_chain(cls, next_block_id: Block) -> ServiceResponse:
        """Appends a Block."""

        pass

    @classmethod
    def create_new_block_block(cls, card_type: CardType) -> ServiceResponse:
        """Creates a New Transaction Block."""

        pass