from pytest import fixture
from models import ENGINE
from sqlalchemy.orm import Session

from models.warehouse.users.payments.cards import Card


@fixture
def get_card_number():
    return "999999999"


@fixture
def tear_down():
    with Session(ENGINE) as session:
        
        session.commit() 


def commit_card(card: Card):
    with Session(ENGINE) as session:
        session.add(card)
        session.commit()
