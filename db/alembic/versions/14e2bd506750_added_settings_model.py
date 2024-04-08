"""added settings model

Revision ID: 14e2bd506750
Revises: 264138947100
Create Date: 2024-04-08 19:32:35.497804

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    EmailVerification,
    ProfileVisibility,
    Theme,
)

# revision identifiers, used by Alembic.
revision: str = "14e2bd506750"
down_revision: Union[str, None] = "264138947100"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "settings_profiles",
        sa.Column("id", sa.String(256), primary_key=True),
        sa.Column("settings_id", sa.String(256), nullable=False),
        # account_id: Column[str] = Column(
        #     "account_id", ForeignKey("accounts.id"), nullable=False
        # )
        sa.Column(
            "email_status",
            sa.Enum(EmailVerification, name="email_verification"),
            default=EmailVerification.UNVERIFIED,
        ),
        sa.Column("mfa_enabled", sa.Boolean, default=False),
        sa.Column("mfa_last_used_date", sa.DateTime, nullable=True),
        sa.Column(
            "profile_visibility_preference",
            sa.Enum(ProfileVisibility, name="profile_visibility_preference"),
            default=ProfileVisibility.PUBLIC,
        ),
        sa.Column(
            "data_sharing_preferences",
            sa.ARRAY(sa.Enum(DataSharingPreference, name="data_sharing_preference")),
            default=[DataSharingPreference.ACCOUNT],
        ),
        sa.Column(
            "communication_preference",
            sa.Enum(Communication, name="communication"),
            default=Communication.EMAIL,
        ),
        sa.Column("location_tracking_enabled", sa.Boolean, default=False),
        sa.Column("cookies_enabled", sa.Boolean, default=False),
        sa.Column(
            "theme_preference",
            sa.Enum(Theme, name="theme"),
            nullable=False,
            default=Theme.LIGHT,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("settings_profiles")
    op.execute("DROP TYPE IF EXISTS email_verification CASCADE")
    op.execute("DROP TYPE IF EXISTS profile_visibility_preference CASCADE")
    op.execute("DROP TYPE IF EXISTS data_sharing_preference CASCADE")
    op.execute("DROP TYPE IF EXISTS communication CASCADE")
    op.execute("DROP TYPE IF EXISTS theme CASCADE")
    # ### end Alembic commands ###
