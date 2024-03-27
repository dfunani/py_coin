from sqlalchemy.orm import Session

from lib.utils.constants.users import AccountPaymentType
from models import ENGINE
from models.user.warehouse import AccountCards


def generate_card_numbers(prefix='', length=20):
    if len(prefix) == length:
        yield prefix
    else:
        for digit in '123456789':
            yield from generate_card_numbers(prefix + digit, length)


    with Session(ENGINE) as session:
            cards = session.query(AccountCards).count()
            if cards != 0:
                session.delete(AccountCards)    
            __generate_cards_numbers(session)

def __generate_cards_numbers(session):
    for prefix in AccountPaymentType:
        for perm in generate_card_numbers(prefix.value[1]):
            if perm[:4] == AccountPaymentType.CHEQUE.value[1]:
                card = AccountCards(perm, AccountPaymentType.CHEQUE)

            if perm[:4] == AccountPaymentType.SAVINGS.value[1]:
                card = AccountCards(perm, AccountPaymentType.SAVINGS)

            if perm[:4] == AccountPaymentType.CREDIT.value[1]:
                card = AccountCards(perm, AccountPaymentType.CREDIT)
                
            session.add(card)
            session.commit()