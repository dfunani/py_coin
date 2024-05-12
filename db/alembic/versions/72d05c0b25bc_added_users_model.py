"""added users model

Revision ID: 72d05c0b25bc
Revises: 
Create Date: 2024-04-02 02:30:57.105818

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from lib.utils.constants.users import Role, Status


# revision identifiers, used by Alembic.
revision: str = "72d05c0b25bc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS users")
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
            unique=True,
            primary_key=True,
        ),
        sa.Column("user_id", sa.String(256), nullable=False, unique=True),
        sa.Column("email", sa.String(256), unique=True, nullable=False),
        sa.Column("password", sa.String(256), nullable=False),
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
        sa.Column(
            "status",
            sa.Enum(Status, name="user_status"),
            nullable=False,
            default=Status.NEW,
        ),
        sa.Column(
            "salt_value",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "role", sa.Enum(Role, name="role"), nullable=False, default=Role.USER
        ),
        schema="users",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users", schema="users")
    op.execute("DROP TYPE IF EXISTS user_status CASCADE")
    op.execute("DROP TYPE IF EXISTS role CASCADE")
    op.execute("DROP SCHEMA IF EXISTS users")
    # ### end Alembic commands ###
