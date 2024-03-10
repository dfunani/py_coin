# class UserSecurityInformation(Base):
#     __tablename__ = "user_security_information"
#     id = Column(
#         Integer, primary_key=True, unique=True, nullable=False, autoincrement="auto"
#     )
#     email_verification_status = Column(Enum(AcountEmailVerification), server_default=AcountEmailVerification.UNVERIFIED)
#     two_factor_auth_enabled = Column(Boolean, server_default=False)
#     last_two_factor_authenticated = Column(DateTime, nullable=False)
#     profile_visibility_enabled = Column(Boolean, server_default=False)
#     data_sharing_prefences = Column(Boolean, server_default=False)
#     communication_preferences = Column(, server_default=False)
#     location_tracking_enabled = Column(Boolean, server_default=False)
#     sending_cookies_enabled = Column(Boolean, server_default=False)
#     registered_user_devices = Column(UserDevice) 
#     login_history = Column(UserLoginHistory, unique=True, nullable=False)
#     theme_preference = Column(Boolean, unique=True, nullable=False)
    