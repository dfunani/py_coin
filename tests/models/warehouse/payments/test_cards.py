from lib.utils.constants.users import CardType
from models.warehouse.users.payments.cards import Card
from tests.models.warehouse.payments.conftest import commit_card


def test_create_card_cheque(get_card_number, tear_down):
    card = Card(CardType.CHEQUE, get_card_number)
    commit_card(card)


def test_create_card_savings(get_card_number, tear_down):
    card = Card(CardType.SAVINGS, get_card_number)
    commit_card(card)


def test_create_card_credit(get_card_number, tear_down):
    card = Card(CardType.CREDIT, get_card_number)
    commit_card(card)
