"""Add pk metric_id for metric_data

Revision ID: d63a2384d937
Revises: d88ba6034aaa
Create Date: 2024-12-21 15:57:01.614168

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d63a2384d937"
down_revision: Union[str, None] = "d88ba6034aaa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "metric_data",
        sa.Column(
            "metric_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("bs_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("event", sa.String(length=50), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("mc", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("metric_id", name=op.f("pk_metric_data")),
        sa.UniqueConstraint(
            "metric_id", name=op.f("uq_metric_data_metric_id")
        ),
    )


def downgrade() -> None:
    op.drop_table("metric_data")
