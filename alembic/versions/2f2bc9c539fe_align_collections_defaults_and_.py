"""align_collections_defaults_and_constraints

Revision ID: 2f2bc9c539fe
Revises: 4e1d706724c5
Create Date: 2026-03-16 16:28:28.929884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f2bc9c539fe'
down_revision: Union[str, Sequence[str], None] = '4e1d706724c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "collections",
        "Date",
        existing_type=sa.Date(),
        nullable=False,
        server_default=sa.text("CURRENT_DATE"),
    )
    op.alter_column(
        "collections",
        "read_only",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.text("FALSE"),
    )
    op.alter_column(
        "collections",
        "last_updated_at",
        existing_type=sa.TIMESTAMP(),
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    op.create_index("ix_collections_record_id", "collections", ["record_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_collections_record_id", table_name="collections")
    op.alter_column(
        "collections",
        "last_updated_at",
        existing_type=sa.TIMESTAMP(),
        nullable=True,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    op.alter_column(
        "collections",
        "read_only",
        existing_type=sa.Boolean(),
        nullable=True,
        server_default=sa.text("FALSE"),
    )
    op.alter_column(
        "collections",
        "Date",
        existing_type=sa.Date(),
        nullable=True,
        server_default=sa.text("CURRENT_DATE"),
    )
