"""added cards warehouse model

Revision ID: af49b667423c
Revises: 72d05c0b25bc
Create Date: 2024-04-02 02:32:46.429097

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from lib.utils.constants.users import CardStatus, CardType

# revision identifiers, used by Alembic.
revision: str = 'af49b667423c'
down_revision: Union[str, None] = '72d05c0b25bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cards',
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
    sa.Column("cvv_number", sa.String(256), nullable=False),
    sa.Column("card_type", sa.Enum(CardType, name=f'card_type_{uuid4}'), nullable=False),
    sa.Column("card_status", sa.Enum(CardStatus, name=f'card_status_{uuid4}'), nullable=False, default=CardStatus.INACTIVE),
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
    op.drop_table('cards')
