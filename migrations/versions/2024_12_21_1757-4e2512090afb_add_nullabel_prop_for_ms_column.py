"""add Nullabel prop for ms column

Revision ID: 4e2512090afb
Revises: d63a2384d937
Create Date: 2024-12-21 17:57:19.455796

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4e2512090afb"
down_revision: Union[str, None] = "d63a2384d937"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "metric_data", "mc", existing_type=sa.INTEGER(), nullable=True
    )
    op.create_unique_constraint(
        op.f("uq_metric_data_metric_id"), "metric_data", ["metric_id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_metric_data_metric_id"), "metric_data", type_="unique"
    )
    op.alter_column(
        "metric_data", "mc", existing_type=sa.INTEGER(), nullable=False
    )
