from json import loads
from cryptography.fernet import Fernet
from config import AppConfig
from lib.interfaces.exceptions import UserError


def encrypt_data(data: bytes) -> str:
    fernet = AppConfig().fernet
    if not isinstance(fernet, Fernet):
        raise UserError("Invalid User Data")
    return fernet.encrypt(data).decode()


def decrypt_data(data: str) -> str:
    fernet = AppConfig().fernet
    if not isinstance(fernet, Fernet):
        raise UserError("Invalid User Data")
    return fernet.decrypt(data.encode()).decode()
