"""Added Contracts Model

Revision ID: 0b0f645bb95f
Revises: 1ee31e72567f
Create Date: 2024-05-08 21:30:25.502110

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from lib.utils.constants.contracts import ContractStatus

# revision identifiers, used by Alembic.
revision: str = "0b0f645bb95f"
down_revision: Union[str, None] = "1ee31e72567f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contracts",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("contract_id", sa.String(256), nullable=False),
        sa.Column(
            "contractor",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("users.payment_profiles.id"),
            nullable=False,
        ),
        sa.Column(
            "contractee",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("users.payment_profiles.id"),
            nullable=False,
        ),
        sa.Column("contract", sa.String, nullable=False),
        sa.Column("title", sa.String(256), nullable=True),
        sa.Column("description", sa.String(256), nullable=True),
        sa.Column("contractor_signiture", sa.String(256), nullable=True),
        sa.Column("contractee_signiture", sa.String(256), nullable=True),
        sa.Column(
            "contract_status",
            sa.Enum(ContractStatus, name="contract_status"),
            nullable=False,
            default=ContractStatus.DRAFT,
        ),
        sa.Column("salt_value", sa.UUID(as_uuid=True), nullable=False),
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
        schema="blockchain",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("contracts", schema="blockchain")
    op.execute("DROP TYPE IF EXISTS contract_status CASCADE")
    # ### end Alembic commands ###
