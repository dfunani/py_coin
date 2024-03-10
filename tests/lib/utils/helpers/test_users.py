"""Testing Application Helpers"""

from lib.utils.helpers.users import check_account_status, get_hash_value
from lib.utils.constants.users import AccountStatus

import sys
print(sys.path)

def test_check_account_status():
    """Testing the validity of the new status being provided."""
    assert check_account_status(AccountStatus.NEW, AccountStatus.VERIFIED)


def test_get_hash_value():
    """Get Hash Value"""
    assert len(get_hash_value(AccountStatus.NEW.value)) == 64

