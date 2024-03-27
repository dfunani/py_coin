"""warehouse: Add Account Cards

Revision ID: 05579a2b9e48
Revises: 37733f744f98
Create Date: 2024-03-27 17:31:09.412760

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from lib.utils.constants.users import AccountPaymentType, CardStatus


# revision identifiers, used by Alembic.
revision: str = '05579a2b9e48'
down_revision: Union[str, None] = '37733f744f98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'account_cards',
        sa.Column(
        "id",
        sa.String(256),
        default=sa.text(f"'{str(uuid4())}'"),
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column(
        "card_id",
        sa.String(256),
        default=sa.text(f"'{str(uuid4())}'"),
        nullable=False,
    ),
    sa.Column("card_number", sa.String(256), unique=True, nullable=False),
    sa.Column("card_type", sa.Enum(AccountPaymentType), nullable=False),
    sa.Column("card_status", sa.Enum(CardStatus), nullable=False, default=CardStatus.INACTIVE),
    sa.Column(
        "created_date", sa.DateTime, default=sa.text("CURRENT_TIMESTAMP")
    ),
    sa.Column(
        "updated_date",
        sa.DateTime,
        default=sa.text("CURRENT_TIMESTAMP"),
        onupdate=sa.text("CURRENT_TIMESTAMP"),
    ),
    )


def downgrade() -> None:
    op.drop_table('account_cards')
