"""Services: BlockChain Service."""

class UserService:
    """Manages User Operations."""

    __instance = None
    ACTIVE = True

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
