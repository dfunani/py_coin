"""Testing Application Validators."""

from pytest import raises
from lib.interfaces.exceptions import ContractError
from lib.utils.constants.contracts import ContractStatus
from lib.validators.contracts import validate_contract_status
from models.blockchain.contracts import Contract


def test_validate_contract_status(contract):
    """Tests Validating Contract Status."""

    assert (
        validate_contract_status(ContractStatus.APPROVED, model=contract)
        == ContractStatus.APPROVED
    )
