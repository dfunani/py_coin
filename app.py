"""_summary_"""

import json
from os import getenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from models import ENGINE
from models.user.accounts import UserAccount
from models.user.users import User


def main():
    """_summary_"""
    with Session(ENGINE) as session:
        try:
            user = User("test@df5s.com", "password11313@")
            fkey = getenv("fernet_key")
            session.add(user)
            session.commit()

            user_data = json.loads(Fernet(fkey).decrypt(user.user_id.encode()))
            account = UserAccount(user_id=user_data.get("id"))
            session.add(account)
            session.commit()

        except IntegrityError as error:
            print(str(error))


if __name__ == "__main__":
    main()
