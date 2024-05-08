"""BlockChain Module: Testing the Contract Class."""

import base64
from datetime import date
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.users import CardType, Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.blockchain.contracts import Contract
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.users import User
from models.warehouse.cards import Card
from tests.conftest import run_test_teardown


def test_contract_invalid_no_args():
    """Testing Contract With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            contract = Contract()
            session.add(contract)
            session.commit()


def test_contract_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            contract = Contract("email", "password")
            session.add(contract)
            session.commit()


def test_contract_valid(payment, payment2):
    """Testing a Valid Contract Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        with open("test_markdown.md", "r") as file:
            contract = Contract()
            contract.contract_id = get_hash_value(file.read(), contract.salt_value)
            contract.contractor = payment.id
            contract.contractee = payment2.id
            contract.contract = encrypt_data(file.read().encode())
            session.add(contract)
            session.commit()

            assert contract.id is not None
            assert contract.contract_status == ContractStatus.DRAFT
            assert isinstance(contract.to_dict(), dict)

            run_test_teardown(contract.id, Contract, session)
