"""added users model

Revision ID: 72d05c0b25bc
Revises: 
Create Date: 2024-04-02 02:30:57.105818

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from lib.utils.constants.users import UserStatus


# revision identifiers, used by Alembic.
revision: str = "72d05c0b25bc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.String(256),
            nullable=False,
            unique=True,
            primary_key=True,
        ),
        sa.Column("user_id", sa.String(256), nullable=False),
        sa.Column("created_date", sa.DateTime, default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_date",
            sa.DateTime,
            default=sa.text("CURRENT_TIMESTAMP"),
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("email", sa.String(256), unique=True, nullable=False),
        sa.Column("password", sa.String(256), nullable=False),
        sa.Column("user_status", sa.Enum(UserStatus, name="user_status"), nullable=False, default=UserStatus.NEW),
        sa.Column("salt_value", sa.String(256)),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS user_status CASCADE")
    # ### end Alembic commands ###
