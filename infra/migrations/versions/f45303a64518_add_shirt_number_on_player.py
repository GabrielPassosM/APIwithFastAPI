"""Add shirt_number on player

Revision ID: f45303a64518
Revises: e84428659bc8
Create Date: 2024-12-10 15:30:52.710524

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "f45303a64518"
down_revision: Union[str, None] = "e84428659bc8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("player", sa.Column("shirt_number", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("player", "shirt_number")
