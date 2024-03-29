from sqlalchemy.orm import Session

from lib.utils.constants.users import AccountPaymentType
from models import ENGINE
from models.warehouse.users.cards import Cards


def __generate_card_numbers(prefix='', length=13):
    if len(prefix) == length:
        yield prefix
    else:
        for digit in '123456789':
            yield from __generate_card_numbers(prefix + digit, length)


    

def generate_cards():
    with Session(ENGINE) as session:
        cards = session.query(Cards).count()
        if cards != 0:
            print('Deleting Cards...')
            count_deleted = session.query(Cards).delete()
            session.commit()
            print(f'Account Cards Deleted: {str(count_deleted)}')
    print('Creating Cards...')
    for prefix in AccountPaymentType:
        print(f'Started: Creating {prefix.value[0]} Cards.')
        for perm in __generate_card_numbers(prefix.value[1]):
            if perm[:4] == AccountPaymentType.CHEQUE.value[1]:
                card = Cards(perm, AccountPaymentType.CHEQUE)

            if perm[:4] == AccountPaymentType.SAVINGS.value[1]:
                card = Cards(perm, AccountPaymentType.SAVINGS)

            if perm[:4] == AccountPaymentType.CREDIT.value[1]:
                card = Cards(perm, AccountPaymentType.CREDIT)
                
            session.add(card)
            session.commit()
        print(f'Completed: Creating {prefix.value[0]} Cards.')