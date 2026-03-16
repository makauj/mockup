"""initial_collections_schema

Revision ID: 4e1d706724c5
Revises: 
Create Date: 2026-03-16 16:24:15.735207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e1d706724c5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "collections",
        sa.Column("record_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("ID", sa.Integer(), nullable=False),
        sa.Column("Name", sa.String(), nullable=True),
        sa.Column("Email", sa.String(), nullable=True),
        sa.Column("Contact", sa.String(), nullable=True),
        sa.Column("Date", sa.Date(), server_default=sa.text("CURRENT_DATE"), nullable=True),
        sa.Column("read_only", sa.Boolean(), server_default=sa.text("FALSE"), nullable=True),
        sa.Column("last_updated_by", sa.String(), nullable=True),
        sa.Column(
            "last_updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["ID"], ["other_table.id"]),
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prevent_update_on_readonly()
        RETURNS TRIGGER AS $$
        BEGIN
            IF OLD.read_only THEN
                RAISE EXCEPTION 'Row % is read-only and cannot be modified', OLD.record_id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER trg_prevent_update_on_readonly
        BEFORE UPDATE ON collections
        FOR EACH ROW
        EXECUTE FUNCTION prevent_update_on_readonly();
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION set_audit_fields()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.last_updated_at := CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER trg_set_audit_fields
        BEFORE INSERT OR UPDATE ON collections
        FOR EACH ROW
        EXECUTE FUNCTION set_audit_fields();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_set_audit_fields ON collections;")
    op.execute("DROP FUNCTION IF EXISTS set_audit_fields();")
    op.execute("DROP TRIGGER IF EXISTS trg_prevent_update_on_readonly ON collections;")
    op.execute("DROP FUNCTION IF EXISTS prevent_update_on_readonly();")
    op.drop_table("collections")
