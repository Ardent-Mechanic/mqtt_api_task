"""Drop table metric_data

Revision ID: d88ba6034aaa
Revises: 1ef30c60747f
Create Date: 2024-12-21 15:55:08.536117

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "d88ba6034aaa"
down_revision: Union[str, None] = "1ef30c60747f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("metric_data")


def downgrade() -> None:
    op.create_table(
        "metric_data",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("bs_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "time", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "event", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
        sa.Column(
            "type", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
        sa.Column(
            "value",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("mc", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_metric_data"),
        sa.UniqueConstraint("bs_id", name="uq_metric_data_bs_id"),
    )
