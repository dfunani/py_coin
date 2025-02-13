"""Added BlockType Trigger

Revision ID: 83a5ef5c0629
Revises: 60eee6a74437
Create Date: 2024-05-14 20:43:40.631676

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "83a5ef5c0629"
down_revision: Union[str, None] = "60eee6a74437"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the SQL commands
trigger_function_sql = """
    CREATE OR REPLACE FUNCTION set_block_type_enum()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.transaction_id IS NOT NULL AND NEW.contract_id IS NOT NULL THEN
            RAISE EXCEPTION 'Invalid combination of transaction_id and contract_id';
        END IF;
        IF NEW.contract_id IS NOT NULL THEN
            NEW.block_type := 'CONTRACT';
        ELSIF NEW.transaction_id IS NOT NULL THEN
            NEW.block_type := 'TRANSACTION';
        END IF;
        
        RETURN NEW;  -- Return the updated row
    END;
    $$ LANGUAGE plpgsql;
    """

create_trigger_sql = """
    CREATE TRIGGER set_block_type_trigger
    BEFORE INSERT ON blockchain.blocks
    FOR EACH ROW
    EXECUTE FUNCTION set_block_type_enum();
    """


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(trigger_function_sql)
    op.execute(create_trigger_sql)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "DROP TRIGGER IF EXISTS set_block_type_trigger ON blockchain.blocks CASCADE;"
    )
    op.execute("DROP FUNCTION IF EXISTS set_block_type_enum() CASCADE;")
    # ### end Alembic commands ###
