"""_summary_"""

import json
from os import getenv
from random import shuffle
from string import ascii_lowercase, ascii_uppercase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from lib.utils.helpers.users import get_hash_value
from models import ENGINE
from models.user.accounts import Account
from models.user.users import User
from config import AppConfig

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


def main():
    """_summary_"""
    with Session(ENGINE) as session:
        try:
            user = User(
                f'{"".join(alphabet[:10])}@{"".join(alphabet[:6])}.co.za',
                "password@12233",
            )
            fkey = getenv("FERNET_KEY")
            session.add(user)
            session.commit()

            user_data = json.loads(Fernet(fkey).decrypt(user.user.encode()))
            account = Account(user_id=user_data.get("id"))
            session.add(account)
            session.commit()
            user = (
                session.query(User)
                .where(
                    User.user_id
                    == get_hash_value(
                        "J4hg5QqpMv@J4hg5Q.co.za" + "password@12233",
                        AppConfig().salt_value,
                    )
                )
                .one_or_none()
            )
            user_data = json.loads(Fernet(fkey).decrypt(user.user.encode()))
            if user_data.get("password") != get_hash_value(
                "password@12233", user_data.get("salt_value")
            ):
                return "Never"
            account = (
                session.query(Account)
                .where(Account.user_id == user_data.get("id"))
                .one_or_none()
            )
            print(account)
            print(str(user))
        except IntegrityError as error:
            print(str(error))
        return 1


if __name__ == "__main__":
    shuffle(alphabet)
    print(main())
