# from typing import Union
# from sqlalchemy import Boolean, Column, DateTime, Enum, String, ARRAY

# from lib.utils.constants.users import EmailVerification


# class UserSettings(Base):
#     __tablename__ = "user_settings"

#     id: Union[str, Column[str]] = Column("id", String(256), primary_key=True)
#     settings_id: Union[str, Column[str]] = Column(
#         "settings_id", String(256), nullable=False
#     )
#     email_status = Column(
#         "email_status", Enum(EmailVerification), default=EmailVerification.UNVERIFIED
#     )
#     mfa_enabled = Column("mfa_enabled", Boolean, default=False)
#     mfa_last_used_date = Column("mfa_last_used_date", DateTime, nullable=True)
#     profile_visibility_enabled = Column(
#         "profile_visibility_enabled", Boolean, default=False
#     )
#     data_sharing_preferences = Column(
#         "data_sharing_preferences", ARRAY(Enum()), default=False
#     )
#     communication_preference = Column("communication_preferences", Enum, default=False)
#     location_tracking_enabled = Column(
#         "location_tracking_enabled", Boolean, default=False
#     )
#     cookies_enabled = Column("cookies_enabled", Boolean, default=False)
#     theme_preference = Column("theme_preference", Boolean, unique=True, nullable=False)
