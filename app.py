"""_summary_"""

from datetime import date
import json
from os import getenv
from random import shuffle
from string import ascii_lowercase, ascii_uppercase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from lib.utils.constants.users import AccountCountry, AccountLanguage, AccountOccupation, AccountPaymentType, Gender, ProfileInterest, SocialMediaLink
# from lib.utils.generators.users import generate_card_numbers
from lib.utils.helpers.users import get_hash_value
from models import ENGINE
from models.user.accounts import Account
from models.user.profiles import Profile
from models.user.users import User
from config import AppConfig
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


def main():
    """_summary_"""
    with Session(ENGINE) as session:
        try:
            # Create User
            user = User(
                f'{"".join(alphabet[:10])}@{"".join(alphabet[:6])}.co.za',
                "password@12233",
            )
            fkey = getenv("FERNET_KEY")
            session.add(user)
            session.commit()

            user_data = json.loads(Fernet(fkey).decrypt(user.user.encode()))

            # Create Account
            account = Account(user_id=user_data.get("id"))
            session.add(account)
            session.commit()
            with open('image.webp', 'rb') as image:
                # Create Profile
                profile = Profile(
                    # '76b87e18-481d-4d02-8e1b-38ec9997c740',
                    "Delali",
                    "Funani",
                    "delali_gamers123",
                    date(199, 12, 31),
                    "0685642078",
                    "Hello World from my test profile.",
                    [ProfileInterest.ANIMALS.value],
                    {SocialMediaLink.GITHUB: "https://github.com/dfunani", SocialMediaLink.FACEBOOK: ''},
                    account_id='76b87e18-481d-4d02-8e1b-38ec9997c740',
                    profile_picture=image.read(),
                    occupation=AccountOccupation.ACCOUNTANT,
                    country=AccountCountry.ANTIGUA_AND_BARBUDA,
                    language=AccountLanguage.AFRIKAANS,
                    gender=Gender.FEMALE,
                )
                profile.account_id='76b87e18-481d-4d02-8e1b-38ec9997c740', 
                profile.gender = Gender.MALE

                session.add(profile)
                session.commit()
            
        except IntegrityError as error:
            print(str(error))
        return 1


if __name__ == "__main__":
    try:
        5/0
    except ZeroDivisionError as e:
        try:
            raise (e.__class__)
        except ZeroDivisionError:
            print('yep')
    # shuffle(alphabet)
    # print(main())
