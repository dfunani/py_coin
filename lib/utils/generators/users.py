from sqlalchemy.orm import Session

from lib.utils.constants.users import CardType
from models import ENGINE
from models.warehouse.cards import Card


def __generate_card_numbers(prefix='', length=9):
    if len(prefix) == length:
        yield prefix
    else:
        for digit in '123456789':
            yield from __generate_card_numbers(prefix + digit, length)


    

def generate_cards():
    with Session(ENGINE) as session:
        cards = session.query(Card).count()
        if cards != 0:
            print('Deleting Cards...')
            count_deleted = session.query(Card).delete()
            session.commit()
            print(f'Account Cards Deleted: {str(count_deleted)}')
    print('Creating Cards...')
    for prefix in CardType:
        print(f'Started: Creating {prefix.value[0]} Cards.')
        for card_number in __generate_card_numbers():
            card = Card(prefix, card_number)
    
            session.add(card)
            session.commit()
            break
        print(f'Completed: Creating {prefix.value[0]} Cards.')