"""Serialisers Module: Testing Contracts Serialiser."""

from pytest import raises
from sqlalchemy.orm import Session

from config import AppConfig
from lib.interfaces.exceptions import ContractError
from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.users import Status
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models.blockchain.contracts import Contract
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.blockchain.contracts import ContractSerialiser
from models import ENGINE
from tests.conftest import get_id_by_regex, run_test_teardown


def test_contractserialiser_create(payment, payment2):
    """Testing Contract Serialiser: Create Contract."""

    with Session(ENGINE) as session:
        contract = ContractSerialiser().create_Contract(
            payment.id, payment2.id, "Testing a string contract, updated."
        )
        contract_id = get_id_by_regex(contract)
        contract = (
            session.query(Contract)
            .filter(Contract.contract_id == contract_id)
            .one_or_none()
        )
        assert contract.id is not None
        assert contract.contract_id is not None
        assert contract.contract is not None

        run_test_teardown(contract.id, Contract, session)


def test_contracter_create_invalid():
    """Testing Contract Serialiser: Create Contract."""

    with raises(ContractError):
        ContractSerialiser().create_Contract("payment.id", "payment.id", "50")


def test_contractileserialiser_get(contract):
    """Testing Contract Serialiser: Get Contract."""

    contract_data = ContractSerialiser().get_Contract(
        contract.contract_id
    )

    assert isinstance(contract_data, dict)
    for key in contract_data:
        assert key not in contract.__EXCLUDE_ATTRIBUTES__


def test_contractliser_get_invalid():
    """Testing Contract Serialiser: Get Contract."""

    with raises(ContractError):
        ContractSerialiser().get_Contract("contract_id")


def test_contractserialiser_delete(contract):
    """Testing Contract Serialiser: Delete Contract."""

    ContractSerialiser().delete_contract(contract.id)


def test_contracter_delete_invalid():
    """Testing Contract Serialiser: Delete Contract."""

    with raises(ContractError):
        ContractSerialiser().delete_contract("contract_data.id")


def test_contractdate_valid_status(contract):
    """Testing Contract Serialiser: Update Contract."""

    with Session(ENGINE) as session:
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.APPROVED,
        )
        contract = session.get(Contract, contract.id)
        assert contract.id is not None
        assert contract.contract_status == ContractStatus.APPROVED


def test_contractdate_valid_status_approved(contract):
    """Testing Contract Serialiser: Update Contract."""

    with Session(ENGINE) as session:
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.APPROVED,
        )
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.ACTIVE,
        )
        contract = session.get(Contract, contract.id)
        assert contract.id is not None
        assert contract.contract_status == ContractStatus.ACTIVE


def test_contractdate_valid_status_approved(contract):
    """Testing Contract Serialiser: Update Contract."""

    with Session(ENGINE) as session:
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.APPROVED,
        )
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.CLOSED,
        )
        contract = session.get(Contract, contract.id)
        assert contract.id is not None
        assert contract.contract_status == ContractStatus.CLOSED


def test_contractdate_valid_status_approved(contract):
    """Testing Contract Serialiser: Update Contract."""

    with Session(ENGINE) as session:
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.REJECTED,
        )
        contract = session.get(Contract, contract.id)
        assert contract.id is not None
        assert contract.contract_status == ContractStatus.REJECTED


def test_contractdate_valid_status_approved(contract):
    """Testing Contract Serialiser: Update Contract."""

    with Session(ENGINE) as session:
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            title="ContractStatusAPPROVED",
            description="Longer Description ContractStatus.APPROVED",
        )
        contract = session.get(Contract, contract.id)
        assert contract.id is not None
        assert contract.contract_status == ContractStatus.DRAFT
        assert contract.title == "ContractStatusAPPROVED"
        assert (
            contract.description == "Longer Description ContractStatus.APPROVED"
        )


def test_contractte_invalid_status(contract):
    """Testing Contract Serialiser: Update Contract."""

    with raises(ContractError):
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.CLOSED,
        )
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.REJECTED,
        )
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.ACTIVE,
        )


def test_contractte_invalid_status_app(contract):
    """Testing Contract Serialiser: Update Contract."""

    with raises(ContractError):
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.APPROVED,
        )
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.REJECTED,
        )


def test_contractte_invalid_status_2(contract):
    """Testing Contract Serialiser: Update Contract."""

    with raises(ContractError):
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract_status=ContractStatus.APPROVED,
        )
        ContractSerialiser().update_contract(
            contract.id,
            contract.contractor_signiture,
            contract.contractee_signiture,
            contract = 55.5
        )

