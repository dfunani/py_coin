"""added payment profiles model

Revision ID: 264138947100
Revises: af49b667423c
Create Date: 2024-04-02 18:50:40.030410

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from lib.utils.constants.users import Status

# revision identifiers, used by Alembic.
revision: str = "264138947100"
down_revision: Union[str, None] = "af49b667423c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "payment_profiles",
        sa.Column("id", sa.String(256), primary_key=True),
        sa.Column("payment_id", sa.String(256), nullable=False),
        # account_id: Column[str] = sa.Column(
        #     "account_id", ForeignKey("accounts.id"), nullable=False
        # )
        sa.Column("card_id", sa.String(256), sa.ForeignKey("cards.id"), nullable=False),
        sa.Column(
            "name", sa.String(256), nullable=False, default="New Payment Account."
        ),
        sa.Column(
            "description",
            sa.String(256),
            nullable=False,
            default="New Payment Account Created for Block Chain Transactions.",
        ),
        sa.Column("created_date", sa.DateTime, default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_date",
            sa.DateTime,
            default=sa.text("CURRENT_TIMESTAMP"),
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "payment_status",
            sa.Enum(Status, name="payment_status"),
            default=Status.NEW,
        ),
        sa.Column("balance", sa.Float, default=0.0, nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("payment_profiles")
    op.execute("DROP TYPE IF EXISTS payment_status CASCADE")
    # ### end Alembic commands ###
