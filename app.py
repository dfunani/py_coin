"""_summary_"""

import json
from os import getenv
from random import shuffle
from string import ascii_lowercase, ascii_uppercase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from models import ENGINE
from models.user.accounts import UserAccount
from models.user.users import User

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
                f'{"".join(alphabet[:10])}@{"".join(alphabet[:6])}123',
            )
            fkey = getenv("FERNET_KEY")
            session.add(user)
            session.commit()

            user_data = json.loads(Fernet(fkey).decrypt(user.user_id.encode()))
            account = UserAccount(user_id=user_data.get("id"))
            session.add(account)
            session.commit()

        except IntegrityError as error:
            print(str(error))


if __name__ == "__main__":
    shuffle(alphabet)
    main()
