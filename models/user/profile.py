# from sqlalchemy import Column


# class UserProfile(Base):
#     __tablename__ = "user_proffile"
#     id = Column(
#         Integer, primary_key=True, unique=True, nullable=False, autoincrement="auto"
#     )
#     first_name = Column(String(256), nullable=False)
#     last_name = Column(String(256), nullable=False)
#     date_of_birth = Column(Date, nullable=False)
#     gender: Column[str] = Column(Enum(Gender), nullable=False)
#     profile_picture = Column(String(256), nullable=False)
#     __phone_number = Column("phone_number", String(256), nullable=False)
#     country: Column[str] = Column(Enum(AccountCountry), nullable=False)
#     language: Column[str] = Column(
#         Enum(AccountLanguage), default=AccountLanguage.ENGLISH.value
#     )
#     biography = Column(String(256), default="This user has not provided a bio yet.")
#     occupation = Column(Enum(AccountOccupation), default=AccountOccupation.OTHER)
#     interests = Column(ARRAY(String(256)), default=[])
#     social_media_links = Column(JSON, default={})
#     __profile_creation_date = Column("profile_creation_date", DateTime, server_default=func.now())
#     last_updated_date = Column(
#         DateTime, server_default=func.now(), onupdate=func.now()
#     )

#     @property
#     def phone_number(self):
#         return self.__phone_number

#     @property.setter
#     def phone_number(self, value):
#         regex = compile(r"^\+?[0-9]+(?:[ -][0-9]+)*$")
#         if regex.match(self.__phone_number):
#             self.__phone_number = value

#     @property
#     def profile_creation_date(self):
#         return self.__profile_creation_date
