"""add updated_at to players

Revision ID: ff1b1aa72dec
Revises: 5275e8e3be50
Create Date: 2025-05-20 19:51:05.612499

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "ff1b1aa72dec"
down_revision: Union[str, None] = "5275e8e3be50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from libs.datetime import utcnow

    op.add_column(
        "player",
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=True, default=utcnow
        ),
    )


def downgrade() -> None:
    pass
