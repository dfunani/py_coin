"""_summary_"""

import json
from random import shuffle
from string import ascii_lowercase, ascii_uppercase
from sys import argv
from sqlalchemy import update
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet

from config import AppConfig
from lib.utils.helpers.users import get_hash_value
from models import ENGINE
from models.user.users import User

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


# def main():
# """_summary_"""
# with Session(ENGINE) as session:
#     try:
#         # Create User
#         user = User(
#             f'{"".join(alphabet[:10])}@{"".join(alphabet[:6])}.co.za',
#             "password@12233",
#         )
#         fkey = getenv("FERNET_KEY")
#         session.add(user)
#         session.commit()


#         # Create Account
#         account = Account(user_id=user_data.get("id"))
#         session.add(account)
#         session.commit()
#         with open('image.webp', 'rb') as image:
#             # Create Profile
#             profile = Profile(
#                 # '76b87e18-481d-4d02-8e1b-38ec9997c740',
#                 "Delali",
#                 "Funani",
#                 "delali_gamers123",
#                 date(199, 12, 31),
#                 "0685642078",
#                 "Hello World from my test profile.",
#                 [ProfileInterest.ANIMALS.value],
#                 {SocialMediaLink.GITHUB: "https://github.com/dfunani", SocialMediaLink.FACEBOOK: ''},
#                 account_id='76b87e18-481d-4d02-8e1b-38ec9997c740',
#                 profile_picture=image.read(),
#                 occupation=AccountOccupation.ACCOUNTANT,
#                 country=AccountCountry.ANTIGUA_AND_BARBUDA,
#                 language=AccountLanguage.AFRIKAANS,
#                 gender=Gender.FEMALE,
#             )
#             profile.account_id='76b87e18-481d-4d02-8e1b-38ec9997c740',
#             profile.gender = Gender.MALE

#             session.add(profile)
#             session.commit()

#     except IntegrityError as error:
#         print(str(error))
#     return 1


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
                    email + password, str(AppConfig().salt_value)
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



def update_user(user_id, **kwargs) -> str:
    with Session(ENGINE) as session:
        # Retrieve the user from the database
        user = session.query(User).filter(User.user_id == user_id).first()

        if user is None:
            return "User not found"

        # Update the password if 'password' key is present in kwargs
        
        # session.execute(update(user))
        for key in kwargs:
            setattr(user, key, kwargs[key])

        # Commit the changes to the database
        session.bulk_update_mappings(user, [kwargs])
        session.commit()
        return 'Updated'



MAPPING = {"create_user": create_user, "get_user": get_user, 'update_user': update_user}


def main(func, **kwargs):
    return func(**kwargs)


if __name__ == "__main__":
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
