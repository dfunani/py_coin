"""Serialisers Module: Testing Accounts Serialiser."""

from pytest import raises
from sqlalchemy.orm import Session

from lib.interfaces.exceptions import AccountError, SettingsProfileError, UserError
from lib.utils.constants.users import (
    DataSharingPreference,
    ProfileVisibility,
    Status,
    Theme,
    Verification,
)
from models.user.accounts import Account
from models.user.settings import SettingsProfile
from models.user.users import User
from models.warehouse.cards import Card
from serialisers.user.settings import SettingsProfileSerialiser
from models import ENGINE
from tests.conftest import get_id_by_regex, run_test_teardown, setup_test_commit
from tests.serialisers.user.conftest import clear_settings_ids


def test_paymentprofileserialiser_create(get_account, regex_account, regex_settings):
    """Testing Account Serialiser: Create Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, str(settings))
        settings = (
            session.query(SettingsProfile)
            .filter(SettingsProfile.settings_id == settings_id)
            .one_or_none()
        )

        run_test_teardown(settings.id, SettingsProfile, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_create_invalid():
    """Testing Account Serialiser: Create Account."""

    with raises(SettingsProfileError):
        SettingsProfileSerialiser().create_settings_profile("user.id")


def test_paymentprofileserialiser_get(get_account, regex_settings, settings_keys):
    """Testing Account Serialiser: Get Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)
        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        assert isinstance(settings_data, dict)
        for key in settings_keys:
            assert key in settings_data

        for key in settings_data:
            assert key in settings_keys

        run_test_teardown(settings_data.get("id"), SettingsProfile, session)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_get_invalid():
    """Testing Account Serialiser: Get Account."""

    with raises(SettingsProfileError):
        SettingsProfileSerialiser().get_settings_profile("account_id")


def test_paymentprofileserialiser_delete(get_account, regex_settings):
    """Testing Account Serialiser: Delete Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        SettingsProfileSerialiser().delete_settings_profile(settings_data.get("id"))
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_delete_invalid():
    """Testing Account Serialiser: Delete Account."""

    with raises(SettingsProfileError):
        SettingsProfileSerialiser().delete_settings_profile("account_data.id")


def test_paymentprofileserialiser_update_valid_profile_visibility_preference(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)
        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        settings_data["profile_visibility_preference"] = ProfileVisibility.PRIVATE

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        SettingsProfileSerialiser().update_settings_profile(
            settings_private_id, **settings_data
        )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_profile_visibility_preference(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
        settings_data["profile_visibility_preference"] = ProfileVisibility.ADMIN

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_profile_visibility_preference_type(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)
        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        settings_data["profile_visibility_preference"] = "ProfileVisibility.ADMIN"

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_communication_status(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        settings_data["communication_status"] = Verification.FAILED

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        SettingsProfileSerialiser().update_settings_profile(
            settings_private_id, **settings_data
        )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_communication_status(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
        settings_data["communication_status"] = "ProfileVisibility.ADMIN"

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_email_status(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        settings_data["email_status"] = Verification.VERIFIED

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        SettingsProfileSerialiser().update_settings_profile(
            settings_private_id, **settings_data
        )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_email_status(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
        settings_data["email_status"] = "ProfileVisibility.ADMIN"

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_mfa_enabled(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        settings_data["mfa_enabled"] = True

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        SettingsProfileSerialiser().update_settings_profile(
            settings_private_id, **settings_data
        )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_mfa_enabled(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
        settings_data["mfa_enabled"] = "ProfileVisibility.ADMIN"

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_data_sharing_preferences(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        settings_data["data_sharing_preferences"] = [
            DataSharingPreference.PROFILE,
            DataSharingPreference.SETTINGS,
        ]

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        SettingsProfileSerialiser().update_settings_profile(
            settings_private_id, **settings_data
        )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_data_sharing_preferences(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
        settings_data["data_sharing_preferences"] = "ProfileVisibility.ADMIN"

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_data_sharing_preferences_list(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
        settings_data["data_sharing_preferences"] = ["ProfileVisibility.ADMIN"]

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_valid_bool(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)

        settings_data["location_tracking_enabled"] = True
        settings_data["cookies_enabled"] = True
        settings_data["theme_preference"] = Theme.GREEN

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        SettingsProfileSerialiser().update_settings_profile(
            settings_private_id, **settings_data
        )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)


def test_paymentprofileserialiser_update_invalid_bool(
    get_account, regex_account, regex_settings
):
    """Testing Account Serialiser: Update Account."""

    with Session(ENGINE) as session:
        setup_test_commit(get_account, session)

        settings = SettingsProfileSerialiser().create_settings_profile(get_account.id)
        settings_id = get_id_by_regex(regex_settings, settings)

        settings_data = SettingsProfileSerialiser().get_settings_profile(settings_id)
        settings_data["location_tracking_enabled"] = "True"
        settings_data["cookies_enabled"] = "True"
        settings_data["theme_preference"] = "True"

        settings_private_id = settings_data["id"]
        settings_data = clear_settings_ids(settings_data)
        with raises(SettingsProfileError):
            SettingsProfileSerialiser().update_settings_profile(
                settings_private_id, **settings_data
            )

        SettingsProfileSerialiser().delete_settings_profile(settings_private_id)
        run_test_teardown(get_account.id, Account, session)
        run_test_teardown(get_account.user_id, User, session)
