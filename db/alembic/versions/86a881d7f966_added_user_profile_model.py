"""Added User Profile Model

Revision ID: 14e2bd506750
Revises: 264138947100
Create Date: 2024-04-08 23:39:03.852511

"""

from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from lib.utils.constants.users import (
    Country,
    Language,
    Occupation,
    Gender,
    Interest,
    Status,
)

# revision identifiers, used by Alembic.
revision: str = "14e2bd506750"
down_revision: Union[str, None] = "264138947100"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_profiles",
        sa.Column(
            "id",
            sa.String(256),
            default=sa.text(f"'{str(uuid4())}'"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "profile_id",
            sa.String(256),
            default=sa.text(f"'{str(uuid4())}'"),
            nullable=False,
        ),
        sa.Column(
            "account_id",
            sa.String(256),
            sa.ForeignKey("users.accounts.id"),
            nullable=False,
        ),
        sa.Column("first_name", sa.String(256), nullable=True),
        sa.Column("last_name", sa.String(256), nullable=True),
        sa.Column("username", sa.String(256), nullable=True),
        sa.Column("date_of_birth", sa.Date, nullable=True),
        sa.Column("gender", sa.Enum(Gender, name="gender"), nullable=True),
        sa.Column("profile_picture", sa.LargeBinary, nullable=True),
        sa.Column("mobile_number", sa.String(256), nullable=True),
        sa.Column(
            "country", sa.Enum(Country, name="account_country"), nullable=True
        ),
        sa.Column(
            "language",
            sa.Enum(Language, name="account_language"),
            default=Language.ENGLISH,
            nullable=True,
        ),
        sa.Column(
            "biography",
            sa.String(256),
            default="This user has not provided a bio yet.",
            nullable=True,
        ),
        sa.Column(
            "occupation",
            sa.Enum(Occupation, name="account_occupation"),
            default=Occupation.OTHER,
            nullable=True,
        ),
        sa.Column(
            "interests",
            sa.ARRAY(sa.Enum(Interest, name="profile_interest")),
            default=[],
            nullable=True,
        ),
        sa.Column(
            "social_media_links",
            sa.JSON,
            default={},
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Enum(Status, name="profile_status"),
            default=Status.NEW,
            nullable=False,
        ),
        sa.Column(
            "created_date",
            sa.DateTime,
            default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_date",
            sa.DateTime,
            default=sa.text("CURRENT_TIMESTAMP"),
            onupdate=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        schema="users",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_profiles", schema="users")
    op.execute("DROP TYPE IF EXISTS gender CASCADE")
    op.execute("DROP TYPE IF EXISTS account_country CASCADE")
    op.execute("DROP TYPE IF EXISTS account_language CASCADE")
    op.execute("DROP TYPE IF EXISTS account_occupation CASCADE")
    op.execute("DROP TYPE IF EXISTS profile_interest CASCADE")
    op.execute("DROP TYPE IF EXISTS profile_status CASCADE")
    # ### end Alembic commands ###
