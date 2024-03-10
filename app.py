"""_summary_"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import ENGINE
from models.user.users import User


def main():
    """_summary_"""
    with Session(ENGINE) as session:
        try:
            user = User("dfunani@test13.com", "password1@12345")
            session.add(user)
            session.commit()
        except IntegrityError as error:
            print(str(error))


if __name__ == "__main__":
    main()
