"""Controllers Module: User Serialiser Testing Configuration."""

from pytest import fixture


@fixture
def user_keys():
    """Testing User Serialiser: Create User."""
    return [
        "id",
        "user_id",
        "created_date",
        "updated_date",
        "email",
        "password",
        "salt_value",
        "status",
        "role",
    ]


@fixture
def account_keys():
    return [
        "id",
        "account_id",
        "user_id",
        "status",
        "created_date",
        "updated_date",
        "user_profiles",
        "payment_profiles",
        "settings_profile",
    ]


@fixture
def payment_keys():
    """Testing Card Serialiser: Create Card."""
    return [
        "id",
        "payment_id",
        # "account_id"
        "card_id",
        "name",
        "description",
        "payment_status",
    ]


@fixture
def settings_keys():
    return [
        "id",
        "settings_id",
        "account_id",
        "email_status",
        "communication_status",
        "mfa_enabled",
        "mfa_last_used_date",
        "profile_visibility_preference",
        "data_sharing_preferences",
        "communication_preference",
        "location_tracking_enabled",
        "cookies_enabled",
        "theme_preference",
    ]


@fixture
def user_profile_keys():
    return [
        "id",
        "profile_id",
        "account_id",
        "first_name",
        "last_name",
        "username",
        "date_of_birth",
        "gender",
        "profile_picture",
        "mobile_number",
        "country",
        "language",
        "biography",
        "occupation",
        "interests",
        "social_media_links",
        "status",
    ]
