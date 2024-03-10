# from models import Base


# class UserAccount(Base):
#     __tablename__ = "users"
#     id = Column(
#         "id",
#         Integer,
#         primary_key=True,
#         unique=True,
#         nullable=False,
#         autoincrement="auto",
#     )
#     user_id = Column("user_id", String(256), unique=True, nullable=False)
#     email = Column("email", String(256), unique=True, nullable=False)
#     username = Column("username", String(256), nullable=False)
#     password = Column("password", String(256), nullable=False)
#     __account_creation_date = Column(
#         "account_creation_date", DateTime, server_default=func.now()
#     )
#     account_updated_date = Column(
#         "account_updated_date", DateTime, server_default=func.now(), onupdate=func.now()
#     )
#     __account_status: Column[str] = Column(
#         "account_status",
#         Enum(AccountStatus),
#         server_default=AccountStatus.NEW,
#     )
#     __account_status_updated_date = Column(
#         "account_status_updated_date",
#         DateTime,
#         server_default=func.now(),
#     )
#     last_login_date = Column(DateTime, nullable=True)
#     __role: Column[str] = Column(
#         "role", Enum(AccountRole), nullable=False, server_default=AccountRole.USER
#     )

#     @property
#     def account_creation_date(self):
#         return self.__account_creation_date

#     @property
#     def account_status(self):
#         return self.__account_status

#     @property
#     def account_status_updated_date(self):
#         return self.__account_status_updated_date

#     @property
#     def role(self):
#         return self.__role

#     @property
#     def account_status_updated(self):
#         return self.__account_status_updated

#     @property.setter
#     def account_status(self, value: AccountStatus):
#         if check_account_status(self.__account_status, value):
#             self.__account_status = value
#             self.__account_status_updated_date = datetime.now()
#         else:
#             raise UserAccountError(
#                 f"Invalid Account Status for {self.__account_status} User."
#             )
