"""Added Accounts Model

Revision ID: af49b667423c
Revises: 72d05c0b25bc
Create Date: 2024-04-09 22:48:13.403029

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from lib.utils.constants.users import Status

# revision identifiers, used by Alembic.
revision: str = "af49b667423c"
down_revision: Union[str, None] = "72d05c0b25bc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            default=sa.text(f"'{str(uuid4())}'"),
            unique=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            "account_id",
            sa.UUID(as_uuid=True),
            default=sa.text(f"'{str(uuid4())}'"),
            unique=True,
        ),
        sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.users.id"), nullable=False),
        sa.Column(
            "status", sa.Enum(Status, name="account_status"), default=Status.NEW, nullable=False
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
    op.drop_table("accounts", schema="users")
    op.execute("DROP TYPE IF EXISTS account_status CASCADE")
    # ### end Alembic commands ###
