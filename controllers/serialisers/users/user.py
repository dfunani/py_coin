from models.user.users import User


class UserSerialiser(User):
    @classmethod
    def get_user_data(cls):
        return cls.__email