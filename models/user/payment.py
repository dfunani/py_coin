# class UserPaymentInformation(Base):
#     __tablename__ = "user_payment_information"
#     id = Column(
#         Integer, primary_key=True, unique=True, nullable=False, autoincrement="auto"
#     )
#     # payment_method = Column(Enum(PaymentMethod), nullable=False)

#     __card_number = Column(String, nullable=False)
#     __expiration_date = Column(String, nullable=False)
#     __cvv = Column(String, nullable=False)
#     __billing_address = Column(String, nullable=False)
#     __account_type = Column(String, nullable=False)
#     __payment_method = Column(String, nullable=False)
#     __amount_balance = Column(Float, server_default=0.0)

#     @property
#     def card_number(self):
#         return self.__card_number
    
#     @property
#     def expiration_date(self):
#         return self.__expiration_date