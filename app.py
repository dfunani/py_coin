"""_summary_"""

import json
from random import shuffle
from string import ascii_lowercase, ascii_uppercase
from sys import argv
import sys
from sqlalchemy import update
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet

from config import AppConfig
from lib.utils.constants.users import CardType
from lib.utils.helpers.users import get_hash_value
from models import ENGINE
from models.user.payments import PaymentProfile
from models.user.users import User
from models.warehouse.users.payments.cards import Card

# from models.warehouse.users.cards import AccountCards

alphabet = [
    *ascii_uppercase,
    *ascii_lowercase,
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]


def create_card():
    card = Card('1991', CardType.CHEQUE)


def create_user() -> str:
    shuffle(alphabet)
    with Session(ENGINE) as session:
        email = f'{"".join(alphabet[:10])}@{"".join(alphabet[:6])}.co.za'
        password = "password@12233"
        user = User(
            email,
            password,
        )
        user_id = str(user)
        session.add(user)
        session.commit()
    return f"{user_id} and Email: {email} with Password: {password}"


def get_user(email, password) -> User:
    with Session(ENGINE) as session:
        user = (
            session.query(User)
            .filter(
                User.user_id
                == get_hash_value(
                    get_hash_value(email, AppConfig().salt_value) + password, str(AppConfig().salt_value)
                )
            )
            .one_or_none()
        )
        if not user:
            return f"No User Found for Email: {email} and Password: {[password]}"
    fernet = AppConfig().fernet
    if not isinstance(fernet, Fernet):
        return f"User Data Error."
    user_data = json.loads(fernet.decrypt(user.user_data.encode()))
    return user_data







MAPPING = {"create_user": create_user, "get_user": get_user, 'update_user': update_user}


def main(func, **kwargs):
    return func(**kwargs)


if __name__ == "__main__":
    # payment = PaymentProfile('Hello World Again.', 'Testing The Hello World Account Payment Profile.', CardType.SAVINGS, '123456')
    # with Session(ENGINE) as session:
    #     session.add(payment)
    #     session.commit()
    # sys.exit()
    if len(argv) > 1:
        func = argv[1]
        args = argv[2:]
    if not func:
        print("No Function to Run.")
    elif func and not args and (func == "--c" or func == "create_user"):
        print(main(MAPPING["create_user"]))
    elif func and len(args) == 2 and (func == "--g" or func == "get_user"):
        print(main(MAPPING["get_user"], email=args[0], password=args[1]))
    elif func and len(args) == 3 and (func == "--u" or func == "update_user"):
        print(main(MAPPING["update_user"], user_id=args[0], **{args[1]: args[2]}))
